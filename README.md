# 🌸 Encanto Íntimo - Loja de Dropshipping

Uma plataforma completa de e-commerce para produtos íntimos e sensuais, desenvolvida em Django com foco na experiência do usuário, discrição e eficiência operacional.

## 🚀 Funcionalidades Principais

### 🛍️ Gestão de Produtos
- **Cadastro Completo**: Nome, descrição, preço, estoque virtual e fornecedor
- **Upload de Múltiplas Imagens**: Galeria de fotos para cada produto
- **Categorização Avançada**: Organização por categorias e tags
- **Variações**: Diferentes tamanhos e cores por produto
- **SEO Otimizado**: Meta tags personalizadas para cada produto

### 🔗 Integração com Fornecedores
- **Cadastro de Fornecedores**: Dados completos e informações de contato
- **Relacionamento com Produtos**: Vinculação automática produto-fornecedor
- **Preparação para APIs**: Estrutura pronta para integrações futuras

### 📑 Sistema de Pedidos
- **Gerenciamento Completo**: Visualização de todos os status dos pedidos
- **Histórico de Status**: Rastreamento detalhado de mudanças
- **Dados do Cliente**: Armazenamento seguro de informações de entrega
- **Notificações Automáticas**: E-mails para cliente e administradores

### 🔐 Autenticação e Perfil
- **Sistema Completo**: Login, logout, registro e recuperação de senha
- **Perfil Detalhado**: Dados pessoais e endereço de entrega
- **Histórico de Pedidos**: Dashboard pessoal para cada cliente
- **Preferências**: Newsletter e promoções personalizadas

### 🛒 Carrinho Inteligente
- **Persistência**: Mantém itens para usuários logados e visitantes
- **Variações**: Seleção de tamanho e cor
- **Cálculos Automáticos**: Subtotal, frete e total em tempo real
- **Checkout Otimizado**: Processo simplificado de finalização

### 💳 Pagamentos Seguros
- **Múltiplos Gateways**: Stripe e Mercado Pago integrados
- **Webhooks**: Processamento automático de confirmações
- **Logs Detalhados**: Rastreamento completo de transações
- **Segurança**: Armazenamento seguro de dados de pagamento

### 🛠️ Painel Administrativo
- **Django Admin**: Interface técnica completa
- **Painel Customizado**: Interface amigável para gestores
- **Relatórios**: Análises de vendas e performance
- **Gestão de Estoque**: Controle de produtos e fornecedores

### 📩 Sistema de Notificações
- **E-mails Transacionais**: Confirmações e atualizações automáticas
- **Templates Personalizados**: Design consistente nas comunicações
- **Newsletter**: Sistema de marketing por e-mail

### 🎨 Frontend Responsivo
- **Tailwind CSS**: Design moderno e consistente
- **Mobile-First**: Otimizado para dispositivos móveis
- **UX Otimizada**: Foco na conversão e experiência do usuário
- **Performance**: Carregamento rápido e eficiente

## 🏗️ Arquitetura Técnica

### **Estrutura de Apps Django**

```
encanto_intimo/
├── produtos/          # Gestão de produtos, categorias e imagens
├── fornecedores/      # Cadastro e gestão de fornecedores
├── usuarios/          # Autenticação e perfis de usuário
├── carrinho/          # Sistema de carrinho de compras
├── pedidos/           # Processamento e gestão de pedidos
├── pagamentos/        # Integração com gateways de pagamento
├── adminpanel/        # Painel administrativo customizado
├── templates/         # Templates HTML organizados
├── static/           # Arquivos CSS, JS e imagens
└── media/            # Upload de arquivos dos usuários
```

### **Tecnologias Utilizadas**

- **Backend**: Django 4.2+ com Django ORM
- **Frontend**: Templates Django + Tailwind CSS
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Pagamentos**: Stripe + Mercado Pago
- **E-mail**: SMTP configurável
- **Storage**: Local (desenvolvimento) / AWS S3 (produção)
- **UI**: Font Awesome + Google Fonts

## 🚀 Instalação e Configuração

### **Pré-requisitos**
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### **1. Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/encanto-intimo.git
cd encanto-intimo
```

### **2. Crie um Ambiente Virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### **3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

### **4. Configure as Variáveis de Ambiente**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
```

### **5. Execute as Migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Crie um Superusuário**
```bash
python manage.py createsuperuser
```

### **7. Execute o Servidor**
```bash
python manage.py runserver
```

O projeto estará disponível em: `http://127.0.0.1:8000`

## ⚙️ Configuração

### **Variáveis de Ambiente (.env)**

```env
# Configurações Básicas
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# E-mail
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu-token-aqui
MERCADOPAGO_PUBLIC_KEY=sua-chave-publica-aqui
```

### **Configuração de E-mail**

Para usar o Gmail:
1. Ative a autenticação de 2 fatores
2. Gere uma senha de app
3. Use a senha de app no .env

### **Configuração de Pagamentos**

**Stripe:**
1. Crie uma conta em stripe.com
2. Obtenha as chaves de API do dashboard
3. Configure as chaves no .env

**Mercado Pago:**
1. Crie uma conta de desenvolvedor
2. Obtenha as credenciais de teste/produção
3. Configure no .env

## 📊 Funcionalidades Implementadas

### ✅ **Concluído**
- [x] Estrutura completa de modelos Django
- [x] Sistema de autenticação e perfis
- [x] Gestão de produtos e categorias
- [x] Carrinho de compras funcional
- [x] Sistema de pedidos
- [x] Integração com fornecedores
- [x] Templates responsivos base
- [x] Django Admin configurado
- [x] Sistema de pagamentos estruturado

### 🚧 **Em Desenvolvimento**
- [ ] Templates completos de todas as páginas
- [ ] Integração completa com Stripe
- [ ] Integração completa com Mercado Pago
- [ ] Sistema de e-mails transacionais
- [ ] Painel administrativo customizado
- [ ] Sistema de relatórios
- [ ] Otimizações de performance

### 📋 **Próximos Passos**
- [ ] Implementação de cupons de desconto
- [ ] Sistema de avaliações de produtos
- [ ] Chat de atendimento
- [ ] Integração com redes sociais
- [ ] API REST para mobile
- [ ] Testes automatizados

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

- **E-mail**: contato@encantointimo.com
- **WhatsApp**: (11) 99999-9999
- **Horário**: Segunda à Sexta, 9h às 18h

---

**Desenvolvido com ❤️ para o sucesso do seu negócio!**
