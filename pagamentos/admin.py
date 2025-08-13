from django.contrib import admin
from .models import Pagamento, LogPagamento


class LogPagamentoInline(admin.TabularInline):
    model = LogPagamento
    extra = 0
    readonly_fields = ['data_evento']


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['id_pagamento_short', 'pedido', 'usuario', 'gateway', 'status', 'valor', 'data_criacao']
    list_filter = ['gateway', 'status', 'data_criacao']
    search_fields = ['id_pagamento', 'transaction_id', 'usuario__username', 'pedido__numero_pedido']
    readonly_fields = ['id_pagamento', 'data_criacao', 'data_processamento', 'data_confirmacao']
    inlines = [LogPagamentoInline]
    
    def id_pagamento_short(self, obj):
        return str(obj.id_pagamento)[:8] + '...'
    id_pagamento_short.short_description = 'ID do Pagamento'
    
    fieldsets = (
        ('Identificação', {
            'fields': ('id_pagamento', 'pedido', 'usuario')
        }),
        ('Detalhes do Pagamento', {
            'fields': ('gateway', 'status', 'valor')
        }),
        ('IDs Externos', {
            'fields': ('transaction_id', 'payment_intent_id', 'preference_id')
        }),
        ('Dados do Cartão', {
            'fields': ('cartao_ultimos_digitos', 'cartao_bandeira'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_processamento', 'data_confirmacao')
        }),
        ('Metadados', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )


@admin.register(LogPagamento)
class LogPagamentoAdmin(admin.ModelAdmin):
    list_display = ['pagamento', 'evento', 'data_evento']
    list_filter = ['evento', 'data_evento']
    search_fields = ['pagamento__id_pagamento', 'evento']
    readonly_fields = ['data_evento']
