from django.contrib import admin
from .models import Categoria, Tag, Produto, ImagemProduto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'ativo', 'ordem']
    list_filter = ['ativo']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ['ordem', 'ativo']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'cor']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}


class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 3


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'fornecedor', 'preco', 'preco_promocional', 'ativo', 'destaque', 'data_cadastro']
    list_filter = ['ativo', 'destaque', 'categoria', 'fornecedor', 'data_cadastro']
    search_fields = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ['ativo', 'destaque', 'preco', 'preco_promocional']
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    filter_horizontal = ['tags']
    inlines = [ImagemProdutoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'descricao', 'descricao_curta')
        }),
        ('Categorização', {
            'fields': ('categoria', 'fornecedor', 'tags')
        }),
        ('Preços', {
            'fields': ('preco', 'preco_promocional')
        }),
        ('Características', {
            'fields': ('tamanhos_disponiveis', 'cores_disponiveis', 'material', 'peso')
        }),
        ('Estoque', {
            'fields': ('estoque_virtual', 'vendas_simuladas')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativo', 'destaque')
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ImagemProduto)
class ImagemProdutoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'alt_text', 'ordem']
    list_filter = ['produto']
    search_fields = ['produto__nome', 'alt_text']
    list_editable = ['ordem']
