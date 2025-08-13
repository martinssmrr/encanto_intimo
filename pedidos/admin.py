from django.contrib import admin
from .models import Pedido, ItemPedido, StatusPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['total_item']


class StatusPedidoInline(admin.TabularInline):
    model = StatusPedido
    extra = 1
    readonly_fields = ['data_alteracao']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido_short', 'usuario', 'status', 'total', 'pagamento_confirmado', 'data_pedido']
    list_filter = ['status', 'pagamento_confirmado', 'forma_pagamento', 'data_pedido']
    search_fields = ['numero_pedido', 'usuario__username', 'usuario__email', 'nome_cliente', 'email_cliente']
    readonly_fields = ['numero_pedido', 'data_pedido', 'data_atualizacao']
    list_editable = ['status']
    inlines = [ItemPedidoInline, StatusPedidoInline]
    
    def numero_pedido_short(self, obj):
        return str(obj.numero_pedido)[:8] + '...'
    numero_pedido_short.short_description = 'Número do Pedido'
    
    fieldsets = (
        ('Identificação', {
            'fields': ('numero_pedido', 'usuario', 'status')
        }),
        ('Dados do Cliente', {
            'fields': ('nome_cliente', 'email_cliente', 'telefone_cliente')
        }),
        ('Endereço de Entrega', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Valores', {
            'fields': ('subtotal', 'valor_frete', 'desconto', 'total')
        }),
        ('Pagamento', {
            'fields': ('forma_pagamento', 'pagamento_confirmado', 'transaction_id')
        }),
        ('Datas', {
            'fields': ('data_pedido', 'data_atualizacao', 'data_envio', 'data_entrega')
        }),
        ('Observações', {
            'fields': ('observacoes', 'codigo_rastreamento'),
            'classes': ('collapse',)
        }),
    )


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
