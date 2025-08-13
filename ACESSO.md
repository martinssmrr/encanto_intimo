# 🔑 Credenciais de Acesso - Encanto Íntimo

## 🖥️ Servidor Local
- **URL**: http://127.0.0.1:8000
- **Status**: ✅ Rodando

## 👤 Admin Django
- **URL**: http://127.0.0.1:8000/admin/
- **Usuário**: admin
- **Senha**: admin123

## 📊 Dados Criados

### 🏷️ Categorias
- Lingerie
- Produtos Sensuais  
- Acessórios
- Perfumaria

### 🏪 Fornecedor
- **Nome**: Fornecedor Exemplo
- **E-mail**: fornecedor@exemplo.com
- **Telefone**: (11) 99999-9999

### 🛍️ Produtos de Exemplo
1. **Conjunto Romantic Lace**
   - Preço: R$ 199,90 → R$ 149,90 (promoção)
   - Categoria: Lingerie
   - Status: Produto em destaque

2. **Baby Doll Sensual**
   - Preço: R$ 129,90
   - Categoria: Lingerie

3. **Camisola Comfort Night**
   - Preço: R$ 89,90
   - Categoria: Lingerie

## 🚀 Comandos Úteis

### Iniciar servidor
```bash
python manage.py runserver
```

### Criar superusuário adicional
```bash
python manage.py createsuperuser
```

### Fazer migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Coletar arquivos estáticos (produção)
```bash
python manage.py collectstatic
```

## 🔧 Funcionalidades Testáveis

### ✅ Já Funcionais
- [ ] Página inicial (http://127.0.0.1:8000)
- [ ] Lista de produtos (http://127.0.0.1:8000/produtos/)
- [ ] Admin Django (http://127.0.0.1:8000/admin/)
- [ ] Gestão de produtos, fornecedores e categorias
- [ ] Sistema de autenticação básico

### 🚧 Em Desenvolvimento
- [ ] Detalhes do produto
- [ ] Carrinho de compras
- [ ] Sistema de checkout
- [ ] Pagamentos
- [ ] Painel administrativo customizado

## 📝 Próximos Passos

1. **Testar funcionalidades básicas**
   - Acessar a página inicial
   - Navegar pela lista de produtos
   - Testar o admin Django

2. **Adicionar mais produtos**
   - Usar o admin para cadastrar produtos
   - Fazer upload de imagens
   - Testar diferentes categorias

3. **Configurar integrações**
   - Configurar e-mail no .env
   - Configurar chaves do Stripe
   - Configurar chaves do Mercado Pago

4. **Implementar templates restantes**
   - Página de detalhes do produto
   - Templates do carrinho
   - Templates de checkout
   - Templates de usuário

---
**Data de criação**: {{ "now"|date:"d/m/Y H:i" }}
**Versão**: 1.0.0
