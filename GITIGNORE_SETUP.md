# 📁 CONFIGURAÇÃO DO .GITIGNORE - ENCANTO ÍNTIMO

## ✅ Arquivo .gitignore criado com sucesso!

### 🎯 **O que está sendo ignorado:**

#### **🐍 Python e Django:**
- `__pycache__/` e arquivos `.pyc`
- `db.sqlite3` (banco de desenvolvimento)
- `staticfiles/` e `media/` (gerados automaticamente)
- Logs do Django (`*.log`)
- Cache do Django

#### **🔐 Arquivos sensíveis:**
- `.env` e variações (`.env.prod`, `.env.dev`, etc.)
- Chaves de API e credenciais
- `local_settings.py`
- Certificados SSL (`*.crt`, `*.key`, `*.pem`)

#### **💾 Bancos de dados:**
- `*.sqlite3` (SQLite)
- `*.sql`, `*.dump` (backups de BD)
- Arquivos PostgreSQL e MySQL

#### **📊 Logs e cache:**
- `logs/` (exceto `.gitkeep`)
- `*.log` (todos os logs)
- Cache do Redis (`dump.rdb`)
- Cache do Django

#### **🛠️ Ferramentas de desenvolvimento:**
- `.vscode/` (Visual Studio Code)
- `.idea/` (PyCharm)
- `node_modules/` (se usar Node.js)
- Arquivos temporários dos editores

#### **💻 Sistema operacional:**
- `.DS_Store` (macOS)
- `Thumbs.db` (Windows)
- Arquivos temporários do Linux

#### **📦 Backups e temporários:**
- `backups/` (exceto `.gitkeep`)
- `*.bak`, `*.tmp`, `*.backup`
- Arquivos de teste

## 🔄 **Comandos importantes para Git:**

### **Se já tinha arquivos commitados que agora devem ser ignorados:**
```bash
# Remover arquivo do rastreamento (mas manter no disco)
git rm --cached arquivo.txt

# Remover diretório do rastreamento
git rm -r --cached diretorio/

# Exemplos específicos:
git rm --cached .env
git rm --cached db.sqlite3
git rm -r --cached __pycache__/
git rm -r --cached media/
```

### **Aplicar .gitignore e fazer commit:**
```bash
# Adicionar .gitignore
git add .gitignore

# Commit do gitignore
git commit -m "Add comprehensive .gitignore for Django project"

# Se removeu arquivos do rastreamento:
git add .
git commit -m "Remove sensitive files from tracking"
```

### **Verificar status depois do .gitignore:**
```bash
# Ver arquivos não rastreados
git status

# Ver arquivos ignorados
git status --ignored

# Ver quais arquivos estão sendo rastreados
git ls-files
```

## 📋 **Arquivos que DEVEM estar no Git:**

### ✅ **Versionados (incluídos):**
- Código fonte (`.py`, `.html`, `.css`, `.js`)
- Templates e arquivos estáticos do projeto
- `requirements.txt` e `requirements-dev.txt`
- `manage.py` e arquivos de configuração do Django
- `.env.example` (template de variáveis)
- `README.md` e documentação
- Arquivos de configuração (`settings/`, `urls.py`)
- `.gitignore` e `.gitkeep`

### ❌ **Ignorados (não incluídos):**
- `.env` (variáveis reais)
- `db.sqlite3` (banco de desenvolvimento)
- `media/` (uploads de usuários)
- `staticfiles/` (arquivos coletados)
- `logs/` (exceto `.gitkeep`)
- `__pycache__/` (cache Python)
- `.venv/` (ambiente virtual)

## 🔧 **Configuração recomendada para novo clone:**

```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/encanto-intimo.git
cd encanto-intimo

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Copiar e configurar variáveis de ambiente
cp .env.example .env
# Editar .env com valores reais

# 6. Aplicar migrações
python manage.py migrate

# 7. Criar superusuário
python manage.py createsuperuser

# 8. Executar servidor
python manage.py runserver
```

## 🚨 **Importante - Segurança:**

### **NUNCA commitar:**
- ❌ Arquivos `.env` com dados reais
- ❌ Chaves de API (Google, Stripe, MercadoPago)
- ❌ Senhas de banco de dados
- ❌ Certificados SSL privados
- ❌ Tokens de autenticação
- ❌ Dados pessoais de usuários

### **SEMPRE manter:**
- ✅ `.env.example` com variáveis documentadas
- ✅ `requirements.txt` atualizado
- ✅ Documentação de configuração
- ✅ Scripts de setup e deploy

## 📁 **Estrutura de diretórios mantida:**

```
encanto_intimo/
├── .gitignore          ✅ (criado)
├── .env.example        ✅ (template)
├── logs/
│   └── .gitkeep       ✅ (mantém diretório)
├── backups/
│   └── .gitkeep       ✅ (mantém diretório)
└── media/             ❌ (ignorado, mas criado automaticamente)
```

---

**🎉 Seu projeto agora está protegido com um .gitignore completo!**

Lembre-se de sempre revisar o que está sendo commitado com `git status` antes de fazer `git commit`.
