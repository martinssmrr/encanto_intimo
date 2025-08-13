from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime
from decimal import Decimal


class EncantoIntimoAdminSite(AdminSite):
    """
    Site Admin personalizado para Encanto Íntimo
    Tema elegante com cores: Vermelho (#B71C1C), Preto (#000000), Dourado (#FFD700)
    """
    site_header = '🎀 Encanto Íntimo - Painel Administrativo'
    site_title = 'Encanto Íntimo Admin'
    index_title = 'Dashboard Executivo'
    site_url = None  # Remove o link "Ver site"
    index_template = 'admin/dashboard.html'  # Template personalizado
    
    def index(self, request, extra_context=None):
        """
        Dashboard personalizado com estatísticas avançadas
        """
        # Calcular estatísticas
        now = timezone.now()
        current_month = now.month
        current_year = now.year
        
        # Inicializar variáveis
        total_pedidos = 0
        pedidos_pendentes = 0
        total_usuarios = 0
        vendas_mes = Decimal('0.00')
        produtos_ativos = 0
        recent_orders = []
        alerts = []
        
        # Tentar buscar dados dos pedidos
        try:
            from pedidos.models import Pedido
            total_pedidos = Pedido.objects.count()
            pedidos_pendentes = Pedido.objects.filter(status='pendente').count()
            
            # Vendas do mês
            vendas_mes = Pedido.objects.filter(
                data_pedido__year=current_year,
                data_pedido__month=current_month,
                pagamento_confirmado=True
            ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
            
            # Pedidos recentes (últimos 10)
            recent_orders = Pedido.objects.select_related('usuario').order_by('-data_pedido')[:10]
            
            # Verificar pedidos pendentes há mais de 24h
            from datetime import timedelta
            pedidos_antigos = Pedido.objects.filter(
                status='pendente',
                data_pedido__lt=now - timedelta(days=1)
            ).count()
            
            if pedidos_antigos > 0:
                alerts.append({
                    'type': 'warning',
                    'title': 'Atenção',
                    'message': f'{pedidos_antigos} pedidos pendentes há mais de 24 horas'
                })
                
        except ImportError:
            pass
        
        # Buscar dados dos usuários (substituto para clientes)
        try:
            from django.contrib.auth.models import User
            total_usuarios = User.objects.filter(is_active=True).count()
        except ImportError:
            pass
        
        # Tentar buscar dados dos produtos
        try:
            from produtos.models import Produto
            produtos_ativos = Produto.objects.filter(ativo=True).count()
            
            # Verificar produtos sem estoque
            produtos_sem_estoque = Produto.objects.filter(
                ativo=True,
                estoque_virtual=0
            ).count()
            
            if produtos_sem_estoque > 0:
                alerts.append({
                    'type': 'info',
                    'title': 'Estoque',
                    'message': f'{produtos_sem_estoque} produtos sem estoque'
                })
                
        except ImportError:
            pass
        
        # Contexto para o template personalizado
        context = {
            'title': 'Dashboard Encanto Íntimo',
            'subtitle': None,
            'total_pedidos': total_pedidos,
            'pedidos_pendentes': pedidos_pendentes,
            'total_clientes': total_usuarios,  # Usando usuários como proxy para clientes
            'vendas_mes': vendas_mes,
            'produtos_ativos': produtos_ativos,
            'recent_orders': recent_orders,
            'alerts': alerts,
            'current_month': current_month,
            'current_year': current_year,
            'current_month_name': now.strftime('%B'),
            'last_check': now.strftime('%H:%M:%S'),
            'last_update': now.strftime('%d/%m/%Y %H:%M'),
            'system_status': 'Operacional',
            'low_stock_products': [],  # Placeholder
            'pending_orders_count': pedidos_pendentes,
            'app_list': self.get_app_list(request),
        }
        
        if extra_context:
            context.update(extra_context)
        
        # Usar template personalizado para dashboard
        return TemplateResponse(request, 'admin/dashboard.html', context)


# Instância personalizada do admin
admin_site = EncantoIntimoAdminSite(name='encanto_admin')

# Registrar os models no site personalizado
def register_models():
    """Registra todos os models no admin personalizado"""
    
    # Registrar Pedidos
    try:
        from pedidos.models import Pedido, ItemPedido, StatusPedido
        from django.contrib import admin
        
        class PedidoAdminSimples(admin.ModelAdmin):
            list_display = ['numero_pedido', 'usuario', 'status', 'total', 'data_pedido']
            list_filter = ['status', 'pagamento_confirmado', 'data_pedido']
            search_fields = ['numero_pedido', 'usuario__username', 'usuario__email']
            readonly_fields = ['numero_pedido', 'data_pedido']
        
        class ItemPedidoAdminSimples(admin.ModelAdmin):
            list_display = ['pedido', 'nome_produto', 'quantidade', 'preco_unitario']
            list_filter = ['produto']
            search_fields = ['nome_produto']
        
        class StatusPedidoAdminSimples(admin.ModelAdmin):
            list_display = ['pedido', 'status']
            list_filter = ['status']
        
        admin_site.register(Pedido, PedidoAdminSimples)
        admin_site.register(ItemPedido, ItemPedidoAdminSimples)
        admin_site.register(StatusPedido, StatusPedidoAdminSimples)
        
    except ImportError as e:
        print(f"Erro ao importar pedidos: {e}")
    
    # Registrar Produtos
    try:
        from produtos.models import Produto, Categoria, Tag, ImagemProduto
        from django.contrib import admin
        
        class ProdutoAdminSimples(admin.ModelAdmin):
            list_display = ['nome', 'categoria', 'preco', 'estoque_virtual', 'ativo']
            list_filter = ['categoria', 'ativo']
            search_fields = ['nome', 'descricao']
            list_editable = ['preco', 'estoque_virtual', 'ativo']
        
        class CategoriaAdminSimples(admin.ModelAdmin):
            list_display = ['nome', 'ativo']
            list_filter = ['ativo']
            search_fields = ['nome']
        
        class TagAdminSimples(admin.ModelAdmin):
            list_display = ['nome']
            search_fields = ['nome']
        
        class ImagemProdutoAdminSimples(admin.ModelAdmin):
            list_display = ['produto', 'ordem']
        
        admin_site.register(Produto, ProdutoAdminSimples)
        admin_site.register(Categoria, CategoriaAdminSimples)
        admin_site.register(Tag, TagAdminSimples)
        admin_site.register(ImagemProduto, ImagemProdutoAdminSimples)
        
    except ImportError as e:
        print(f"Erro ao importar produtos: {e}")
    
    # Registrar Fornecedores
    try:
        from fornecedores.models import Fornecedor
        from django.contrib import admin
        
        class FornecedorAdminSimples(admin.ModelAdmin):
            list_display = ['nome', 'email', 'telefone', 'ativo']
            list_filter = ['ativo']
            search_fields = ['nome', 'email', 'telefone']
        
        admin_site.register(Fornecedor, FornecedorAdminSimples)
        
    except ImportError as e:
        print(f"Erro ao importar fornecedores: {e}")
    
    # Registrar Usuários
    try:
        from usuarios.models import PerfilUsuario
        from django.contrib.auth.models import User, Group
        from django.contrib.auth.admin import UserAdmin, GroupAdmin
        from django.contrib import admin
        
        class PerfilUsuarioAdminSimples(admin.ModelAdmin):
            list_display = ['get_username', 'telefone', 'get_email']
            search_fields = ['usuario__username', 'usuario__email', 'telefone']
            
            def get_username(self, obj):
                return obj.usuario.username if obj.usuario else '-'
            get_username.short_description = 'Usuário'
            
            def get_email(self, obj):
                return obj.usuario.email if obj.usuario else '-'
            get_email.short_description = 'E-mail'
        
        admin_site.register(PerfilUsuario, PerfilUsuarioAdminSimples)
        admin_site.register(User, UserAdmin)
        admin_site.register(Group, GroupAdmin)
        
    except ImportError as e:
        print(f"Erro ao importar usuarios: {e}")
    
    # Registrar Pagamentos
    try:
        from pagamentos.models import Pagamento, LogPagamento
        from django.contrib import admin
        
        class PagamentoAdminSimples(admin.ModelAdmin):
            list_display = ['pedido', 'valor', 'status', 'data_criacao']
            list_filter = ['status', 'data_criacao']
            search_fields = ['pedido__numero_pedido']
        
        class LogPagamentoAdminSimples(admin.ModelAdmin):
            list_display = ['pagamento']
        
        admin_site.register(Pagamento, PagamentoAdminSimples)
        admin_site.register(LogPagamento, LogPagamentoAdminSimples)
        
    except ImportError as e:
        print(f"Erro ao importar pagamentos: {e}")

# Registrar modelos automaticamente
register_models()
