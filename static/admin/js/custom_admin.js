/**
 * CUSTOM ADMIN JS - ENCANTO ÍNTIMO
 * Funcionalidades JavaScript personalizadas para o Django Admin
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. CONTADORES DO DASHBOARD
    initDashboardCounters();
    
    // 2. CONFIRMAÇÃO DE AÇÕES
    initActionConfirmations();
    
    // 3. MELHORIAS DE UX
    initUXImprovements();
    
    // 4. AUTO-REFRESH PARA PEDIDOS
    initAutoRefresh();
    
    // 5. FILTROS RÁPIDOS
    initQuickFilters();
    
});

/**
 * Inicializa contadores animados no dashboard
 */
function initDashboardCounters() {
    const counters = document.querySelectorAll('.dashboard-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        const duration = 1000; // 1 segundo
        const step = target / (duration / 16); // 60fps
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current);
        }, 16);
    });
}

/**
 * Adiciona confirmações para ações críticas
 */
function initActionConfirmations() {
    // Confirmação para ações de exclusão
    const deleteButtons = document.querySelectorAll('input[value*="delete"], input[value*="deletar"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('⚠️ Tem certeza que deseja executar esta ação? Esta operação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });
    
    // Confirmação para mudanças de status em massa
    const statusActions = document.querySelectorAll('option[value*="status"], option[value*="confirmar"]');
    statusActions.forEach(option => {
        option.parentElement.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.value.includes('cancelar') || selectedOption.value.includes('deletar')) {
                // Adicionar confirmação no submit do form
                const form = this.closest('form');
                form.addEventListener('submit', function(e) {
                    if (!confirm('⚠️ Confirma a execução desta ação em massa?')) {
                        e.preventDefault();
                    }
                });
            }
        });
    });
}

/**
 * Melhorias gerais de UX
 */
function initUXImprovements() {
    // 1. Tooltip para botões
    addTooltips();
    
    // 2. Destacar linhas ao passar o mouse
    enhanceTableRows();
    
    // 3. Auto-save draft para formulários longos
    initAutoSave();
    
    // 4. Melhorar campos de data
    enhanceDateFields();
    
    // 5. Shortcuts de teclado
    initKeyboardShortcuts();
}

/**
 * Adiciona tooltips informativos
 */
function addTooltips() {
    const tooltips = {
        'input[name="status"]': 'Altere o status do pedido aqui',
        'input[name="pagamento_confirmado"]': 'Marque quando o pagamento for confirmado',
        'input[name="ativo"]': 'Desative para ocultar o cliente/produto',
        '.action-checkbox': 'Selecione itens para ações em massa'
    };
    
    Object.entries(tooltips).forEach(([selector, text]) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            el.title = text;
            el.style.cursor = 'help';
        });
    });
}

/**
 * Melhora a experiência das linhas da tabela
 */
function enhanceTableRows() {
    const rows = document.querySelectorAll('#changelist-table tbody tr');
    
    rows.forEach(row => {
        // Clique na linha seleciona checkbox
        row.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'INPUT') {
                const checkbox = this.querySelector('.action-checkbox');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    this.classList.toggle('selected', checkbox.checked);
                }
            }
        });
        
        // Visual feedback
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#fef2f2';
        });
        
        row.addEventListener('mouseleave', function() {
            if (!this.classList.contains('selected')) {
                this.style.backgroundColor = '';
            }
        });
    });
}

/**
 * Auto-save para formulários longos
 */
function initAutoSave() {
    const forms = document.querySelectorAll('#changelist-form, .change-form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        let saveTimeout;
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                // Salvar no localStorage após 2 segundos de inatividade
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData);
                    localStorage.setItem('admin_draft_' + window.location.pathname, JSON.stringify(data));
                    
                    // Mostrar indicador de salvamento
                    showSaveIndicator();
                }, 2000);
            });
        });
    });
}

/**
 * Melhora campos de data com formatação automática
 */
function enhanceDateFields() {
    const dateFields = document.querySelectorAll('input[type="date"], .vDateField');
    
    dateFields.forEach(field => {
        // Adicionar placeholder
        if (!field.placeholder) {
            field.placeholder = 'dd/mm/aaaa';
        }
        
        // Formatação automática para campos de texto
        if (field.classList.contains('vDateField')) {
            field.addEventListener('input', function() {
                let value = this.value.replace(/\D/g, '');
                if (value.length >= 2) {
                    value = value.substring(0, 2) + '/' + value.substring(2);
                }
                if (value.length >= 5) {
                    value = value.substring(0, 5) + '/' + value.substring(5, 9);
                }
                this.value = value;
            });
        }
    });
}

/**
 * Shortcuts de teclado úteis
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl + S = Salvar
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            const saveButton = document.querySelector('input[type="submit"][name="_save"]');
            if (saveButton) {
                saveButton.click();
            }
        }
        
        // Ctrl + A = Selecionar todos (em listas)
        if (e.ctrlKey && e.key === 'a' && document.querySelector('#changelist-table')) {
            e.preventDefault();
            const selectAllCheckbox = document.querySelector('#action-toggle');
            if (selectAllCheckbox) {
                selectAllCheckbox.click();
            }
        }
        
        // Escape = Cancelar/voltar
        if (e.key === 'Escape') {
            const cancelButton = document.querySelector('.cancel-link, input[name="_cancel"]');
            if (cancelButton) {
                cancelButton.click();
            }
        }
    });
}

/**
 * Auto-refresh para lista de pedidos (opcional)
 */
function initAutoRefresh() {
    // Só ativar na lista de pedidos
    if (window.location.pathname.includes('/pedidos/pedido/')) {
        const refreshInterval = 30000; // 30 segundos
        
        setInterval(() => {
            // Verificar se há mudanças no servidor
            fetch(window.location.href, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                // Comparar timestamps ou conteúdo específico
                // Implementar atualização seletiva se necessário
            })
            .catch(error => {
                console.log('Auto-refresh error:', error);
            });
        }, refreshInterval);
    }
}

/**
 * Filtros rápidos personalizados
 */
function initQuickFilters() {
    // Adicionar filtros rápidos para status de pedidos
    if (document.querySelector('#changelist-filter')) {
        addQuickStatusFilters();
    }
    
    // Filtro de data rápida
    addQuickDateFilters();
}

/**
 * Adiciona filtros rápidos de status
 */
function addQuickStatusFilters() {
    const filterDiv = document.querySelector('#changelist-filter');
    if (!filterDiv) return;
    
    const quickFilters = document.createElement('div');
    quickFilters.className = 'quick-filters';
    quickFilters.innerHTML = `
        <h3>🚀 Filtros Rápidos</h3>
        <div class="quick-filter-buttons">
            <button type="button" class="button quick-filter" data-filter="status=pendente">
                Pendentes
            </button>
            <button type="button" class="button quick-filter" data-filter="status=confirmado">
                Confirmados
            </button>
            <button type="button" class="button quick-filter" data-filter="status=enviado">
                Enviados
            </button>
            <button type="button" class="button quick-filter" data-filter="pagamento_confirmado=True">
                Pagos
            </button>
        </div>
    `;
    
    filterDiv.insertBefore(quickFilters, filterDiv.firstChild);
    
    // Adicionar event listeners
    const filterButtons = quickFilters.querySelectorAll('.quick-filter');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            const url = new URL(window.location.href);
            const [key, value] = filter.split('=');
            url.searchParams.set(key, value);
            window.location.href = url.toString();
        });
    });
}

/**
 * Adiciona filtros de data rápidos
 */
function addQuickDateFilters() {
    const filterDiv = document.querySelector('#changelist-filter');
    if (!filterDiv) return;
    
    const dateFilters = document.createElement('div');
    dateFilters.className = 'quick-date-filters';
    dateFilters.innerHTML = `
        <h3>📅 Período</h3>
        <div class="quick-date-buttons">
            <button type="button" class="button quick-date" data-days="1">Hoje</button>
            <button type="button" class="button quick-date" data-days="7">7 dias</button>
            <button type="button" class="button quick-date" data-days="30">30 dias</button>
            <button type="button" class="button quick-date" data-days="90">3 meses</button>
        </div>
    `;
    
    filterDiv.appendChild(dateFilters);
    
    // Event listeners para filtros de data
    const dateButtons = dateFilters.querySelectorAll('.quick-date');
    dateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const days = parseInt(this.dataset.days);
            const endDate = new Date();
            const startDate = new Date();
            startDate.setDate(endDate.getDate() - days);
            
            const url = new URL(window.location.href);
            url.searchParams.set('data_pedido__gte', startDate.toISOString().split('T')[0]);
            url.searchParams.set('data_pedido__lte', endDate.toISOString().split('T')[0]);
            window.location.href = url.toString();
        });
    });
}

/**
 * Mostra indicador de salvamento automático
 */
function showSaveIndicator() {
    // Remover indicador existente
    const existing = document.querySelector('.save-indicator');
    if (existing) {
        existing.remove();
    }
    
    // Criar novo indicador
    const indicator = document.createElement('div');
    indicator.className = 'save-indicator';
    indicator.innerHTML = '💾 Rascunho salvo automaticamente';
    indicator.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #22c55e;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(indicator);
    
    // Animar entrada
    setTimeout(() => {
        indicator.style.opacity = '1';
    }, 100);
    
    // Remover após 3 segundos
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }, 300);
    }, 3000);
}

/**
 * Adiciona CSS dinâmico para melhorias
 */
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .quick-filters, .quick-date-filters {
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            border: 1px solid #e5e7eb;
        }
        
        .quick-filter-buttons, .quick-date-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        
        .quick-filter, .quick-date {
            font-size: 12px !important;
            padding: 6px 12px !important;
            background: white !important;
            border: 1px solid #d1d5db !important;
            color: #374151 !important;
        }
        
        .quick-filter:hover, .quick-date:hover {
            background: #DC2626 !important;
            color: white !important;
            border-color: #DC2626 !important;
        }
        
        .selected {
            background-color: #fef2f2 !important;
        }
        
        @media (max-width: 768px) {
            .quick-filter-buttons, .quick-date-buttons {
                flex-direction: column;
            }
            
            .quick-filter, .quick-date {
                width: 100%;
                text-align: center;
            }
        }
    `;
    document.head.appendChild(style);
}

// Aplicar estilos dinâmicos
addDynamicStyles();
