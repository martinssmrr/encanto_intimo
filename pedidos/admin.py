from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Pedido, ItemPedido, StatusPedido


class ItemPedidoInline(admin.TabularInline):
    """Inline para edição de itens do pedido"""
    model = ItemPedido
    extra = 0
    readonly_fields = ['total_item']
    fields = [
        'produto', 'nome_produto', 'quantidade', 'preco_unitario', 'total_item',
        'tamanho', 'cor', 'fornecedor_nome'
    ]
    
    def get_readonly_fields(self, request, obj=None):
        # Se o pedido já foi confirmado, tornar campos read-only
        if obj and obj.status in ['confirmado', 'processando', 'enviado', 'entregue']:
            return self.readonly_fields + ['produto', 'quantidade', 'preco_unitario']
        return self.readonly_fields


class StatusPedidoInline(admin.TabularInline):
    """Inline para histórico de status"""
    model = StatusPedido
    extra = 1
    readonly_fields = ['data_alteracao']
    fields = ['status', 'observacao', 'usuario_alteracao', 'data_alteracao']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se é edição, não adicionar automaticamente usuário
            return self.readonly_fields + ['usuario_alteracao']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.usuario_alteracao:
            obj.usuario_alteracao = request.user
        super().save_model(request, obj, form, change)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Admin customizado para Pedidos com funcionalidades avançadas
    """
    
    # Configurações de listagem
    list_display = [
        'numero_pedido_display',
        'cliente_info',
        'usuario',
        'status_display',
        'total_display',
        'pagamento_status',
        'forma_pagamento',
        'data_pedido',
        'data_atualizacao'
    ]
    
    list_filter = [
        'status',
        'pagamento_confirmado',
        'forma_pagamento',
        'data_pedido',
        'data_atualizacao',
        'data_envio',
        # ('cliente', admin.RelatedOnlyFieldListFilter),  # Comentado temporariamente
    ]
    
    search_fields = [
        'numero_pedido',
        'usuario__username',
        'usuario__email',
        'nome_cliente',
        'email_cliente',
        # 'cliente__nome_completo',  # Comentado temporariamente
        # 'cliente__email',  # Comentado temporariamente
        'transaction_id'
    ]
    
    readonly_fields = [
        'numero_pedido',
        'data_pedido',
        'data_atualizacao',
        'total_itens_display',
        'endereco_completo_display'
    ]
    
    # list_editable = ['status']  # Comentado temporariamente
    
    ordering = ['-data_pedido']
    
    list_per_page = 25
    
    # Inlines
    inlines = [ItemPedidoInline, StatusPedidoInline]
    
    # Actions
    actions = [
        'marcar_como_confirmado',
        'marcar_como_processando',
        'marcar_como_enviado',
        'confirmar_pagamento'
    ]
    
    fieldsets = (
        ('🏷️ Identificação', {
            'fields': ('numero_pedido', 'usuario', 'cliente', 'status'),
            'classes': ('wide',),
        }),
        ('👤 Dados do Cliente', {
            'fields': (
                ('nome_cliente', 'email_cliente'),
                'telefone_cliente'
            ),
            'classes': ('wide',),
        }),
        ('🏠 Endereço de Entrega', {
            'fields': (
                ('cep', 'estado'),
                ('endereco', 'numero'),
                ('complemento', 'bairro'),
                'cidade',
                'endereco_completo_display'
            ),
            'classes': ('wide', 'collapse'),
        }),
        ('💰 Valores', {
            'fields': (
                ('subtotal', 'valor_frete'),
                ('desconto', 'total'),
                'total_itens_display'
            ),
            'classes': ('wide',),
        }),
        ('💳 Pagamento', {
            'fields': (
                ('forma_pagamento', 'pagamento_confirmado'),
                'transaction_id'
            ),
            'classes': ('wide',),
        }),
        ('📅 Datas', {
            'fields': (
                ('data_pedido', 'data_atualizacao'),
                ('data_envio', 'data_entrega')
            ),
            'classes': ('wide',),
        }),
        ('📋 Observações e Rastreamento', {
            'fields': ('observacoes', 'codigo_rastreamento'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        """Otimiza consultas"""
        qs = super().get_queryset(request)
        return qs.select_related('usuario', 'cliente').prefetch_related('itens')

    # Métodos de exibição customizada
    def numero_pedido_display(self, obj):
        pedido_short = str(obj.numero_pedido)[:8]
        return format_html(
            '<span style="font-family: monospace; font-weight: bold; color: #0066cc;">#{}</span>',
            pedido_short
        )
    numero_pedido_display.short_description = 'Nº Pedido'
    numero_pedido_display.admin_order_field = 'numero_pedido'

    def cliente_info(self, obj):
        # Função simplificada - app clientes não registrada
        return format_html(
            '<strong>{}</strong><br>'
            '<small style="color: #666;">{}</small>',
            obj.nome_cliente or (obj.usuario.get_full_name() or obj.usuario.username),
            obj.email_cliente or obj.usuario.email
        )
    cliente_info.short_description = 'Cliente'

    def status_display(self, obj):
        status_colors = {
            'pendente': '#ffc107',      # Amarelo
            'confirmado': '#17a2b8',    # Azul claro
            'processando': '#007bff',   # Azul
            'enviado': '#fd7e14',       # Laranja
            'entregue': '#28a745',      # Verde
            'cancelado': '#dc3545',     # Vermelho
            'devolvido': '#6f42c1',     # Roxo
        }
        
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'

    def total_display(self, obj):
        return format_html(
            '<span style="color: #006600; font-weight: bold; font-size: 14px;">R$ {:.2f}</span>',
            obj.total
        )
    total_display.short_description = 'Total'
    total_display.admin_order_field = 'total'

    def pagamento_status(self, obj):
        if obj.pagamento_confirmado:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✅ Confirmado</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">❌ Pendente</span>'
            )
    pagamento_status.short_description = 'Pagamento'
    pagamento_status.boolean = True

    def total_itens_display(self, obj):
        total = obj.total_itens()
        return format_html(
            '<span style="color: #0066cc; font-weight: bold;">{} itens</span>',
            total
        )
    total_itens_display.short_description = 'Total de Itens'

    def endereco_completo_display(self, obj):
        endereco = obj.endereco_completo
        return format_html(
            '<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; max-width: 400px;">{}</div>',
            endereco
        )
    endereco_completo_display.short_description = 'Endereço Completo'

    # Actions customizadas
    def marcar_como_confirmado(self, request, queryset):
        updated = queryset.filter(status='pendente').update(status='confirmado')
        self.message_user(request, f'{updated} pedidos confirmados.')
    marcar_como_confirmado.short_description = "✅ Confirmar pedidos selecionados"

    def marcar_como_processando(self, request, queryset):
        updated = queryset.filter(status__in=['pendente', 'confirmado']).update(status='processando')
        self.message_user(request, f'{updated} pedidos marcados como processando.')
    marcar_como_processando.short_description = "🔄 Marcar como processando"

    def marcar_como_enviado(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for pedido in queryset.filter(status__in=['confirmado', 'processando']):
            pedido.status = 'enviado'
            if not pedido.data_envio:
                pedido.data_envio = timezone.now()
            pedido.save()
            updated += 1
        self.message_user(request, f'{updated} pedidos marcados como enviados.')
    marcar_como_enviado.short_description = "📦 Marcar como enviado"

    def confirmar_pagamento(self, request, queryset):
        updated = queryset.update(pagamento_confirmado=True)
        self.message_user(request, f'Pagamento confirmado para {updated} pedidos.')
    confirmar_pagamento.short_description = "💳 Confirmar pagamento"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'nome_produto', 'quantidade', 'preco_unitario', 'total_item']
    list_filter = ['pedido__status', 'fornecedor_nome']
    search_fields = ['nome_produto', 'pedido__numero_pedido']


@admin.register(StatusPedido)
class StatusPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'status', 'data_alteracao', 'usuario_alteracao']
    list_filter = ['status', 'data_alteracao']
    search_fields = ['pedido__numero_pedido']
    readonly_fields = ['data_alteracao']
