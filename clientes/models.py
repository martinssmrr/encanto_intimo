from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    """
    Modelo para gerenciar informações de clientes
    """
    # Informações pessoais básicas
    nome_completo = models.CharField(max_length=200, verbose_name='Nome Completo')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    
    # Relacionamento com User (opcional)
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='cliente_profile',
        verbose_name='Usuário'
    )
    
    # Endereço básico
    endereco = models.CharField(max_length=255, verbose_name='Endereço')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    
    # Status e datas
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-data_cadastro']
        app_label = 'clientes'

    def __str__(self):
        return self.nome_completo
