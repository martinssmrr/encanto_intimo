from django.contrib import admin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'ativo', 'produtos_count', 'data_cadastro']
    list_filter = ['ativo', 'data_cadastro']
    search_fields = ['nome', 'email']
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'telefone', 'ativo')
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Integração', {
            'fields': ('catalogo_url', 'api_endpoint')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
