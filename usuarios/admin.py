from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'


class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)


# Reregistrar User com o inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefone', 'cidade', 'estado', 'aceita_newsletter', 'data_cadastro']
    list_filter = ['estado', 'aceita_newsletter', 'aceita_promocoes', 'data_cadastro']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'telefone']
    readonly_fields = ['data_cadastro', 'data_atualizacao']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Dados Pessoais', {
            'fields': ('telefone', 'data_nascimento', 'cpf')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Preferências', {
            'fields': ('aceita_newsletter', 'aceita_promocoes')
        }),
        ('Datas', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
