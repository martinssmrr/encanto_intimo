from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    
    # Foto de perfil
    foto = models.ImageField(
        upload_to='perfis/', 
        blank=True, 
        null=True, 
        verbose_name="Foto de Perfil",
        help_text="Tamanho recomendado: 400x400px"
    )
    
    # Endereço padrão
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    endereco = models.CharField(max_length=200, blank=True, verbose_name="Endereço")
    numero = models.CharField(max_length=10, blank=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    
    # Preferências
    aceita_newsletter = models.BooleanField(default=True, verbose_name="Aceita Newsletter")
    aceita_promocoes = models.BooleanField(default=True, verbose_name="Aceita Promoções")
    
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username}'

    @property
    def endereco_completo(self):
        if not self.endereco:
            return ''
        
        endereco_parts = [self.endereco]
        if self.numero:
            endereco_parts.append(self.numero)
        if self.complemento:
            endereco_parts.append(f'- {self.complemento}')
        if self.bairro:
            endereco_parts.append(f'{self.bairro}')
        if self.cidade and self.estado:
            endereco_parts.append(f'{self.cidade}/{self.estado}')
        if self.cep:
            endereco_parts.append(f'CEP: {self.cep}')
            
        return ', '.join(endereco_parts)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()
