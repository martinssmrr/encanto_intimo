from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Admin customizado para Cliente com funcionalidades avançadas
    """
    
    # Configurações de listagem
    list_display = [
        'nome_completo', 
        'email', 
        'telefone', 
        'cidade_estado', 
        'tem_usuario_sistema',
        'total_pedidos_display',
        'valor_total_display',
        'ultimo_pedido_display',
        'ativo',
        'data_cadastro'
    ]
    
    list_filter = [
        'ativo',
        'estado',
        'aceita_newsletter',
        'aceita_promocoes',
        'data_cadastro',
        ('usuario', admin.EmptyFieldListFilter),  # Filtro para clientes com/sem usuário
    ]
    
    search_fields = [
        'nome_completo',
        'email',
        'telefone',
        'cpf',
        'cidade',
        'usuario__username',
        'usuario__first_name',
        'usuario__last_name'
    ]
    
    readonly_fields = [
        'data_cadastro',
        'data_atualizacao',
        'total_pedidos_display',
        'valor_total_display',
        'ultimo_pedido_display',
        'endereco_completo_display'
    ]
    
    list_editable = ['ativo', 'aceita_newsletter']
    
    ordering = ['-data_cadastro']
    
    list_per_page = 25
    
    # Configuração de campos em fieldsets
    fieldsets = (
        ('👤 Dados Pessoais', {
            'fields': ('nome_completo', 'email', 'telefone', 'cpf', 'data_nascimento'),
            'classes': ('wide',),
        }),
        ('🏠 Endereço', {
            'fields': (
                ('cep', 'estado'),
                ('endereco', 'numero'),
                ('complemento', 'bairro'),
                'cidade',
                'endereco_completo_display'
            ),
            'classes': ('wide',),
        }),
        ('👥 Vinculação com Usuário', {
            'fields': ('usuario',),
            'description': 'Se o cliente possui conta no sistema'
        }),
        ('⚙️ Preferências', {
            'fields': (
                ('aceita_newsletter', 'aceita_promocoes'),
                'ativo'
            )
        }),
        ('📊 Estatísticas', {
            'fields': (
                'total_pedidos_display',
                'valor_total_display', 
                'ultimo_pedido_display'
            ),
            'classes': ('collapse',),
        }),
        ('📝 Observações Internas', {
            'fields': ('observacoes',),
            'classes': ('collapse',),
        }),
        ('🕒 Metadados', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions customizadas
    actions = [
        'ativar_clientes',
        'desativar_clientes',
        'ativar_newsletter',
        'desativar_newsletter'
    ]

    def get_queryset(self, request):
        """Otimiza as consultas incluindo dados relacionados"""
        qs = super().get_queryset(request)
        return qs.select_related('usuario').prefetch_related('pedidos')

    # Métodos para exibição customizada
    def cidade_estado(self, obj):
        if obj.cidade and obj.estado:
            return f"{obj.cidade}/{obj.estado}"
        return "-"
    cidade_estado.short_description = "Cidade/Estado"
    cidade_estado.admin_order_field = 'cidade'

    def total_pedidos_display(self, obj):
        total = obj.total_pedidos
        if total > 0:
            url = reverse('admin:pedidos_pedido_changelist') + f'?cliente__id__exact={obj.id}'
            return format_html(
                '<a href="{}" style="color: #0066cc; font-weight: bold;">{} pedidos</a>',
                url, total
            )
        return format_html('<span style="color: #999;">0 pedidos</span>')
    total_pedidos_display.short_description = "Total de Pedidos"

    def valor_total_display(self, obj):
        valor = obj.valor_total_compras
        if valor > 0:
            return format_html(
                '<span style="color: #006600; font-weight: bold;">R$ {:.2f}</span>',
                valor
            )
        return format_html('<span style="color: #999;">R$ 0,00</span>')
    valor_total_display.short_description = "Total Compras"

    def ultimo_pedido_display(self, obj):
        ultimo = obj.ultimo_pedido
        if ultimo:
            return format_html(
                '<span style="color: #0066cc;">{}</span>',
                ultimo.strftime('%d/%m/%Y')
            )
        return format_html('<span style="color: #999;">Nunca</span>')
    ultimo_pedido_display.short_description = "Último Pedido"

    def endereco_completo_display(self, obj):
        endereco = obj.endereco_completo
        if endereco:
            return format_html(
                '<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; max-width: 400px;">{}</div>',
                endereco
            )
        return "-"
    endereco_completo_display.short_description = "Endereço Completo"

    # Actions customizadas
    def ativar_clientes(self, request, queryset):
        updated = queryset.update(ativo=True)
        self.message_user(request, f'{updated} clientes foram ativados.')
    ativar_clientes.short_description = "✅ Ativar clientes selecionados"

    def desativar_clientes(self, request, queryset):
        updated = queryset.update(ativo=False)
        self.message_user(request, f'{updated} clientes foram desativados.')
    desativar_clientes.short_description = "❌ Desativar clientes selecionados"

    def ativar_newsletter(self, request, queryset):
        updated = queryset.update(aceita_newsletter=True)
        self.message_user(request, f'{updated} clientes ativaram newsletter.')
    ativar_newsletter.short_description = "📧 Ativar newsletter"

    def desativar_newsletter(self, request, queryset):
        updated = queryset.update(aceita_newsletter=False)
        self.message_user(request, f'{updated} clientes desativaram newsletter.')
    desativar_newsletter.short_description = "📧 Desativar newsletter"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
