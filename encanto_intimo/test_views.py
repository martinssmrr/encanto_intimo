from django.shortcuts import render, redirect
from django.contrib import messages

def teste_mensagens(request):
    """View para testar o sistema de mensagens"""
    messages.success(request, 'Esta é uma mensagem de sucesso!')
    messages.error(request, 'Esta é uma mensagem de erro!')
    messages.warning(request, 'Esta é uma mensagem de aviso!')
    messages.info(request, 'Esta é uma mensagem informativa!')
    
    return redirect('home')
