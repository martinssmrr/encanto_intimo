# 🔐 CONFIGURAÇÃO DO LOGIN COM GOOGLE - GUIA COMPLETO

Este guia explica como configurar o login com Google no projeto Encanto Íntimo usando django-allauth.

## 📋 Pré-requisitos

1. ✅ **django-allauth instalado** - Já incluído no requirements.txt
2. ✅ **Configurações do Django** - Já configuradas no settings/base.py
3. ⚠️ **Credenciais do Google Cloud** - Precisa ser configurado

## 🚀 Como obter as credenciais do Google

### Passo 1: Acessar o Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Faça login com sua conta Google
3. Crie um novo projeto ou selecione um existente

### Passo 2: Habilitar a API do Google+

1. No menu lateral, vá em **"APIs e Serviços"** → **"Biblioteca"**
2. Procure por **"Google+ API"** ou **"People API"**
3. Clique em **"Ativar"**

### Passo 3: Criar credenciais OAuth 2.0

1. Vá em **"APIs e Serviços"** → **"Credenciais"**
2. Clique em **"+ CRIAR CREDENCIAIS"** → **"ID do cliente OAuth"**
3. Escolha **"Aplicativo da Web"**
4. Configure:
   - **Nome**: "Encanto Íntimo - Login Social"
   - **Origens JavaScript autorizadas**:
     - `http://localhost:8000` (desenvolvimento)
     - `https://seudominio.com` (produção)
   - **URIs de redirecionamento autorizados**:
     - `http://localhost:8000/accounts/google/login/callback/` (dev)
     - `https://seudominio.com/accounts/google/login/callback/` (prod)

### Passo 4: Copiar as credenciais

Após criar, você receberá:
- **Client ID**: Algo como `123456789-abc123.apps.googleusercontent.com`
- **Client Secret**: Algo como `GOCSPX-abcd1234efgh5678`

## ⚙️ Configuração no projeto

### 1. Atualizar o arquivo .env

Edite o arquivo `.env` na raiz do projeto:

```env
# Google OAuth 2.0
GOOGLE_CLIENT_ID=seu_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
```

### 2. Instalar dependências

```bash
pip install django-allauth
```

### 3. Executar migrações

```bash
python manage.py migrate
```

### 4. Configurar o Site no Django Admin

1. Execute o servidor: `python manage.py runserver`
2. Acesse: http://localhost:8000/admin/
3. Vá em **Sites** → **Sites**
4. Edite o site existente (ID=1):
   - **Domain name**: `localhost:8000` (dev) ou `seudominio.com` (prod)
   - **Display name**: `Encanto Íntimo`

### 5. Configurar o Google Provider (Opcional - via Admin)

1. No Django Admin, vá em **Social Applications**
2. Clique em **"Adicionar social application"**
3. Configure:
   - **Provider**: Google
   - **Name**: Google Login
   - **Client id**: Seu Client ID do Google
   - **Secret key**: Seu Client Secret do Google
   - **Sites**: Selecione o site criado anteriormente

**Nota**: Esta configuração é opcional pois já está configurada no settings.py via variáveis de ambiente.

## 🧪 Testando a integração

### 1. Acessar a página de login

Acesse: http://localhost:8000/usuarios/login/

Você deve ver:
- ✅ Formulário de login tradicional
- ✅ Botão "Continuar com Google" estilizado
- ✅ Separador visual entre as opções

### 2. Testar o login com Google

1. Clique no botão "Continuar com Google"
2. Será redirecionado para o Google
3. Após autorização, voltará para o site
4. Deve ser redirecionado para `/usuarios/perfil/`

### 3. Verificar criação do perfil

1. Acesse o Django Admin
2. Vá em **Usuarios** → **Perfil usuarios**
3. Verifique se o perfil foi criado automaticamente
4. Os dados do Google (nome, email) devem estar preenchidos

## 🔧 Personalização e configurações avançadas

### Configurações disponíveis no settings.py

```python
# Configurações do Allauth já implementadas:

# Redirecionamentos
LOGIN_REDIRECT_URL = '/usuarios/perfil/'
LOGOUT_REDIRECT_URL = '/'

# Configurações da conta
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# Configurações sociais
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
```

### Adaptadores personalizados

O projeto usa adaptadores personalizados em `usuarios/adapters.py` que:

- ✅ Criam automaticamente o `PerfilUsuario` após login social
- ✅ Preenchem dados do perfil com informações do Google
- ✅ Conectam contas sociais a usuários existentes (mesmo email)
- ✅ Redirecionam para a página de perfil após login

## 🚨 Troubleshooting

### Erro: "redirect_uri_mismatch"

**Problema**: URI de redirecionamento não autorizada

**Solução**:
1. Verifique se a URL no Google Cloud Console está correta
2. Para desenvolvimento: `http://localhost:8000/accounts/google/login/callback/`
3. Para produção: `https://seudominio.com/accounts/google/login/callback/`
4. **Importante**: Inclua a barra `/` no final

### Erro: "invalid_client"

**Problema**: Client ID ou Secret incorretos

**Solução**:
1. Verifique se as variáveis no `.env` estão corretas
2. Verifique se não há espaços em branco nas variáveis
3. Copie novamente as credenciais do Google Cloud Console

### Erro: "Site matching query does not exist"

**Problema**: Site não configurado no Django

**Solução**:
1. Execute: `python manage.py migrate`
2. Configure o site no Django Admin conforme instruções acima
3. Certifique-se que `SITE_ID = 1` no settings.py

### Botão do Google não aparece

**Problema**: Template não carrega os providers

**Solução**:
1. Verifique se `{% load socialaccount %}` está no topo do template
2. Verifique se as migrações foram executadas
3. Verifique se o Google provider está ativo no admin

## 📚 URLs importantes do projeto

- **Login**: `/usuarios/login/`
- **Logout**: `/accounts/logout/`
- **Perfil**: `/usuarios/perfil/`
- **Callback Google**: `/accounts/google/login/callback/`
- **Admin**: `/admin/`

## 🔒 Segurança

### Configurações de segurança implementadas:

- ✅ **HTTPS obrigatório em produção**
- ✅ **Verificação de email opcional**
- ✅ **Limite de tentativas de login**
- ✅ **Conexão automática de contas com mesmo email**
- ✅ **Redirecionamento seguro após login**

### Dados coletados do Google:

- ✅ **Nome completo**
- ✅ **Email**
- ✅ **Foto do perfil** (se disponível)
- ❌ **Não coletamos dados sensíveis**

## 🚀 Deploy em produção

### Configurações adicionais para produção:

1. **Atualizar URLs no Google Cloud Console**:
   - Origem: `https://seudominio.com`
   - Callback: `https://seudominio.com/accounts/google/login/callback/`

2. **Configurar HTTPS**:
   ```python
   # No settings/prod.py
   SECURE_SSL_REDIRECT = True
   ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
   ```

3. **Atualizar Site no admin**:
   - Domain: `seudominio.com`
   - Display name: `Encanto Íntimo`

4. **Variáveis de ambiente**:
   ```env
   GOOGLE_CLIENT_ID=seu_client_id_de_producao
   GOOGLE_CLIENT_SECRET=seu_client_secret_de_producao
   ```

---

## ✅ Checklist de implementação

- [ ] ✅ **django-allauth instalado e configurado**
- [ ] ✅ **Configurações no settings.py adicionadas**
- [ ] ✅ **URLs do allauth incluídas**
- [ ] ✅ **Template de login atualizado**
- [ ] ✅ **Adaptadores personalizados criados**
- [ ] ⚠️ **Credenciais do Google configuradas no .env**
- [ ] ⚠️ **Projeto criado no Google Cloud Console**
- [ ] ⚠️ **URIs de redirecionamento configuradas**
- [ ] ⚠️ **Migrações executadas**
- [ ] ⚠️ **Site configurado no Django Admin**
- [ ] ⚠️ **Teste de login realizado**

**Agora seu projeto está pronto para usar login com Google! 🎉**
