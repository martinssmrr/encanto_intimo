/* ==========================================================================
   ENCANTO ÍNTIMO - ADMIN PANEL JAVASCRIPT
   Funcionalidades modernas e interativas
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // =======================================================================
    // UTILITÁRIOS GERAIS
    // =======================================================================
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    function animateValue(element, start, end, duration) {
        const range = end - start;
        const startTime = performance.now();
        
        function updateValue(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (range * progress));
            
            element.textContent = current.toLocaleString('pt-BR');
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            }
        }
        
        requestAnimationFrame(updateValue);
    }
    
    // =======================================================================
    // DASHBOARD ESTATÍSTICAS ANIMADAS
    // =======================================================================
    
    function initStatistics() {
        const statNumbers = document.querySelectorAll('.stat-card .number');
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const finalValue = parseInt(element.textContent) || 0;
                    
                    element.textContent = '0';
                    
                    setTimeout(() => {
                        animateValue(element, 0, finalValue, 2000);
                    }, 300);
                    
                    observer.unobserve(element);
                }
            });
        }, observerOptions);
        
        statNumbers.forEach(number => {
            observer.observe(number);
        });
    }
    
    // =======================================================================
    // NAVEGAÇÃO RESPONSIVA
    // =======================================================================
    
    function initResponsiveNavigation() {
        // Criar botão de menu mobile
        const header = document.getElementById('header');
        if (header && !document.querySelector('.mobile-menu-toggle')) {
            const mobileToggle = document.createElement('button');
            mobileToggle.className = 'mobile-menu-toggle';
            mobileToggle.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            `;
            
            // Estilos do botão
            Object.assign(mobileToggle.style, {
                display: 'none',
                background: 'transparent',
                border: 'none',
                color: '#FFD700',
                padding: '8px',
                cursor: 'pointer',
                position: 'absolute',
                right: '20px',
                top: '50%',
                transform: 'translateY(-50%)',
                zIndex: '1001'
            });
            
            header.appendChild(mobileToggle);
            
            // Toggle da navegação mobile
            const navSidebar = document.getElementById('nav-sidebar');
            mobileToggle.addEventListener('click', () => {
                if (navSidebar) {
                    navSidebar.classList.toggle('show');
                }
            });
            
            // Mostrar/esconder botão baseado no tamanho da tela
            function checkScreenSize() {
                if (window.innerWidth <= 768) {
                    mobileToggle.style.display = 'block';
                } else {
                    mobileToggle.style.display = 'none';
                    if (navSidebar) {
                        navSidebar.classList.remove('show');
                    }
                }
            }
            
            window.addEventListener('resize', debounce(checkScreenSize, 250));
            checkScreenSize();
        }
    }
    
    // =======================================================================
    // ANIMAÇÕES DE ENTRADA
    // =======================================================================
    
    function initAnimations() {
        const animatedElements = document.querySelectorAll('.stat-card, .form-row, #result_list tbody tr');
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            animationObserver.observe(element);
        });
    }
    
    // =======================================================================
    // MELHORIAS DE UX
    // =======================================================================
    
    function initUXEnhancements() {
        // Auto-focus no primeiro campo de formulário
        const firstInput = document.querySelector('input[type="text"]:not([readonly]), input[type="email"]:not([readonly]), textarea:not([readonly])');
        if (firstInput && !document.querySelector('.has-error')) {
            firstInput.focus();
        }
        
        // Confirmação para ações de exclusão
        const deleteLinks = document.querySelectorAll('.deletelink, a[href*="delete"]');
        deleteLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                if (!confirm('⚠️ Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
                    e.preventDefault();
                }
            });
        });
        
        // Melhorar seletores de data/hora
        const dateInputs = document.querySelectorAll('input[type="date"], input[type="datetime-local"], input[type="time"]');
        dateInputs.forEach(input => {
            input.style.cursor = 'pointer';
        });
        
        // Adicionar tooltips para botões
        const buttons = document.querySelectorAll('.button, input[type="submit"]');
        buttons.forEach(button => {
            if (!button.title && button.textContent) {
                const text = button.textContent.trim();
                if (text.includes('Salvar')) {
                    button.title = 'Salvar alterações (Ctrl+S)';
                } else if (text.includes('Excluir')) {
                    button.title = 'Excluir item selecionado';
                } else if (text.includes('Adicionar')) {
                    button.title = 'Adicionar novo item';
                }
            }
        });
    }
    
    // =======================================================================
    // ATALHOS DE TECLADO
    // =======================================================================
    
    function initKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl+S para salvar
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                const saveButton = document.querySelector('input[type="submit"][value*="Salvar"], .button.default');
                if (saveButton) {
                    saveButton.click();
                }
            }
            
            // Ctrl+H para voltar ao início
            if (e.ctrlKey && e.key === 'h') {
                e.preventDefault();
                window.location.href = '/admin/';
            }
            
            // Ctrl+N para novo item (se na listagem)
            if (e.ctrlKey && e.key === 'n' && window.location.pathname.includes('changelist')) {
                e.preventDefault();
                const addButton = document.querySelector('a[href*="add/"]');
                if (addButton) {
                    window.location.href = addButton.href;
                }
            }
            
            // ESC para fechar modal ou voltar
            if (e.key === 'Escape') {
                const modal = document.querySelector('.modal, .popup');
                if (modal) {
                    modal.style.display = 'none';
                } else {
                    history.back();
                }
            }
        });
    }
    
    // =======================================================================
    // MELHORIAS NAS TABELAS
    // =======================================================================
    
    function initTableEnhancements() {
        const tables = document.querySelectorAll('#result_list');
        
        tables.forEach(table => {
            // Adicionar indicador de ordenação
            const headers = table.querySelectorAll('th a');
            headers.forEach(header => {
                if (header.href.includes('o=')) {
                    const isDesc = header.href.includes('-');
                    const arrow = isDesc ? ' ↓' : ' ↑';
                    if (!header.textContent.includes('↑') && !header.textContent.includes('↓')) {
                        header.textContent += arrow;
                    }
                }
            });
            
            // Destacar linha ativa
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('click', function() {
                    rows.forEach(r => r.style.backgroundColor = '');
                    this.style.backgroundColor = 'rgba(183, 28, 28, 0.1)';
                });
            });
        });
    }
    
    // =======================================================================
    // MELHORIAS NOS FORMULÁRIOS
    // =======================================================================
    
    function initFormEnhancements() {
        // Validação em tempo real
        const requiredFields = document.querySelectorAll('input[required], textarea[required], select[required]');
        
        requiredFields.forEach(field => {
            const label = document.querySelector(`label[for="${field.id}"]`);
            if (label && !label.querySelector('.required-indicator')) {
                const indicator = document.createElement('span');
                indicator.className = 'required-indicator';
                indicator.innerHTML = ' *';
                indicator.style.color = '#B71C1C';
                indicator.style.fontWeight = 'bold';
                label.appendChild(indicator);
            }
            
            field.addEventListener('blur', function() {
                if (this.value.trim() === '') {
                    this.style.borderColor = '#F44336';
                    this.style.boxShadow = '0 0 0 3px rgba(244, 67, 54, 0.1)';
                } else {
                    this.style.borderColor = '#4CAF50';
                    this.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.1)';
                }
            });
        });
        
        // Contador de caracteres para textareas
        const textareas = document.querySelectorAll('textarea[maxlength]');
        textareas.forEach(textarea => {
            const maxLength = parseInt(textarea.getAttribute('maxlength'));
            if (maxLength) {
                const counter = document.createElement('div');
                counter.className = 'char-counter';
                counter.style.cssText = `
                    text-align: right;
                    font-size: 12px;
                    color: #666;
                    margin-top: 4px;
                `;
                
                function updateCounter() {
                    const remaining = maxLength - textarea.value.length;
                    counter.textContent = `${textarea.value.length}/${maxLength} caracteres`;
                    counter.style.color = remaining < 50 ? '#F44336' : '#666';
                }
                
                textarea.addEventListener('input', updateCounter);
                textarea.parentNode.insertBefore(counter, textarea.nextSibling);
                updateCounter();
            }
        });
    }
    
    // =======================================================================
    // SISTEMA DE NOTIFICAÇÕES
    // =======================================================================
    
    function initNotifications() {
        // Auto-hide success messages
        const messages = document.querySelectorAll('.messagelist li');
        messages.forEach((message, index) => {
            setTimeout(() => {
                message.style.transform = 'translateX(0)';
                message.style.opacity = '1';
            }, index * 200);
            
            if (!message.classList.contains('error')) {
                setTimeout(() => {
                    message.style.transform = 'translateX(100%)';
                    message.style.opacity = '0';
                    setTimeout(() => message.remove(), 300);
                }, 5000);
            }
            
            // Click to dismiss
            message.style.cursor = 'pointer';
            message.addEventListener('click', () => {
                message.style.transform = 'translateX(100%)';
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 300);
            });
        });
        
        // Aplicar animação inicial
        messages.forEach(message => {
            message.style.transform = 'translateX(100%)';
            message.style.opacity = '0';
            message.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        });
    }
    
    // =======================================================================
    // TEMA ESCURO/CLARO (FUTURO)
    // =======================================================================
    
    function initThemeToggle() {
        // Detectar preferência do sistema
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const savedTheme = localStorage.getItem('admin-theme');
        
        if (savedTheme) {
            document.body.setAttribute('data-theme', savedTheme);
        } else if (prefersDark) {
            document.body.setAttribute('data-theme', 'dark');
        }
    }
    
    // =======================================================================
    // SEARCH ENHANCEMENTS
    // =======================================================================
    
    function initSearchEnhancements() {
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            // Adicionar placeholder mais descritivo
            searchInput.placeholder = 'Pesquisar... (Ctrl+F)';
            
            // Atalho Ctrl+F para focar na busca
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'f' && !e.defaultPrevented) {
                    e.preventDefault();
                    searchInput.focus();
                    searchInput.select();
                }
            });
            
            // Busca em tempo real (debounced)
            const form = searchInput.closest('form');
            if (form) {
                const debouncedSubmit = debounce(() => {
                    if (searchInput.value.length >= 3 || searchInput.value.length === 0) {
                        form.submit();
                    }
                }, 500);
                
                searchInput.addEventListener('input', debouncedSubmit);
            }
        }
    }
    
    // =======================================================================
    // INICIALIZAÇÃO GERAL
    // =======================================================================
    
    function init() {
        console.log('🎨 Encanto Íntimo Admin Theme carregado');
        
        // Aguardar um frame para garantir que o DOM está pronto
        requestAnimationFrame(() => {
            initStatistics();
            initResponsiveNavigation();
            initAnimations();
            initUXEnhancements();
            initKeyboardShortcuts();
            initTableEnhancements();
            initFormEnhancements();
            initNotifications();
            initThemeToggle();
            initSearchEnhancements();
        });
    }
    
    // =======================================================================
    // PERFORMANCE MONITORING
    // =======================================================================
    
    if (performance.mark) {
        performance.mark('admin-theme-start');
        
        window.addEventListener('load', () => {
            performance.mark('admin-theme-end');
            performance.measure('admin-theme-load', 'admin-theme-start', 'admin-theme-end');
            
            const measure = performance.getEntriesByName('admin-theme-load')[0];
            console.log(`⚡ Admin theme carregado em ${measure.duration.toFixed(2)}ms`);
        });
    }
    
    // Inicializar tudo
    init();
    
    // =======================================================================
    // EXPORT PARA DEBUGGING
    // =======================================================================
    
    window.EncantoIntimoAdmin = {
        init,
        debounce,
        animateValue
    };
});
