from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.conf import settings
import json
import logging

from .models import Pagamento
from .services import MercadoPagoService
from carrinho.models import Carrinho
from pedidos.models import Pedido, ItemPedido
from produtos.models import Produto

logger = logging.getLogger(__name__)


class ProcessarPagamentoView(LoginRequiredMixin, View):
    """View para processar pagamento via Mercado Pago"""
    
    def post(self, request):
        """Cria preferência e redireciona para Mercado Pago"""
        try:
            # Verificar se há itens no carrinho
            try:
                carrinho = Carrinho.objects.get(usuario=request.user)
                carrinho_items = carrinho.itens.all()
            except Carrinho.DoesNotExist:
                messages.error(request, "Seu carrinho está vazio!")
                return redirect('carrinho:visualizar')
            
            if not carrinho_items.exists():
                messages.error(request, "Seu carrinho está vazio!")
                return redirect('carrinho:visualizar')
            
            # Criar o pedido primeiro
            with transaction.atomic():
                pedido = self._criar_pedido_do_carrinho(request.user, carrinho_items)
                
                # Criar preferência no Mercado Pago
                mp_service = MercadoPagoService()
                resultado = mp_service.criar_preferencia_pagamento(
                    carrinho_items, 
                    pedido.numero_pedido, 
                    request
                )
                
                if resultado["status"] == "success":
                    # Salvar informações do pagamento
                    Pagamento.objects.create(
                        pedido=pedido,
                        preference_id=resultado["preference_id"],
                        status='pendente',
                        forma_pagamento='mercado_pago'
                    )
                    
                    # Usar sandbox_init_point em desenvolvimento
                    if settings.MERCADO_PAGO.get('SANDBOX', True):
                        redirect_url = resultado["sandbox_init_point"]
                    else:
                        redirect_url = resultado["init_point"]
                    
                    # Limpar carrinho após criar pedido
                    carrinho.limpar()
                    
                    # Redirecionar para Mercado Pago
                    return redirect(redirect_url)
                else:
                    messages.error(request, f"Erro ao processar pagamento: {resultado.get('message', 'Erro desconhecido')}")
                    # Excluir pedido se não conseguiu criar preferência
                    pedido.delete()
                    return redirect('carrinho:visualizar')
                    
        except Exception as e:
            logger.error(f"Erro ao processar pagamento: {str(e)}")
            messages.error(request, "Erro interno. Tente novamente.")
            return redirect('carrinho:visualizar')
    
    def _criar_pedido_do_carrinho(self, usuario, carrinho_items):
        """Cria pedido a partir dos itens do carrinho"""
        from decimal import Decimal
        
        # Calcular totais
        subtotal = Decimal('0.00')
        for item in carrinho_items:
            subtotal += item.produto.preco_final * item.quantidade
        
        # Verificar se o usuário tem endereço padrão (simplificado)
        pedido_data = {
            'usuario': usuario,
            'nome_cliente': usuario.get_full_name() or usuario.username,
            'email_cliente': usuario.email,
            'telefone_cliente': getattr(usuario, 'telefone', ''),
            'status': 'pendente',
            'forma_pagamento': 'mercado_pago',
            'subtotal': subtotal,
            'valor_frete': Decimal('0.00'),  # Frete grátis por padrão
            'desconto': Decimal('0.00'),
            'total': subtotal,
            'pagamento_confirmado': False,
            # Endereço padrão (pode ser melhorado para pegar do perfil do usuário)
            'endereco': 'Endereço a definir',
            'numero': '000',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '00000-000'
        }
        
        pedido = Pedido.objects.create(**pedido_data)
        
        # Criar itens do pedido
        for item in carrinho_items:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                nome_produto=item.produto.nome,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco_final,
                tamanho=getattr(item, 'tamanho', ''),
                cor=getattr(item, 'cor', ''),
                fornecedor_nome=getattr(item.produto, 'fornecedor', '')
            )
        
        return pedido


@method_decorator(csrf_exempt, name='dispatch')
class MercadoPagoWebhookView(View):
    """Webhook para receber notificações do Mercado Pago"""
    
    def post(self, request):
        try:
            # Parse do JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()
            
            logger.info(f"Webhook MP recebido: {data}")
            
            # Processar notificação
            mp_service = MercadoPagoService()
            resultado = mp_service.processar_webhook_notification(data)
            
            if resultado["status"] == "success":
                # Atualizar pedido baseado no pagamento
                self._atualizar_pedido_por_pagamento(resultado)
                
            return HttpResponse(status=200)
            
        except Exception as e:
            logger.error(f"Erro no webhook MP: {str(e)}")
            return HttpResponse(status=500)
    
    def _atualizar_pedido_por_pagamento(self, payment_info):
        """Atualiza status do pedido baseado no pagamento"""
        try:
            external_reference = payment_info.get("external_reference")
            payment_status = payment_info.get("payment_status")
            
            if external_reference:
                pedido = Pedido.objects.get(numero_pedido=external_reference)
                pagamento = Pagamento.objects.get(pedido=pedido)
                
                # Mapear status do MP para status do sistema
                if payment_status == "approved":
                    pedido.status = 'confirmado'
                    pedido.pagamento_confirmado = True
                    pagamento.status = 'aprovado'
                    
                elif payment_status == "rejected":
                    pedido.status = 'cancelado'
                    pagamento.status = 'rejeitado'
                    
                elif payment_status in ["pending", "in_process"]:
                    pagamento.status = 'pendente'
                
                # Salvar payment_id e dados adicionais
                pagamento.payment_id = payment_info.get("payment_data", {}).get("id")
                pagamento.transaction_amount = payment_info.get("transaction_amount")
                pagamento.payment_method = payment_info.get("payment_method")
                
                pedido.save()
                pagamento.save()
                
                logger.info(f"Pedido {external_reference} atualizado para status {payment_status}")
                
        except (Pedido.DoesNotExist, Pagamento.DoesNotExist) as e:
            logger.error(f"Pedido/Pagamento não encontrado: {str(e)}")
        except Exception as e:
            logger.error(f"Erro ao atualizar pedido: {str(e)}")


class PagamentoSucessoView(LoginRequiredMixin, TemplateView):
    """View para página de sucesso do pagamento"""
    template_name = 'pagamentos/sucesso.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obter informações do pagamento da URL
        payment_id = self.request.GET.get('payment_id')
        external_reference = self.request.GET.get('external_reference')
        
        if external_reference:
            try:
                pedido = Pedido.objects.get(numero_pedido=external_reference)
                context['pedido'] = pedido
                
                if payment_id:
                    # Verificar status do pagamento no MP
                    mp_service = MercadoPagoService()
                    payment_info = mp_service.verificar_pagamento(payment_id)
                    context['payment_info'] = payment_info
                    
            except Pedido.DoesNotExist:
                messages.error(self.request, "Pedido não encontrado.")
        
        return context


class PagamentoFalhaView(LoginRequiredMixin, TemplateView):
    """View para página de falha do pagamento"""
    template_name = 'pagamentos/falha.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        external_reference = self.request.GET.get('external_reference')
        if external_reference:
            try:
                pedido = Pedido.objects.get(numero_pedido=external_reference)
                context['pedido'] = pedido
            except Pedido.DoesNotExist:
                pass
        
        return context


class PagamentoPendenteView(LoginRequiredMixin, TemplateView):
    """View para página de pagamento pendente"""
    template_name = 'pagamentos/pendente.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        external_reference = self.request.GET.get('external_reference')
        if external_reference:
            try:
                pedido = Pedido.objects.get(numero_pedido=external_reference)
                context['pedido'] = pedido
            except Pedido.DoesNotExist:
                pass
        
        return context


class PagamentoCanceladoView(LoginRequiredMixin, TemplateView):
    template_name = 'pagamentos/cancelado.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        external_reference = self.request.GET.get('external_reference')
        if external_reference:
            try:
                pedido = Pedido.objects.get(numero_pedido=external_reference)
                context['pedido'] = pedido
            except Pedido.DoesNotExist:
                pass
        
        return context
