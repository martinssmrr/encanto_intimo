"""
Serviços de integração com o Mercado Pago
"""
import mercadopago
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class MercadoPagoService:
    """Classe para gerenciar integração com Mercado Pago"""
    
    def __init__(self):
        """Inicializa SDK do Mercado Pago"""
        self.sdk = mercadopago.SDK(settings.MERCADO_PAGO['ACCESS_TOKEN'])
        if settings.MERCADO_PAGO.get('SANDBOX', True):
            self.sdk.test_mode = True
    
    def criar_preferencia_pagamento(self, carrinho_items, pedido_id, request):
        """
        Cria uma preferência de pagamento no Mercado Pago
        
        Args:
            carrinho_items: Lista de itens do carrinho
            pedido_id: ID do pedido criado
            request: Request object do Django
            
        Returns:
            dict: Resposta da API do Mercado Pago
        """
        try:
            # Preparar itens para o Mercado Pago
            items = []
            total = Decimal('0.00')
            
            for item in carrinho_items:
                preco_unitario = float(item.produto.preco_final)
                quantidade = item.quantidade
                subtotal = preco_unitario * quantidade
                total += Decimal(str(subtotal))
                
                items.append({
                    "id": str(item.produto.id),
                    "title": item.produto.nome,
                    "description": item.produto.descricao[:250] if item.produto.descricao else item.produto.nome,
                    "picture_url": self._get_produto_image_url(item.produto, request),
                    "category_id": "fashion",
                    "quantity": quantidade,
                    "unit_price": preco_unitario,
                    "currency_id": "BRL"
                })
            
            # URLs de retorno
            base_url = f"{request.scheme}://{request.get_host()}"
            
            # Log para debug
            success_url = f"{base_url}{reverse('pagamentos:sucesso')}"
            failure_url = f"{base_url}{reverse('pagamentos:falha')}"
            pending_url = f"{base_url}{reverse('pagamentos:pendente')}"
            webhook_url = f"{base_url}{reverse('pagamentos:webhook')}"
            
            logger.info(f"URLs construídas - Success: {success_url}, Failure: {failure_url}, Pending: {pending_url}, Webhook: {webhook_url}")
            
            preference_data = {
                "items": items,
                "external_reference": str(pedido_id),
                "payment_methods": {
                    "excluded_payment_methods": [],
                    "excluded_payment_types": [],
                    "installments": 12  # Até 12 parcelas
                },
                "back_urls": {
                    "success": success_url,
                    "failure": failure_url,
                    "pending": pending_url
                },
                # Removendo notification_url temporariamente para desenvolvimento local
                # "notification_url": webhook_url,
                "metadata": {
                    "pedido_id": str(pedido_id),
                    "total_amount": str(total)
                },
                "statement_descriptor": "ENCANTO INTIMO"
            }
            
            logger.info(f"Criando preferência MP para pedido {pedido_id}")
            logger.debug(f"Dados da preferência: {preference_data}")
            
            response = self.sdk.preference().create(preference_data)
            logger.debug(f"Resposta do MP: {response}")
            
            if response["status"] == 201:
                logger.info(f"Preferência criada com sucesso: {response['response']['id']}")
                return {
                    "status": "success",
                    "preference_id": response["response"]["id"],
                    "init_point": response["response"]["init_point"],
                    "sandbox_init_point": response["response"]["sandbox_init_point"]
                }
            else:
                logger.error(f"Erro ao criar preferência: {response}")
                return {
                    "status": "error",
                    "message": "Erro ao criar preferência de pagamento",
                    "details": response
                }
                
        except Exception as e:
            logger.error(f"Exceção ao criar preferência MP: {str(e)}")
            return {
                "status": "error",
                "message": f"Erro interno: {str(e)}"
            }
    
    def _get_produto_image_url(self, produto, request):
        """Obtém URL completa da imagem do produto"""
        try:
            if produto.imagem_principal:
                return f"{request.scheme}://{request.get_host()}{produto.imagem_principal.url}"
            else:
                # URL de imagem padrão
                return f"{request.scheme}://{request.get_host()}/static/images/produto-sem-foto.jpg"
        except:
            return None
    
    def verificar_pagamento(self, payment_id):
        """
        Verifica status de um pagamento
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
            
        Returns:
            dict: Informações do pagamento
        """
        try:
            response = self.sdk.payment().get(payment_id)
            
            if response["status"] == 200:
                payment_data = response["response"]
                return {
                    "status": "success",
                    "payment_status": payment_data.get("status"),
                    "status_detail": payment_data.get("status_detail"),
                    "external_reference": payment_data.get("external_reference"),
                    "transaction_amount": payment_data.get("transaction_amount"),
                    "payment_method": payment_data.get("payment_method_id"),
                    "payment_data": payment_data
                }
            else:
                return {
                    "status": "error",
                    "message": "Pagamento não encontrado"
                }
                
        except Exception as e:
            logger.error(f"Erro ao verificar pagamento {payment_id}: {str(e)}")
            return {
                "status": "error",
                "message": f"Erro ao verificar pagamento: {str(e)}"
            }
    
    def processar_webhook_notification(self, notification_data):
        """
        Processa notificação webhook do Mercado Pago
        
        Args:
            notification_data: Dados da notificação
            
        Returns:
            dict: Resultado do processamento
        """
        try:
            # Tipos de notificação
            if notification_data.get("type") == "payment":
                payment_id = notification_data.get("data", {}).get("id")
                
                if payment_id:
                    return self.verificar_pagamento(payment_id)
                    
            return {
                "status": "ignored",
                "message": "Tipo de notificação não processado"
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {str(e)}")
            return {
                "status": "error",
                "message": f"Erro ao processar webhook: {str(e)}"
            }
