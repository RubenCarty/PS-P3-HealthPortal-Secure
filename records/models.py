import uuid
from django.db import models
from django.conf import settings
from patients.models import Patient
# Importamos nuestra herramienta de cifrado
from patients.encryption import EncryptedField 

class MedicalRecord(models.Model):
    """
    Núcleo clínico del sistema (Historia Médica).
    Relaciona al paciente con el médico que lo atiende.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Llaves foráneas (texto plano para filtros y ABAC)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='medical_records_doctor')
    
    created_at = models.DateTimeField(auto_now_add=True)

    # --------------------------------------------------------
    # Datos SENSIBLES (Cifrados en la Base de Datos - Semana 3)
    # --------------------------------------------------------
    diagnostico_cifrado = models.TextField()
    medicamentos_cifrados = models.TextField()
    notas_cifradas = models.TextField()

    # Aplicamos la "magia" del EncryptedField para usarlos normalmente en Python
    diagnostico = EncryptedField('diagnostico_cifrado')
    medicamentos = EncryptedField('medicamentos_cifrados')
    notas = EncryptedField('notas_cifradas')

    def __str__(self):
        # Mantenemos tu string original
        return f"Registro {self.id} - Paciente: {self.patient}"