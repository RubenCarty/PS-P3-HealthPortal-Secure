import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para UQ·HealthShield.
    Hereda de AbstractUser para mantener username, email y passwords seguros,
    pero cambia el ID a UUID y agrega el control de roles (ABAC).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Opciones de roles estrictas para el control de acceso
    ROLE_CHOICES = [
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
        ('enfermero', 'Enfermero'),
        ('admin', 'Administrador'),
        ('auditor', 'Auditor'),
    ]
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='paciente')
    
    # Clave secreta para validación 2FA (Semana 2)
    totp_secret = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"