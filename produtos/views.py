from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Produto, Categoria


class ProdutoListView(ListView):
    model = Produto
    template_name = 'produtos/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Produto.objects.filter(ativo=True).select_related('categoria', 'fornecedor')
        
        # Filtros
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__slug=categoria)
            
        preco_min = self.request.GET.get('preco_min')
        if preco_min:
            queryset = queryset.filter(preco__gte=preco_min)
            
        preco_max = self.request.GET.get('preco_max')
        if preco_max:
            queryset = queryset.filter(preco__lte=preco_max)
            
        # Ordenação
        ordem = self.request.GET.get('ordem', '-data_cadastro')
        queryset = queryset.order_by(ordem)
        
        return queryset


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produtos/detalhe.html'
    context_object_name = 'produto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Produto.objects.filter(ativo=True).select_related('categoria', 'fornecedor').prefetch_related('imagens', 'tags')


class ProdutoBuscarView(ListView):
    model = Produto
    template_name = 'produtos/buscar.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Produto.objects.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query) |
                Q(categoria__nome__icontains=query) |
                Q(tags__nome__icontains=query)
            ).filter(ativo=True).distinct()
        return Produto.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class CategoriaProdutosView(ListView):
    model = Produto
    template_name = 'produtos/categoria.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'], ativo=True)
        return Produto.objects.filter(categoria=self.categoria, ativo=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context
