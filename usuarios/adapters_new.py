"""
Adaptadores personalizados para django-allauth
Integra a autenticação social com o modelo PerfilUsuario existente.
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Adaptador personalizado para contas padrão
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Salva o usuário e cria o perfil associado
        """
        user = super().save_user(request, user, form, commit=False)
        
        if commit:
            user.save()
            # Criar o perfil automaticamente
            PerfilUsuario.objects.get_or_create(user=user)
        
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptador personalizado para contas sociais (Google, Facebook, etc.)
    """
    
    def save_user(self, request, sociallogin, form=None):
        """
        Salva o usuário vindo de login social e cria o perfil
        """
        user = super().save_user(request, sociallogin, form)
        
        # Obter dados extras do Google
        extra_data = sociallogin.account.extra_data
        
        # Criar ou atualizar o perfil - sempre cria o perfil se não existir
        perfil, created = PerfilUsuario.objects.get_or_create(user=user)
        
        # Atualizar dados do User com informações do Google
        if 'given_name' in extra_data and not user.first_name:
            user.first_name = extra_data.get('given_name', '')
        
        if 'family_name' in extra_data and not user.last_name:
            user.last_name = extra_data.get('family_name', '')
        
        if 'name' in extra_data and not user.first_name and not user.last_name:
            # Se não tem given_name/family_name, usar o nome completo no first_name
            user.first_name = extra_data.get('name', '')
        
        # Salvar dados atualizados
        user.save()
        
        return user
    
    def pre_social_login(self, request, sociallogin):
        """
        Conecta uma conta social a uma conta existente se o email for o mesmo
        """
        # Se o usuário já está logado, conectar a conta social
        if request.user.is_authenticated:
            return
        
        # Verificar se já existe um usuário com este email
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                existing_user = User.objects.get(email=email)
                # Conectar a conta social ao usuário existente
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
    
    def get_login_redirect_url(self, request):
        """
        Define para onde redirecionar após login social bem-sucedido
        """
        # Redirecionar para o perfil do usuário
        return '/usuarios/perfil/'
