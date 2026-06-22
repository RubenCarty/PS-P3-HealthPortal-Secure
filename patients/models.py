import uuid
from django.db import models

class Patient(models.Model):
    """
    Modelo para almacenar los datos de filiación del paciente.
    Los nombres y apellidos se mantienen en texto plano para permitir filtros.
    Campos como DNI, teléfono y fecha de nacimiento quedan preparados 
    para el cifrado obligatorio AES-256-GCM de la Semana 3.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    
    # NOTA: Estos campos se manejarán como texto plano temporalmente en la Semana 2
    # para las migraciones iniciales, y se transformarán en EncryptedField en la Semana 3.
    dni = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"