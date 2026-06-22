import uuid
from django.db import models
from django.conf import settings
from patients.models import Patient

class MedicalRecord(models.Model):
    """
    Núcleo clínico del sistema (Historia Médica).
    Relaciona al paciente con el médico que lo atiende.
    Los campos de diagnóstico, medicamentos y notas están preparados
    para ser convertidos a EncryptedField (cifrado AES-256-GCM) en la Semana 3.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Llaves foráneas (texto plano para filtros y ABAC)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='records_created')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # NOTA: Se usan campos de texto normales temporalmente para las migraciones
    # de la Semana 2. En la Semana 3 se cambiarán a cifrados.
    diagnostico = models.TextField()
    medicamentos = models.TextField()
    notas = models.TextField()

    def __str__(self):
        return f"Registro {self.id} - Paciente: {self.patient.apellidos}"