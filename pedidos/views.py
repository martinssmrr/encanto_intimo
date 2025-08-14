from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from .models import Pedido, ItemPedido, StatusPedido
from carrinho.models import Carrinho
from produtos.models import Produto
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json


class CheckoutView(LoginRequiredMixin, TemplateView):
    """
    View para exibir a página de checkout com os itens do carrinho
    e formulário de endereço de entrega.
    """
    template_name = 'pedidos/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            carrinho = Carrinho.objects.get(usuario=self.request.user)
            context['carrinho'] = carrinho
            context['itens'] = carrinho.itens.all()
            
            # Verificar se há itens no carrinho
            if not carrinho.itens.exists():
                messages.warning(self.request, 'Seu carrinho está vazio!')
                context['carrinho_vazio'] = True
                
        except Carrinho.DoesNotExist:
            context['carrinho'] = None
            context['itens'] = []
            context['carrinho_vazio'] = True
            
        return context


class MeusPedidosView(LoginRequiredMixin, ListView):
    """
    View para listar todos os pedidos do usuário logado.
    """
    model = Pedido
    template_name = 'pedidos/meus_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10
    
    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user
        ).prefetch_related('itens__produto').order_by('-data_pedido')


@login_required
@require_POST
def finalizar_pedido(request):
    """
    Processa a finalização do pedido.
    Valida estoque, cria pedido e redireciona para pagamento.
    """
    try:
        with transaction.atomic():
            # Obter carrinho do usuário
            carrinho = get_object_or_404(Carrinho, usuario=request.user)
            
            if not carrinho.itens.exists():
                messages.error(request, 'Seu carrinho está vazio!')
                return redirect('carrinho:carrinho')
            
            # Validar dados do formulário
            dados_entrega = {
                'nome_cliente': request.POST.get('nome_cliente'),
                'email_cliente': request.POST.get('email_cliente'),
                'telefone_cliente': request.POST.get('telefone_cliente'),
                'cep': request.POST.get('cep'),
                'endereco': request.POST.get('endereco'),
                'numero': request.POST.get('numero'),
                'complemento': request.POST.get('complemento', ''),
                'bairro': request.POST.get('bairro'),
                'cidade': request.POST.get('cidade'),
                'estado': request.POST.get('estado'),
                'forma_pagamento': request.POST.get('forma_pagamento'),
                'observacoes': request.POST.get('observacoes', ''),
            }
            
            # Validar campos obrigatórios
            campos_obrigatorios = [
                'nome_cliente', 'email_cliente', 'telefone_cliente',
                'cep', 'endereco', 'numero', 'bairro', 'cidade', 
                'estado', 'forma_pagamento'
            ]
            
            for campo in campos_obrigatorios:
                if not dados_entrega.get(campo):
                    messages.error(request, f'O campo {campo.replace("_", " ").title()} é obrigatório!')
                    return redirect('pedidos:checkout')
            
            # Validar estoque antes de criar o pedido
            itens_validados = []
            for item_carrinho in carrinho.itens.all():
                produto = item_carrinho.produto
                
                # Verificar se o produto ainda está ativo
                if not produto.ativo:
                    messages.error(request, f'O produto "{produto.nome}" não está mais disponível.')
                    return redirect('carrinho:carrinho')
                
                # Verificar estoque
                if produto.estoque < item_carrinho.quantidade:
                    messages.error(
                        request, 
                        f'Estoque insuficiente para "{produto.nome}". '
                        f'Disponível: {produto.estoque}, Solicitado: {item_carrinho.quantidade}'
                    )
                    return redirect('carrinho:carrinho')
                
                itens_validados.append(item_carrinho)
            
            # Criar o pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                subtotal=carrinho.subtotal,
                valor_frete=carrinho.valor_frete,
                total=carrinho.total,
                **dados_entrega
            )
            
            # Criar itens do pedido e reduzir estoque temporariamente
            for item_carrinho in itens_validados:
                produto = item_carrinho.produto
                
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    nome_produto=produto.nome,
                    preco_unitario=item_carrinho.preco_unitario,
                    quantidade=item_carrinho.quantidade,
                    tamanho=getattr(item_carrinho, 'tamanho', ''),
                    cor=getattr(item_carrinho, 'cor', ''),
                    fornecedor_nome=produto.fornecedor.nome if produto.fornecedor else '',
                    fornecedor_email=produto.fornecedor.email if produto.fornecedor else '',
                )
                
                # Reservar estoque (será confirmado após pagamento)
                produto.estoque -= item_carrinho.quantidade
                produto.save()
            
            # Criar histórico de status inicial
            StatusPedido.objects.create(
                pedido=pedido,
                status='pendente',
                observacao='Pedido criado e aguardando pagamento',
                usuario_alteracao=request.user
            )
            
            # Limpar carrinho
            carrinho.limpar()
            
            # Enviar email de confirmação
            enviar_email_status_pedido(pedido, 'criado')
            
            messages.success(request, f'Pedido #{str(pedido.numero_pedido)[:8]} criado com sucesso!')
            
            # Redirecionar para pagamento
            return redirect('pedidos:pagamento', numero_pedido=pedido.numero_pedido)
            
    except Exception as e:
        messages.error(request, f'Erro ao processar pedido: {str(e)}')
        return redirect('pedidos:checkout')


class PagamentoView(LoginRequiredMixin, DetailView):
    """
    View para exibir opções de pagamento do pedido.
    """
    model = Pedido
    template_name = 'pedidos/pagamento.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user,
            status='pendente'
        )


@csrf_exempt
def confirmar_pagamento(request):
    """
    Webhook para confirmar pagamento via gateway (Mercado Pago, etc).
    """
    if request.method == 'POST':
        try:
            # Para este exemplo, vamos simular confirmação manual
            data = json.loads(request.body)
            numero_pedido = data.get('pedido_id')
            status_pagamento = data.get('status')
            transaction_id = data.get('transaction_id')
            
            pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido)
            
            if status_pagamento == 'approved':
                with transaction.atomic():
                    # Confirmar pagamento
                    pedido.pagamento_confirmado = True
                    pedido.transaction_id = transaction_id
                    pedido.status = 'confirmado'
                    pedido.save()
                    
                    # Atualizar histórico
                    StatusPedido.objects.create(
                        pedido=pedido,
                        status='confirmado',
                        observacao=f'Pagamento confirmado. ID: {transaction_id}'
                    )
                    
                    # Enviar email
                    enviar_email_status_pedido(pedido, 'pago')
                    
                return JsonResponse({'status': 'success'})
            
            elif status_pagamento == 'rejected':
                # Restaurar estoque em caso de rejeição
                with transaction.atomic():
                    for item in pedido.itens.all():
                        produto = item.produto
                        produto.estoque += item.quantidade
                        produto.save()
                    
                    pedido.status = 'cancelado'
                    pedido.save()
                    
                    StatusPedido.objects.create(
                        pedido=pedido,
                        status='cancelado',
                        observacao='Pagamento rejeitado - estoque restaurado'
                    )
                    
                return JsonResponse({'status': 'payment_rejected'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'invalid_method'})


@login_required
def confirmar_pagamento_manual(request, numero_pedido):
    """
    Simula confirmação manual de pagamento para testes.
    """
    pedido = get_object_or_404(
        Pedido, 
        numero_pedido=numero_pedido, 
        usuario=request.user,
        status='pendente'
    )
    
    with transaction.atomic():
        pedido.pagamento_confirmado = True
        pedido.transaction_id = f'MANUAL_{timezone.now().strftime("%Y%m%d%H%M%S")}'
        pedido.status = 'confirmado'
        pedido.save()
        
        StatusPedido.objects.create(
            pedido=pedido,
            status='confirmado',
            observacao='Pagamento confirmado manualmente (teste)',
            usuario_alteracao=request.user
        )
        
        enviar_email_status_pedido(pedido, 'pago')
        
    messages.success(request, 'Pagamento confirmado com sucesso!')
    return redirect('pedidos:confirmacao', numero_pedido=numero_pedido)


class ConfirmacaoView(LoginRequiredMixin, DetailView):
    """
    View para exibir confirmação do pedido após pagamento.
    """
    model = Pedido
    template_name = 'pedidos/confirmacao.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    """
    View para exibir detalhes completos do pedido.
    """
    model = Pedido
    template_name = 'pedidos/detalhe.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).prefetch_related('itens')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historico'] = self.object.historico_status.all()
        return context


class RastrearPedidoView(DetailView):
    """
    View pública para rastreamento de pedido (não requer login).
    """
    model = Pedido
    template_name = 'pedidos/rastrear.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historico'] = self.object.historico_status.all()
        return context


@login_required
def cancelar_pedido(request, numero_pedido):
    """
    Permite cancelar pedido se ainda estiver em status que permite cancelamento.
    """
    pedido = get_object_or_404(
        Pedido, 
        numero_pedido=numero_pedido, 
        usuario=request.user
    )
    
    if not pedido.pode_cancelar():
        messages.error(request, 'Este pedido não pode mais ser cancelado.')
        return redirect('pedidos:detalhe', numero_pedido=numero_pedido)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', 'Cancelado pelo cliente')
        
        with transaction.atomic():
            # Restaurar estoque
            for item in pedido.itens.all():
                produto = item.produto
                produto.estoque += item.quantidade
                produto.save()
            
            # Atualizar status do pedido
            pedido.status = 'cancelado'
            pedido.save()
            
            # Registrar no histórico
            StatusPedido.objects.create(
                pedido=pedido,
                status='cancelado',
                observacao=f'Cancelado pelo cliente. Motivo: {motivo}',
                usuario_alteracao=request.user
            )
            
            # Enviar email
            enviar_email_status_pedido(pedido, 'cancelado')
            
        messages.success(request, 'Pedido cancelado com sucesso!')
        return redirect('pedidos:meus_pedidos')
    
    return render(request, 'pedidos/cancelar.html', {'pedido': pedido})


def enviar_email_status_pedido(pedido, acao):
    """
    Envia email para o cliente informando sobre mudanças no status do pedido.
    """
    try:
        assuntos = {
            'criado': f'Pedido #{str(pedido.numero_pedido)[:8]} - Criado com Sucesso!',
            'pago': f'Pedido #{str(pedido.numero_pedido)[:8]} - Pagamento Confirmado!',
            'enviado': f'Pedido #{str(pedido.numero_pedido)[:8]} - Enviado!',
            'entregue': f'Pedido #{str(pedido.numero_pedido)[:8]} - Entregue!',
            'cancelado': f'Pedido #{str(pedido.numero_pedido)[:8]} - Cancelado',
        }
        
        mensagens = {
            'criado': f'Seu pedido foi criado com sucesso e está aguardando pagamento.\n\n'
                     f'Total: R$ {pedido.total}\n'
                     f'Forma de pagamento: {pedido.get_forma_pagamento_display()}\n\n'
                     f'Você pode acompanhar o status do seu pedido em nosso site.',
            
            'pago': f'Seu pagamento foi confirmado com sucesso!\n\n'
                   f'Agora seu pedido entrará em processamento e será enviado em breve.\n'
                   f'Você receberá um email com o código de rastreamento assim que o produto for despachado.',
            
            'enviado': f'Seu pedido foi enviado!\n\n'
                      f'Código de rastreamento: {pedido.codigo_rastreamento}\n'
                      f'Você pode acompanhar a entrega através do nosso site ou diretamente nos Correios.',
            
            'entregue': f'Seu pedido foi entregue com sucesso!\n\n'
                       f'Esperamos que você tenha gostado dos produtos.\n'
                       f'Sua opinião é muito importante para nós!',
            
            'cancelado': f'Seu pedido foi cancelado.\n\n'
                        f'Se o pagamento já foi realizado, o estorno será processado em até 5 dias úteis.\n'
                        f'Em caso de dúvidas, entre em contato conosco.'
        }
        
        send_mail(
            subject=assuntos.get(acao, 'Atualização do Pedido'),
            message=mensagens.get(acao, 'Seu pedido foi atualizado.'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[pedido.email_cliente],
            fail_silently=True,
        )
        
    except Exception as e:
        print(f'Erro ao enviar email: {e}')  # Log do erro
