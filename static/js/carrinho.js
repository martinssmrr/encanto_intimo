/* Carrinho JavaScript - Sistema de Carrinho Dinâmico */

class CarrinhoManager {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initMasks();
    }

    // Formatação monetária
    formatMoney(value) {
        return 'R$ ' + parseFloat(value).toFixed(2).replace('.', ',');
    }

    // Máscaras de input
    initMasks() {
        // Máscara para CEP
        $(document).on('input', '#cep', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length <= 8) {
                value = value.replace(/^(\d{5})(\d)/, '$1-$2');
            }
            this.value = value;
        });

        // Máscara para telefone
        $(document).on('input', '#telefone', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/^(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                if (value.length < 14) {
                    value = value.replace(/^(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
                }
            }
            this.value = value;
        });

        // Máscara para CPF
        $(document).on('input', '#cpf', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            }
            this.value = value;
        });
    }

    // Eventos do carrinho
    bindEvents() {
        // Calcular frete
        $(document).on('submit', '#calcular-frete', (e) => {
            e.preventDefault();
            this.calcularFrete();
        });

        // Aumentar quantidade
        $(document).on('click', '.btn-increase', (e) => {
            const itemId = $(e.target).closest('.btn-increase').data('item-id');
            const input = $(`.quantity-input[data-item-id="${itemId}"]`);
            const currentValue = parseInt(input.val());
            const maxValue = parseInt(input.attr('max'));
            
            if (currentValue < maxValue) {
                input.val(currentValue + 1);
                this.updateQuantity(itemId, currentValue + 1);
            }
        });

        // Diminuir quantidade
        $(document).on('click', '.btn-decrease', (e) => {
            const itemId = $(e.target).closest('.btn-decrease').data('item-id');
            const input = $(`.quantity-input[data-item-id="${itemId}"]`);
            const currentValue = parseInt(input.val());
            
            if (currentValue > 1) {
                input.val(currentValue - 1);
                this.updateQuantity(itemId, currentValue - 1);
            }
        });

        // Mudança manual na quantidade
        $(document).on('change', '.quantity-input', (e) => {
            const itemId = $(e.target).data('item-id');
            const quantity = parseInt($(e.target).val());
            const maxValue = parseInt($(e.target).attr('max'));
            
            if (quantity < 1) {
                $(e.target).val(1);
                this.updateQuantity(itemId, 1);
            } else if (quantity > maxValue) {
                $(e.target).val(maxValue);
                this.updateQuantity(itemId, maxValue);
            } else {
                this.updateQuantity(itemId, quantity);
            }
        });

        // Remover item
        $(document).on('click', '.btn-remove', (e) => {
            const itemId = $(e.target).closest('.btn-remove').data('item-id');
            this.removeItem(itemId);
        });

        // Limpar carrinho
        $(document).on('click', '#limpar-carrinho', () => {
            this.clearCart();
        });

        // Checkout - buscar endereço por CEP
        $(document).on('blur', '#cep', (e) => {
            const cep = e.target.value.replace(/\D/g, '');
            if (cep.length === 8) {
                this.buscarEnderecoPorCep(cep);
                this.calcularFreteCheckout(cep);
            }
        });

        // Seleção de forma de pagamento
        $(document).on('click', '.payment-option', (e) => {
            $('.payment-option').removeClass('selected');
            $(e.currentTarget).addClass('selected');
            $(e.currentTarget).find('input[type="radio"]').prop('checked', true);
            this.atualizarTotalCheckout();
        });

        // Formulário de checkout
        $(document).on('submit', '#checkout-form', (e) => {
            this.submitCheckout(e);
        });
    }

    // Calcular frete no carrinho
    calcularFrete() {
        const cep = $('#cep').val().replace(/\D/g, '');
        if (cep.length !== 8) {
            $('#resultado-frete').html('<div class="alert alert-danger py-2">CEP inválido</div>');
            return;
        }

        $.ajax({
            url: window.urls.calcular_frete,
            method: 'POST',
            data: {
                'cep': cep,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: (data) => {
                if (data.success) {
                    $('.frete').text(this.formatMoney(data.frete));
                    $('.total').text(this.formatMoney(data.total));
                    $('#resultado-frete').html(`<div class="alert alert-success py-2">${data.message}</div>`);
                } else {
                    $('#resultado-frete').html(`<div class="alert alert-danger py-2">${data.message}</div>`);
                }
            },
            error: () => {
                $('#resultado-frete').html('<div class="alert alert-danger py-2">Erro ao calcular frete</div>');
            }
        });
    }

    // Atualizar quantidade via AJAX
    updateQuantity(itemId, quantity) {
        $.ajax({
            url: `/carrinho/atualizar/${itemId}/`,
            method: 'POST',
            data: {
                'quantidade': quantity,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: (data) => {
                if (data.success) {
                    if (data.removed) {
                        $(`.cart-item[data-item-id="${itemId}"]`).remove();
                        if ($('.cart-item').length === 0) {
                            location.reload();
                        }
                    } else {
                        $(`.item-total[data-item-id="${itemId}"]`).text(this.formatMoney(data.item_total));
                    }
                    this.updateTotals(data);
                    this.showMessage(data.message, 'success');
                } else {
                    this.showMessage(data.message, 'danger');
                }
            },
            error: () => {
                this.showMessage('Erro ao atualizar carrinho', 'danger');
            }
        });
    }

    // Remover item
    removeItem(itemId) {
        if (!confirm('Tem certeza que deseja remover este item?')) {
            return;
        }

        $.ajax({
            url: `/carrinho/remover/${itemId}/`,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: (data) => {
                if (data.success) {
                    $(`.cart-item[data-item-id="${itemId}"]`).remove();
                    this.updateTotals(data);
                    this.showMessage(data.message, 'success');
                    
                    if ($('.cart-item').length === 0) {
                        location.reload();
                    }
                } else {
                    this.showMessage(data.message, 'danger');
                }
            },
            error: () => {
                this.showMessage('Erro ao remover item', 'danger');
            }
        });
    }

    // Limpar carrinho
    clearCart() {
        if (!confirm('Tem certeza que deseja limpar o carrinho?')) {
            return;
        }

        $.ajax({
            url: window.urls.limpar_carrinho,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: (data) => {
                if (data.success) {
                    location.reload();
                }
            }
        });
    }

    // Atualizar totais na interface
    updateTotals(data) {
        $('.subtotal').text(this.formatMoney(data.subtotal));
        $('.total').text(this.formatMoney(data.total));
        
        // Atualizar contador no header
        if (data.total_itens > 0) {
            $('.carrinho-contador').text(data.total_itens).show();
        } else {
            $('.carrinho-contador').hide();
        }
    }

    // Buscar endereço por CEP (checkout)
    buscarEnderecoPorCep(cep) {
        $.getJSON(`https://viacep.com.br/ws/${cep}/json/`, (data) => {
            if (!data.erro) {
                $('#endereco').val(data.logradouro);
                $('#bairro').val(data.bairro);
                $('#cidade').val(data.localidade);
                $('#estado').val(data.uf);
            }
        });
    }

    // Calcular frete no checkout
    calcularFreteCheckout(cep) {
        $.ajax({
            url: window.urls.calcular_frete,
            method: 'POST',
            data: {
                'cep': cep,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: (data) => {
                if (data.success) {
                    $('.frete-valor').text('R$ ' + parseFloat(data.frete).toFixed(2).replace('.', ','));
                    this.atualizarTotalCheckout();
                }
            }
        });
    }

    // Atualizar total no checkout
    atualizarTotalCheckout() {
        if (!window.checkoutData) return;

        const formaPagamento = $('input[name="forma_pagamento"]:checked').val();
        const freteTexto = $('.frete-valor').text();
        let frete = 0;
        
        if (freteTexto !== 'A calcular') {
            frete = parseFloat(freteTexto.replace('R$ ', '').replace(',', '.'));
        }
        
        let total = window.checkoutData.subtotal + frete;
        let desconto = 0;
        
        // Aplicar desconto PIX
        if (formaPagamento === 'pix') {
            desconto = total * 0.05;
            total = total - desconto;
            $('.desconto-pix').show();
            $('.desconto-valor').text('- R$ ' + desconto.toFixed(2).replace('.', ','));
        } else {
            $('.desconto-pix').hide();
        }
        
        $('.total-valor').text('R$ ' + total.toFixed(2).replace('.', ','));
    }

    // Submeter formulário de checkout
    submitCheckout(e) {
        e.preventDefault();
        
        // Verificar se todos os campos obrigatórios estão preenchidos
        let valid = true;
        $(e.target).find('[required]').each(function() {
            if (!$(this).val()) {
                valid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!valid) {
            this.showMessage('Por favor, preencha todos os campos obrigatórios', 'danger');
            return;
        }
        
        // Verificar se o frete foi calculado
        if ($('.frete-valor').text() === 'A calcular') {
            this.showMessage('Por favor, informe o CEP para calcular o frete', 'danger');
            $('#cep').focus();
            return;
        }
        
        // Desabilitar botão e enviar
        const submitBtn = $(e.target).find('button[type="submit"]');
        const originalText = submitBtn.html();
        
        submitBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Processando...');
        
        // Enviar formulário
        setTimeout(() => {
            $.ajax({
                url: window.urls.finalizar_compra,
                method: 'POST',
                data: $(e.target).serialize(),
                success: (data) => {
                    if (data.success) {
                        window.location.href = data.redirect_url;
                    } else {
                        this.showMessage(data.message, 'danger');
                        submitBtn.prop('disabled', false).html(originalText);
                    }
                },
                error: () => {
                    this.showMessage('Erro ao processar pedido. Tente novamente.', 'danger');
                    submitBtn.prop('disabled', false).html(originalText);
                }
            });
        }, 2000);
    }

    // Mostrar mensagens
    showMessage(message, type) {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        // Remover alertas existentes
        $('.alert').remove();
        
        // Adicionar novo alerta no topo
        $('main').prepend(alertHtml);
        
        // Scroll para o topo
        $('html, body').animate({ scrollTop: 0 }, 300);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            $('.alert').fadeOut();
        }, 5000);
    }
}

// Adicionar produto ao carrinho (função global para uso em qualquer página)
function adicionarAoCarrinho(produtoId, quantidade = 1, tamanho = '', cor = '') {
    $.ajax({
        url: `/carrinho/adicionar/${produtoId}/`,
        method: 'POST',
        data: {
            'quantidade': quantidade,
            'tamanho': tamanho,
            'cor': cor,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(data) {
            if (data.success) {
                // Atualizar contador do carrinho
                $('.carrinho-contador').text(data.total_itens).show();
                
                // Mostrar mensagem de sucesso
                window.carrinhoManager.showMessage(data.message, 'success');
                
                // Opcional: mostrar mini carrinho
                if (typeof atualizarMiniCarrinho === 'function') {
                    atualizarMiniCarrinho();
                }
            } else {
                window.carrinhoManager.showMessage(data.message, 'danger');
            }
        },
        error: function() {
            window.carrinhoManager.showMessage('Erro ao adicionar produto ao carrinho', 'danger');
        }
    });
}

// Inicializar quando o documento estiver pronto
$(document).ready(function() {
    window.carrinhoManager = new CarrinhoManager();
});
