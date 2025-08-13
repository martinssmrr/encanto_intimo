#!/usr/bin/env python
"""
Script de configuração inicial para o projeto Encanto Íntimo
Execute este script após instalar as dependências para configurar dados iniciais
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Configura o ambiente Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings')
    django.setup()

def criar_dados_iniciais():
    """Cria dados iniciais para testar o sistema"""
    from fornecedores.models import Fornecedor
    from produtos.models import Categoria, Tag, Produto
    from django.contrib.auth.models import User
    
    print("📦 Criando dados iniciais...")
    
    # Criar categorias
    categorias = [
        {'nome': 'Lingerie', 'descricao': 'Peças íntimas femininas'},
        {'nome': 'Produtos Sensuais', 'descricao': 'Produtos para casais'},
        {'nome': 'Acessórios', 'descricao': 'Acessórios complementares'},
        {'nome': 'Perfumaria', 'descricao': 'Perfumes e cosméticos'},
    ]
    
    for cat_data in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data['nome'],
            defaults={'descricao': cat_data['descricao']}
        )
        if created:
            print(f"✅ Categoria criada: {categoria.nome}")
    
    # Criar tags
    tags = [
        {'nome': 'Romântico', 'cor': '#ff69b4'},
        {'nome': 'Sensual', 'cor': '#dc143c'},
        {'nome': 'Conforto', 'cor': '#4169e1'},
        {'nome': 'Luxo', 'cor': '#ffd700'},
        {'nome': 'Presente', 'cor': '#9370db'},
    ]
    
    for tag_data in tags:
        tag, created = Tag.objects.get_or_create(
            nome=tag_data['nome'],
            defaults={'cor': tag_data['cor']}
        )
        if created:
            print(f"🏷️ Tag criada: {tag.nome}")
    
    # Criar fornecedor
    fornecedor, created = Fornecedor.objects.get_or_create(
        nome='Fornecedor Exemplo',
        defaults={
            'email': 'fornecedor@exemplo.com',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua Exemplo, 123 - São Paulo, SP',
            'observacoes': 'Fornecedor de exemplo para testes'
        }
    )
    if created:
        print(f"🏪 Fornecedor criado: {fornecedor.nome}")
    
    # Criar produtos de exemplo
    categoria_lingerie = Categoria.objects.get(nome='Lingerie')
    tag_romantico = Tag.objects.get(nome='Romântico')
    
    produtos_exemplo = [
        {
            'nome': 'Conjunto Romantic Lace',
            'descricao': 'Conjunto de lingerie em renda delicada com detalhes românticos. Peça confeccionada em renda francesa de alta qualidade.',
            'descricao_curta': 'Conjunto de lingerie em renda delicada',
            'preco': 199.90,
            'preco_promocional': 149.90,
            'categoria': categoria_lingerie,
            'fornecedor': fornecedor,
            'tamanhos_disponiveis': ['P', 'M', 'G', 'GG'],
            'cores_disponiveis': ['Preto', 'Branco', 'Vermelho'],
            'material': 'Renda francesa 85% Poliamida, 15% Elastano',
            'estoque_virtual': 50,
            'destaque': True,
        },
        {
            'nome': 'Baby Doll Sensual',
            'descricao': 'Baby doll em tecido acetinado com acabamento em renda. Design sensual e confortável para momentos especiais.',
            'descricao_curta': 'Baby doll em tecido acetinado',
            'preco': 129.90,
            'categoria': categoria_lingerie,
            'fornecedor': fornecedor,
            'tamanhos_disponiveis': ['P', 'M', 'G'],
            'cores_disponiveis': ['Rosa', 'Preto', 'Azul'],
            'material': 'Cetim 90% Poliéster, 10% Elastano',
            'estoque_virtual': 30,
        },
        {
            'nome': 'Camisola Comfort Night',
            'descricao': 'Camisola em modal super macio, perfeita para noites confortáveis. Tecido respirável e toque sedoso.',
            'descricao_curta': 'Camisola em modal super macio',
            'preco': 89.90,
            'categoria': categoria_lingerie,
            'fornecedor': fornecedor,
            'tamanhos_disponiveis': ['P', 'M', 'G', 'GG', 'XG'],
            'cores_disponiveis': ['Nude', 'Cinza', 'Rosa'],
            'material': 'Modal 95%, Elastano 5%',
            'estoque_virtual': 40,
        }
    ]
    
    for produto_data in produtos_exemplo:
        produto, created = Produto.objects.get_or_create(
            nome=produto_data['nome'],
            defaults=produto_data
        )
        if created:
            produto.tags.add(tag_romantico)
            print(f"🛍️ Produto criado: {produto.nome}")

def main():
    """Função principal"""
    print("🌸 Encanto Íntimo - Setup Inicial")
    print("=" * 50)
    
    try:
        setup_django()
        criar_dados_iniciais()
        
        print("\n✅ Setup concluído com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Execute: python manage.py createsuperuser")
        print("2. Execute: python manage.py runserver")
        print("3. Acesse: http://127.0.0.1:8000")
        print("4. Admin: http://127.0.0.1:8000/admin")
        
    except Exception as e:
        print(f"❌ Erro durante o setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
