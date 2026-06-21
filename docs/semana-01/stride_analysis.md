# Análisis de Amenazas STRIDE — UQ·HealthShield

Este documento detalla el modelado de amenazas utilizando la metodología STRIDE para el portal de salud UQ·HealthShield, justificando las decisiones de arquitectura y seguridad a implementar.

## 1. S - Spoofing (Falsificación de Identidad)

- **Amenaza:** Un atacante intenta hacerse pasar por un médico o administrador usando credenciales robadas (phishing) para acceder a historias clínicas.
- **Mitigación en el Sistema:** Se implementará autenticación de doble factor (2FA) obligatoria basada en TOTP (Time-based One-Time Password) para los roles críticos (médico y admin). Además, `django-axes` bloqueará intentos de fuerza bruta en el login tras 5 fallos.

## 2. T - Tampering (Alteración de Datos)

- **Amenaza:** Un atacante con acceso a la base de datos o un usuario malicioso intenta modificar un diagnóstico o una receta médica sin autorización.
- **Mitigación en el Sistema:** Los datos de salud protegidos (PHI) estarán cifrados. Además, se creará un _Audit Trail_ inmutable que registrará cualquier cambio o acceso, garantizando la integridad de los registros.

## 3. R - Repudiation (Repudio)

- **Amenaza:** Un usuario (ej. un médico o auditor) realiza una acción indebida (como visualizar la historia de un paciente que no le corresponde) y luego niega haberlo hecho.
- **Mitigación en el Sistema:** El _Audit Trail_ funcionará como un registro inmutable. Cada acceso generará un log con fecha, hora, usuario y dato accedido, sin permisos de `UPDATE` o `DELETE` a nivel de base de datos para esa tabla. Se implementarán firmas criptográficas para el módulo de consentimiento.

## 4. I - Information Disclosure (Divulgación de Información)

- **Amenaza:** Fuga de datos masiva debido a una inyección SQL, robo de backups de la base de datos o exposición de datos en tránsito.
- **Mitigación en el Sistema:**
  - **En Reposo:** Cifrado end-to-end con AES-256-GCM para todos los campos PHI.
  - **En Tránsito:** Forzado de HTTPS (HSTS, `SECURE_SSL_REDIRECT = True`).

## 5. D - Denial of Service (Denegación de Servicio)

- **Amenaza:** Un atacante inunda el endpoint de login con solicitudes automáticas.
- **Mitigación en el Sistema:** Uso de Rate Limiting y bloqueo de IPs maliciosas mediante la librería `django-axes`.

## 6. E - Elevation of Privilege (Elevación de Privilegios)

- **Amenaza:** Un paciente intenta manipular la URL o los parámetros para ver los datos de otro paciente, o un enfermero intenta obtener permisos de administrador.
- **Mitigación en el Sistema:** Implementación de ABAC (Attribute-Based Access Control) granular para verificar atributos antes de cargar la vista.
