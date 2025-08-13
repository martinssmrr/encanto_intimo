# 📋 Guia de Configurações por Ambiente - Encanto Íntimo

Este documento explica como usar as configurações separadas por ambiente no projeto Django **Encanto Íntimo**.

## 🏗️ Estrutura das Configurações

```
encanto_intimo/
├── settings/
│   ├── __init__.py      # Documentação do pacote
│   ├── base.py          # Configurações comuns
│   ├── dev.py           # Configurações de desenvolvimento
│   └── prod.py          # Configurações de produção
├── wsgi.py              # Configurado para produção
└── manage.py            # Configurado para desenvolvimento
```

## 🔧 Como Usar

### Desenvolvimento Local

1. **Configuração Padrão:**
   ```bash
   # O manage.py já está configurado para desenvolvimento
   python manage.py runserver
   ```

2. **Configuração Explícita:**
   ```bash
   # Windows
   set DJANGO_SETTINGS_MODULE=encanto_intimo.settings.dev
   python manage.py runserver
   
   # Linux/Mac
   export DJANGO_SETTINGS_MODULE=encanto_intimo.settings.dev
   python manage.py runserver
   ```

### Produção

1. **Configurar Variável de Ambiente:**
   ```bash
   # Windows
   set DJANGO_SETTINGS_MODULE=encanto_intimo.settings.prod
   
   # Linux/Mac
   export DJANGO_SETTINGS_MODULE=encanto_intimo.settings.prod
   ```

2. **Executar Comandos:**
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   gunicorn encanto_intimo.wsgi:application
   ```

## 📝 Variáveis de Ambiente Necessárias

### Para Desenvolvimento (.env)
```env
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Para Produção (.env.prod)
```env
SECRET_KEY=sua-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=encantointimo.com,www.encantointimo.com

# Database
DB_NAME=encanto_intimo_prod
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app

# Pagamentos
STRIPE_LIVE_PUBLISHABLE_KEY=pk_live_...
STRIPE_LIVE_SECRET_KEY=sk_live_...
```

## 🚀 Deploy em Produção

### 1. Configurar Servidor

```bash
# Instalar dependências
pip install -r requirements.txt
pip install psycopg2-binary gunicorn

# Configurar variáveis de ambiente
export DJANGO_SETTINGS_MODULE=encanto_intimo.settings.prod
```

### 2. Executar Migrações

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 3. Iniciar Aplicação

```bash
# Com Gunicorn
gunicorn --bind 0.0.0.0:8000 encanto_intimo.wsgi:application

# Com systemd (recomendado)
sudo systemctl start encanto-intimo
sudo systemctl enable encanto-intimo
```

## 🔒 Configurações de Segurança

### Desenvolvimento
- ✅ DEBUG=True
- ✅ HTTP permitido
- ✅ SQLite
- ✅ Console email backend
- ✅ Logs detalhados

### Produção
- ✅ DEBUG=False
- ✅ HTTPS obrigatório
- ✅ PostgreSQL
- ✅ SMTP email
- ✅ Cache Redis
- ✅ Logs otimizados
- ✅ Proteções de segurança:
  - SSL Redirect
  - HSTS Headers
  - Secure Cookies
  - XSS Protection
  - Content Type Protection

## 📊 Logs e Monitoramento

### Desenvolvimento
- Logs no console
- Arquivo: `logs/dev.log`

### Produção
- Logs rotativos: `/var/log/encanto_intimo/`
- Email para admins em caso de erro
- Integração com Sentry (opcional)

## 🗄️ Banco de Dados

### Desenvolvimento
```python
# SQLite (automático)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### Produção
```python
# PostgreSQL (via variáveis de ambiente)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        # ... outras configurações
    }
}
```

## 🎯 Comandos Úteis

```bash
# Verificar configuração atual
python manage.py diffsettings

# Testar configurações
python manage.py check --deploy

# Verificar variáveis de ambiente
python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)"

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Executar testes
python manage.py test
```

## ⚠️ Importantes

1. **Nunca commite arquivos .env** com valores reais
2. **Sempre use HTTPS em produção**
3. **Configure backup do banco de dados**
4. **Monitore logs regularmente**
5. **Mantenha dependências atualizadas**

## 🆘 Troubleshooting

### Erro: "No module named 'encanto_intimo.settings'"
```bash
# Verifique se está no diretório correto
cd /caminho/para/projeto

# Verifique a variável de ambiente
echo $DJANGO_SETTINGS_MODULE
```

### Erro: "Database connection failed"
```bash
# Verifique as variáveis de ambiente do banco
# Teste a conexão manualmente
psql -h localhost -U usuario -d banco
```

### Erro: "Static files not found"
```bash
# Execute collectstatic
python manage.py collectstatic --noinput

# Verifique as configurações de STATIC_ROOT
```

## 📚 Referências

- [Django Settings Documentation](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)

---

**Desenvolvido para o projeto Encanto Íntimo** 💖
