from .models import Carrinho, ItemCarrinho


def carrinho(request):
    """Context processor para disponibilizar dados do carrinho em todos os templates"""
    carrinho_obj = None
    total_itens = 0
    subtotal = 0
    
    if request.user.is_authenticated:
        try:
            carrinho_obj = Carrinho.objects.get(usuario=request.user)
            total_itens = carrinho_obj.total_itens
            subtotal = carrinho_obj.subtotal
        except Carrinho.DoesNotExist:
            pass
    else:
        # Para usuários anônimos, usar session
        session_key = request.session.session_key
        if session_key:
            try:
                carrinho_obj = Carrinho.objects.get(session_key=session_key)
                total_itens = carrinho_obj.total_itens
                subtotal = carrinho_obj.subtotal
            except Carrinho.DoesNotExist:
                pass
    
    return {
        'carrinho': carrinho_obj,
        'carrinho_total_itens': total_itens,
        'carrinho_subtotal': subtotal,
    }
