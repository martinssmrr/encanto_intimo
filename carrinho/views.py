from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.db import transaction
import json
from .models import Carrinho, ItemCarrinho
from produtos.models import Produto


class CarrinhoMixin:
    """Mixin para obter ou criar carrinho"""
    
    def get_carrinho(self):
        if self.request.user.is_authenticated:
            carrinho, created = Carrinho.objects.get_or_create(usuario=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            carrinho, created = Carrinho.objects.get_or_create(session_key=session_key)
        return carrinho


class CarrinhoView(CarrinhoMixin, TemplateView):
    template_name = 'carrinho/carrinho.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho = self.get_carrinho()
        context['carrinho'] = carrinho
        context['itens'] = carrinho.itens.select_related('produto').all()
        context['tem_itens'] = carrinho.itens.exists()
        
        # Calcular quanto falta para frete grátis
        frete_gratis_limite = 199
        if carrinho.subtotal < frete_gratis_limite:
            context['falta_frete_gratis'] = frete_gratis_limite - carrinho.subtotal
        else:
            context['falta_frete_gratis'] = 0
            
        return context


class AdicionarItemView(CarrinhoMixin, View):
    
    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id, ativo=True)
        quantidade = int(request.POST.get('quantidade', 1))
        tamanho = request.POST.get('tamanho', '')
        cor = request.POST.get('cor', '')
        
        # Verificar estoque
        if produto.estoque_disponivel() < quantidade:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Estoque insuficiente. Disponível: {produto.estoque_disponivel()}'
                })
            messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque_disponivel()}')
            return redirect('produtos:produto_detail', slug=produto.slug)
        
        carrinho = self.get_carrinho()
        
        # Verificar se o item já existe no carrinho
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho,
            produto=produto,
            tamanho=tamanho,
            cor=cor,
            defaults={'quantidade': quantidade}
        )
        
        if not created:
            nova_quantidade = item.quantidade + quantidade
            if produto.estoque_disponivel() < nova_quantidade:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'Estoque insuficiente. Máximo disponível: {produto.estoque_disponivel()}'
                    })
                messages.error(request, f'Não é possível adicionar mais itens. Estoque máximo: {produto.estoque_disponivel()}')
                return redirect('carrinho:visualizar')
            
            item.quantidade = nova_quantidade
            item.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{produto.nome} adicionado ao carrinho!',
                'total_itens': carrinho.total_itens,
                'subtotal': float(carrinho.subtotal),
                'total': float(carrinho.total)
            })
        
        messages.success(request, f'{produto.nome} adicionado ao carrinho!')
        return redirect('carrinho:visualizar')


class AtualizarItemView(CarrinhoMixin, View):
    
    def post(self, request, item_id):
        item = get_object_or_404(ItemCarrinho, id=item_id)
        
        # Verificar se o item pertence ao carrinho do usuário
        carrinho = self.get_carrinho()
        if item.carrinho != carrinho:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Item não encontrado'})
            messages.error(request, 'Item não encontrado no seu carrinho')
            return redirect('carrinho:visualizar')
        
        quantidade = int(request.POST.get('quantidade', 1))
        
        if quantidade <= 0:
            item.delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Item removido do carrinho!',
                    'total_itens': carrinho.total_itens,
                    'subtotal': float(carrinho.subtotal),
                    'total': float(carrinho.total),
                    'removed': True
                })
            messages.success(request, 'Item removido do carrinho!')
        else:
            # Verificar estoque
            if item.produto.estoque_disponivel() < quantidade:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': f'Estoque insuficiente. Disponível: {item.produto.estoque_disponivel()}'
                    })
                messages.error(request, f'Estoque insuficiente para {item.produto.nome}')
                return redirect('carrinho:visualizar')
            
            item.quantidade = quantidade
            item.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Carrinho atualizado!',
                    'total_itens': carrinho.total_itens,
                    'subtotal': float(carrinho.subtotal),
                    'total': float(carrinho.total),
                    'item_total': float(item.total)
                })
            messages.success(request, 'Carrinho atualizado!')
        
        return redirect('carrinho:visualizar')


class RemoverItemView(CarrinhoMixin, View):
    
    def post(self, request, item_id):
        item = get_object_or_404(ItemCarrinho, id=item_id)
        
        # Verificar se o item pertence ao carrinho do usuário
        carrinho = self.get_carrinho()
        if item.carrinho != carrinho:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Item não encontrado'})
            messages.error(request, 'Item não encontrado no seu carrinho')
            return redirect('carrinho:visualizar')
        
        nome_produto = item.produto.nome
        item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{nome_produto} removido do carrinho!',
                'total_itens': carrinho.total_itens,
                'subtotal': float(carrinho.subtotal),
                'total': float(carrinho.total)
            })
        
        messages.success(request, f'{nome_produto} removido do carrinho!')
        return redirect('carrinho:visualizar')


class LimparCarrinhoView(CarrinhoMixin, View):
    
    def post(self, request):
        carrinho = self.get_carrinho()
        carrinho.limpar()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Carrinho limpo!',
                'total_itens': 0,
                'subtotal': 0,
                'total': 0
            })
        
        messages.success(request, 'Carrinho limpo!')
        return redirect('carrinho:visualizar')


class CalcularFreteView(CarrinhoMixin, View):
    
    def post(self, request):
        cep = request.POST.get('cep', '').replace('-', '').replace('.', '')
        
        if not cep or len(cep) != 8:
            return JsonResponse({
                'success': False,
                'message': 'CEP inválido'
            })
        
        carrinho = self.get_carrinho()
        
        if not carrinho.itens.exists():
            return JsonResponse({
                'success': False,
                'message': 'Carrinho vazio'
            })
        
        try:
            valor_frete = carrinho.calcular_frete(cep)
            return JsonResponse({
                'success': True,
                'frete': float(valor_frete),
                'total': float(carrinho.total),
                'message': 'Frete calculado com sucesso!' if valor_frete > 0 else 'Frete grátis!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Erro ao calcular frete'
            })


class CheckoutView(CarrinhoMixin, TemplateView):
    template_name = 'carrinho/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho = self.get_carrinho()
        
        # Verificar se há itens no carrinho
        if not carrinho.itens.exists():
            messages.error(self.request, 'Seu carrinho está vazio!')
            return redirect('carrinho:visualizar')
        
        # Verificar estoque antes do checkout
        itens_sem_estoque = []
        for item in carrinho.itens.all():
            if not item.verificar_estoque():
                itens_sem_estoque.append(item)
        
        context['carrinho'] = carrinho
        context['itens'] = carrinho.itens.select_related('produto').all()
        context['itens_sem_estoque'] = itens_sem_estoque
        context['pode_finalizar'] = len(itens_sem_estoque) == 0
        
        return context


class FinalizarCompraView(CarrinhoMixin, View):
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        carrinho = self.get_carrinho()
        
        # Verificações básicas
        if not carrinho.itens.exists():
            messages.error(request, 'Seu carrinho está vazio!')
            return redirect('carrinho:visualizar')
        
        # Verificar estoque novamente
        for item in carrinho.itens.all():
            if not item.verificar_estoque():
                messages.error(request, f'Produto {item.produto.nome} não tem estoque suficiente!')
                return redirect('carrinho:checkout')
        
        # Dados do formulário
        dados_cliente = {
            'nome': request.POST.get('nome'),
            'email': request.POST.get('email'),
            'telefone': request.POST.get('telefone'),
            'cep': request.POST.get('cep'),
            'endereco': request.POST.get('endereco'),
            'numero': request.POST.get('numero'),
            'complemento': request.POST.get('complemento'),
            'bairro': request.POST.get('bairro'),
            'cidade': request.POST.get('cidade'),
            'estado': request.POST.get('estado'),
            'forma_pagamento': request.POST.get('forma_pagamento'),
        }
        
        # Validações básicas
        campos_obrigatorios = ['nome', 'email', 'telefone', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'forma_pagamento']
        for campo in campos_obrigatorios:
            if not dados_cliente.get(campo):
                messages.error(request, f'Campo {campo} é obrigatório!')
                return redirect('carrinho:checkout')
        
        try:
            with transaction.atomic():
                # Criar pedido (implementar na próxima etapa)
                # Por enquanto, apenas limpar o carrinho
                carrinho.limpar()
                messages.success(request, 'Pedido realizado com sucesso! Em breve você receberá a confirmação por e-mail.')
                return redirect('home')
                
        except Exception as e:
            messages.error(request, 'Erro ao processar pedido. Tente novamente.')
            return redirect('carrinho:checkout')
