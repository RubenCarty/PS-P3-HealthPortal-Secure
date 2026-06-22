from django.db import models
from .encryption import EncryptedField

class Patient(models.Model):
    # Datos NO sensibles (se guardan normales)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    # Datos SENSIBLES (Cifrados con nuestro motor)
    # Definimos las columnas en la base de datos para guardar el texto cifrado
    dni_cifrado = models.TextField()
    telefono_cifrado = models.TextField()
    fecha_nacimiento_cifrada = models.TextField()

    # Aplicamos la "magia" del EncryptedField para usarlos fácilmente en el código
    dni = EncryptedField('dni_cifrado')
    telefono = EncryptedField('telefono_cifrado')
    fecha_nacimiento = EncryptedField('fecha_nacimiento_cifrada')

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"