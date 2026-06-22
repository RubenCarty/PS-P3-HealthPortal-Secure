import uuid
from django.db import models
from django.conf import settings
from patients.models import Patient

class ConsentRecord(models.Model):
    """
    Registro de consentimiento y control de acceso (Motor ABAC).
    Mapea qué médico tiene permiso temporal para ver la historia de un paciente.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relaciones
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consent_given')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consent_received')
    
    # Vigencia del acceso
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    # Hash SHA-256 para auditoría y evitar manipulación en la base de datos
    integrity_hash = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Acceso: Dr. {self.doctor.username} -> Paciente: {self.patient.apellidos}"