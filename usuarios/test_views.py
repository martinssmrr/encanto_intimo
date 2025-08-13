from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse

def logout_view(request):
    """View simples de logout para teste"""
    auth_logout(request)
    return render(request, 'usuarios/logout.html')
