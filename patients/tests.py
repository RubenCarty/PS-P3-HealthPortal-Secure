from django.test import TestCase
from patients.encryption import PHIEncryption

class EncryptionTests(TestCase):
    
    def test_cifrado_y_descifrado_correcto(self):
        """Verifica que un dato se cifre y se pueda recuperar exactamente igual."""
        texto_original = "Diagnóstico ultra secreto: Hipertensión"
        
        # Ciframos
        texto_cifrado = PHIEncryption.encrypt(texto_original)
        self.assertNotEqual(texto_original, texto_cifrado) # Comprobamos que sí cambió
        
        # Desciframos
        texto_recuperado = PHIEncryption.decrypt(texto_cifrado)
        self.assertEqual(texto_original, texto_recuperado) # Comprobamos que regresó a la normalidad

    def test_dato_alterado_excepcion_capturada(self):
        """Verifica que si un hacker altera un bit del texto cifrado, el sistema lo bloquea."""
        texto_original = "Dato médico vital"
        texto_cifrado = PHIEncryption.encrypt(texto_original)
        
        # Simulamos a un hacker alterando el último caracter de la cadena cifrada
        cifrado_alterado = texto_cifrado[:-1] + ('A' if texto_cifrado[-1] != 'A' else 'B')
        
        # Al intentar descifrar el dato corrupto, nuestro motor debe devolver la excepción de la rúbrica
        texto_recuperado = PHIEncryption.decrypt(cifrado_alterado)
        self.assertEqual(texto_recuperado, "[DATO NO DISPONIBLE]")