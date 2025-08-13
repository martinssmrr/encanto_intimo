from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, UpdateView, ListView
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import PerfilUsuario
from .forms import CadastroUsuarioForm, EditarPerfilForm
from pedidos.models import Pedido


class LoginView(DjangoLoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True


class LogoutView(TemplateView):
    template_name = 'usuarios/logout.html'
    
    def get(self, request, *args, **kwargs):
        """Faz logout do usuário e exibe a página de confirmação"""
        logout(request)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'usuarios/cadastro.html'
    form_class = CadastroUsuarioForm
    success_url = reverse_lazy('usuarios:login')
    success_message = "Conta criada com sucesso! Faça login para continuar."
    
    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(
                self.request, 
                f'Bem-vindo(a), {user.get_full_name()}! Sua conta foi criada com sucesso. '
                'Agora você pode fazer login e aproveitar nossas ofertas exclusivas!'
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(
                self.request, 
                'Ocorreu um erro ao criar sua conta. Tente novamente ou entre em contato conosco.'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor, corrija os erros abaixo e tente novamente.'
        )
        return super().form_invalid(form)


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Criar perfil se não existir
        perfil, created = PerfilUsuario.objects.get_or_create(user=self.request.user)
        
        context['perfil'] = perfil
        context['usuario'] = self.request.user
        context['pedidos_recentes'] = Pedido.objects.filter(
            usuario=self.request.user
        ).order_by('-data_pedido')[:5]
        context['total_pedidos'] = Pedido.objects.filter(usuario=self.request.user).count()
        
        # Formulário de edição pré-preenchido
        context['form'] = EditarPerfilForm(instance=perfil, user=self.request.user)
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Processar formulário de edição do perfil"""
        perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
        form = EditarPerfilForm(
            request.POST, 
            request.FILES, 
            instance=perfil, 
            user=request.user
        )
        
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, 
                    '✅ Seu perfil foi atualizado com sucesso!'
                )
                return redirect('usuarios:perfil')
            except Exception as e:
                messages.error(
                    request,
                    '❌ Ocorreu um erro ao atualizar seu perfil. Tente novamente.'
                )
        else:
            messages.error(
                request,
                '❌ Por favor, corrija os erros abaixo e tente novamente.'
            )
        
        # Se houve erro, recarregar página com erros
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class EditarPerfilView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PerfilUsuario
    template_name = 'usuarios/editar_perfil.html'
    fields = ['telefone', 'data_nascimento', 'cpf', 'cep', 'endereco', 'numero', 
              'complemento', 'bairro', 'cidade', 'estado', 'aceita_newsletter', 'aceita_promocoes']
    success_url = reverse_lazy('usuarios:perfil')
    success_message = "Perfil atualizado com sucesso!"
    
    def get_object(self):
        return self.request.user.perfil


class MeusPedidosView(LoginRequiredMixin, ListView):
    template_name = 'usuarios/meus_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-data_pedido')
