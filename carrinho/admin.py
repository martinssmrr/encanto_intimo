from django.contrib import admin
from .models import Carrinho, ItemCarrinho


class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0
    readonly_fields = ['total']


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'session_key', 'total_itens', 'subtotal', 'data_criacao']
    list_filter = ['data_criacao']
    search_fields = ['usuario__username', 'session_key']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    inlines = [ItemCarrinhoInline]


@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['carrinho', 'produto', 'quantidade', 'tamanho', 'cor', 'total', 'data_adicao']
    list_filter = ['data_adicao']
    search_fields = ['produto__nome', 'carrinho__usuario__username']
    readonly_fields = ['data_adicao']
