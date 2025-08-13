from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from pedidos.models import Pedido
from usuarios.forms import EditarPerfilForm

def test_perfil_view(request):
    """View de teste para debug do perfil"""
    try:
        # Criar ou pegar um usuário de teste
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@test.com',
                'first_name': 'Usuário',
                'last_name': 'Teste'
            }
        )
        
        # Criar perfil se não existir
        perfil, created = PerfilUsuario.objects.get_or_create(user=user)
        
        # Dados para o template
        context = {
            'perfil': perfil,
            'usuario': user,
            'pedidos_recentes': Pedido.objects.filter(usuario=user)[:5],
            'total_pedidos': Pedido.objects.filter(usuario=user).count(),
            'form': EditarPerfilForm(instance=perfil, user=user)
        }
        
        return render(request, 'usuarios/perfil.html', context)
    
    except Exception as e:
        return HttpResponse(f"Erro: {str(e)}")
