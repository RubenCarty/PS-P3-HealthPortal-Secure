from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .utils import generate_totp_secret, get_totp_qr_code, verify_totp

User = get_user_model()

def login_view(request):
    """Vista del paso 1: Usuario y Contraseña."""
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            # Requisito S2: TOTP obligatorio (médicos/admins) y opcional (si el paciente/enfermero ya tiene uno)
            if user.rol in ['medico', 'admin'] or user.totp_secret:
                # Lo mandamos a la sala de espera del 2FA
                request.session['pre_2fa_user_id'] = str(user.id)
                return redirect('verify_2fa')
            else:
                # Pacientes y enfermeros sin 2FA activado entran directo
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Recuerda que al 5to intento serás bloqueado.")
            
    return render(request, 'accounts/login.html')

def verify_2fa_view(request):
    """Vista del paso 2: Escanear QR o ingresar código de 6 dígitos."""
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login') # Si intentan entrar aquí sin pasar por el login, los devolvemos
        
    user = User.objects.get(id=user_id)
    qr_code = None
    
    # Si es su primera vez y no tiene clave, le generamos una nueva
    if not user.totp_secret:
        user.totp_secret = generate_totp_secret()
        user.save()
        
    # Generamos el QR en formato Base64 para mostrarlo en el HTML
    qr_code = get_totp_qr_code(user.username, user.totp_secret)
    
    if request.method == 'POST':
        token = request.POST.get('totp_token')
        # Verificamos si el código de 6 dígitos coincide
        if verify_totp(user.totp_secret, token):
            
            # --- LÍNEA CORREGIDA ---
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            del request.session['pre_2fa_user_id'] # Limpiamos la sala de espera
            return redirect('home') # 'home' lo crearemos más adelante
        else:
            messages.error(request, "Código de seguridad incorrecto. Intenta de nuevo.")
            
    return render(request, 'accounts/verify_2fa.html', {'qr_code': qr_code})