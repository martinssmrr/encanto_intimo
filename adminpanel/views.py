from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from produtos.models import Produto
from fornecedores.models import Fornecedor
from pedidos.models import Pedido


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'adminpanel/dashboard.html'


# Views de Produtos
class ProdutoListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Produto
    template_name = 'adminpanel/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 20


class ProdutoDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Produto
    template_name = 'adminpanel/produto_detail.html'
    context_object_name = 'produto'


class ProdutoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Produto
    template_name = 'adminpanel/produto_form.html'
    fields = '__all__'
    success_url = reverse_lazy('adminpanel:produto_list')


class ProdutoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Produto
    template_name = 'adminpanel/produto_form.html'
    fields = '__all__'
    success_url = reverse_lazy('adminpanel:produto_list')


class ProdutoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Produto
    template_name = 'adminpanel/produto_confirm_delete.html'
    success_url = reverse_lazy('adminpanel:produto_list')


# Views de Fornecedores
class FornecedorListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'adminpanel/fornecedor_list.html'
    context_object_name = 'fornecedores'
    paginate_by = 20


class FornecedorDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Fornecedor
    template_name = 'adminpanel/fornecedor_detail.html'
    context_object_name = 'fornecedor'


class FornecedorCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Fornecedor
    template_name = 'adminpanel/fornecedor_form.html'
    fields = '__all__'
    success_url = reverse_lazy('adminpanel:fornecedor_list')


class FornecedorUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Fornecedor
    template_name = 'adminpanel/fornecedor_form.html'
    fields = '__all__'
    success_url = reverse_lazy('adminpanel:fornecedor_list')


class FornecedorDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'adminpanel/fornecedor_confirm_delete.html'
    success_url = reverse_lazy('adminpanel:fornecedor_list')


# Views de Pedidos
class PedidoListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Pedido
    template_name = 'adminpanel/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 20


class PedidoDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Pedido
    template_name = 'adminpanel/pedido_detail.html'
    context_object_name = 'pedido'
    slug_field = 'numero_pedido'
    slug_url_kwarg = 'numero_pedido'


class AtualizarStatusView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'adminpanel/atualizar_status.html'


class RelatoriosView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'adminpanel/relatorios.html'
