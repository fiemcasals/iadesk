from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.conf import settings
from .models import Usuario

def login_view(request):
    """Vista para iniciar sesión en la plataforma"""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = settings.LOGIN_REDIRECT_URL
            return redirect(next_url)
        else:
            error = 'Usuario o contraseña incorrectos. Por favor intenta de nuevo.'

    return render(request, 'login/login.html', {'error': error})

def register_view(request):
    """Vista para registrar una nueva cuenta de usuario"""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not username or not password:
            error = 'Todos los campos obligatorios deben completarse.'
        elif password != password_confirm:
            error = 'Las contraseñas no coinciden.'
        elif len(password) < 4:
            error = 'La contraseña debe tener al menos 4 caracteres.'
        elif User.objects.filter(username=username).exists():
            error = f"El usuario '{username}' ya existe. Elige otro nombre de usuario."
        else:
            # Crear usuario en el sistema de autenticación de Django
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Registrar también en el modelo Usuario de la app login
            try:
                Usuario.objects.get_or_create(nombre=username, email=email or f"{username}@local.dev")
            except Exception:
                pass

            # Iniciar sesión automáticamente
            auth_login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'login/register.html', {'error': error})

def logout_view(request):
    """Cierra la sesión y redirige a la pantalla de login"""
    auth_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
