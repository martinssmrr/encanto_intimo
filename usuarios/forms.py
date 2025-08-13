from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import PerfilUsuario


class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        }),
        label='Nome'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        }),
        label='Sobrenome'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu.email@exemplo.com'
        }),
        label='E-mail'
    )
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'foto', 'telefone', 'data_nascimento', 'cpf',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'aceita_newsletter', 'aceita_promocoes'
        ]
        
        widgets = {
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
                'id': 'telefone'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'id': 'cpf'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'id': 'cep'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apartamento, bloco, etc.'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da cidade'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SP',
                'maxlength': '2',
                'style': 'text-transform: uppercase'
            }),
            'aceita_newsletter': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aceita_promocoes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'foto': 'Foto de Perfil',
            'telefone': 'Telefone',
            'data_nascimento': 'Data de Nascimento',
            'cpf': 'CPF',
            'cep': 'CEP',
            'endereco': 'Endereço',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'aceita_newsletter': 'Quero receber newsletter',
            'aceita_promocoes': 'Quero receber promoções'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance.user
        
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise ValidationError('Este e-mail já está sendo usado por outro usuário.')
        return email
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            # Remover formatação para validação
            telefone_limpo = re.sub(r'[^\d]', '', telefone)
            
            if len(telefone_limpo) < 10:
                raise ValidationError('Telefone deve ter pelo menos 10 dígitos.')
        
        return telefone
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remover formatação para validação
            cep_limpo = re.sub(r'[^\d]', '', cep)
            
            if len(cep_limpo) != 8:
                raise ValidationError('CEP deve ter 8 dígitos.')
        
        return cep
    
    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado:
            return estado.upper()
        return estado
    
    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        
        if foto:
            # Verificar tamanho do arquivo (máximo 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise ValidationError('A imagem deve ter no máximo 5MB.')
            
            # Verificar tipo do arquivo
            if not foto.content_type.startswith('image/'):
                raise ValidationError('Apenas arquivos de imagem são permitidos.')
        
        return foto
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        
        # Atualizar dados do usuário
        user = perfil.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            perfil.save()
        
        return perfil


class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        }),
        label='Nome'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        }),
        label='Sobrenome'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu.email@exemplo.com'
        }),
        label='E-mail'
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999',
            'id': 'telefone'
        }),
        label='Telefone'
    )
    
    cep = forms.CharField(
        max_length=9,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000',
            'id': 'cep'
        }),
        label='CEP'
    )
    
    endereco = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua, Avenida, etc.'
        }),
        label='Endereço'
    )
    
    numero = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123'
        }),
        label='Número'
    )
    
    complemento = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartamento, bloco, etc. (opcional)'
        }),
        label='Complemento'
    )
    
    bairro = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do bairro'
        }),
        label='Bairro'
    )
    
    cidade = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da cidade'
        }),
        label='Cidade'
    )
    
    estado = forms.CharField(
        max_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'SP',
            'maxlength': '2',
            'style': 'text-transform: uppercase'
        }),
        label='Estado'
    )
    
    aceita_termos = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Li e aceito os termos de uso e política de privacidade'
    )
    
    aceita_newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Quero receber ofertas e novidades por e-mail',
        initial=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customizar campos padrão
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário único'
        })
        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].help_text = 'Letras, números e @/./+/-/_ apenas.'
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres com pelo menos 1 número'
        })
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = 'Mínimo 8 caracteres, incluindo pelo menos um número.'
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite a senha novamente'
        })
        self.fields['password2'].label = 'Confirmar senha'
        self.fields['password2'].help_text = None
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já está cadastrado.')
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            # Verificar se tem pelo menos 8 caracteres
            if len(password1) < 8:
                raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
            
            # Verificar se tem pelo menos um número
            if not re.search(r'\d', password1):
                raise ValidationError('A senha deve conter pelo menos um número.')
        
        return password1
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        # Remover formatação para validação
        telefone_limpo = re.sub(r'[^\d]', '', telefone)
        
        if len(telefone_limpo) < 10:
            raise ValidationError('Telefone deve ter pelo menos 10 dígitos.')
        
        return telefone
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        # Remover formatação para validação
        cep_limpo = re.sub(r'[^\d]', '', cep)
        
        if len(cep_limpo) != 8:
            raise ValidationError('CEP deve ter 8 dígitos.')
        
        return cep
    
    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado:
            return estado.upper()
        return estado
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Criar perfil do usuário
            PerfilUsuario.objects.create(
                user=user,
                telefone=self.cleaned_data['telefone'],
                cep=self.cleaned_data['cep'],
                endereco=self.cleaned_data['endereco'],
                numero=self.cleaned_data['numero'],
                complemento=self.cleaned_data['complemento'],
                bairro=self.cleaned_data['bairro'],
                cidade=self.cleaned_data['cidade'],
                estado=self.cleaned_data['estado'],
                aceita_newsletter=self.cleaned_data['aceita_newsletter'],
                aceita_promocoes=self.cleaned_data['aceita_newsletter']  # Assumindo que são iguais
            )
        
        return user
