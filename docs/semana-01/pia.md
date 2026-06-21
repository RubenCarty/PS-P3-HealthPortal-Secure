# Privacy Impact Assessment (PIA) — UQ·HealthShield

## 1. Introducción

Este documento evalúa el impacto en la privacidad del portal de salud digital UQ·HealthShield. El objetivo principal es garantizar que el sistema cumpla con la confidencialidad, integridad y disponibilidad requerida por los estándares de HIPAA y el Artículo 9 de la Ley N°29733 del Perú.

## 2. Clasificación de la Información

Para el diseño seguro de la base de datos, la información se ha categorizado en 3 niveles:

| Nivel de Privacidad              | Datos del Sistema                                                                  | Tratamiento Técnico                                                                                                     |
| :------------------------------- | :--------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| **Público**                      | Información general expuesta en la landing page del portal.                        | Accesible en internet sin requerir autenticación.                                                                       |
| **Confidencial**                 | Tablas de control ABAC, consentimientos digitales, roles de usuario y audit trail. | Requiere autenticación 2FA y control ABAC. **No se cifran** para permitir la ejecución de filtros de búsqueda en la BD. |
| **Altamente Confidencial (PHI)** | Diagnósticos, medicamentos, notas clínicas, DNI y teléfono.                        | **Cifrado obligatorio con AES-256-GCM** transparente en modelos Django (`EncryptedField`).                              |

## 3. Identificación de Riesgos y Mitigación

- **Riesgo:** Exposición de datos clínicos (texto plano) ante una brecha de la base de datos.
  - **Mitigación:** Aplicación de cifrado AES-256-GCM a todos los campos PHI, asegurando que un atacante solo obtenga cadenas ilegibles en base64.
- **Riesgo:** Visualización de historias clínicas por médicos no autorizados (Control de acceso genérico).
  - **Mitigación:** Arquitectura ABAC (Attribute-Based Access Control), donde el paciente otorga consentimiento digital y solo su médico tratante tiene permisos de lectura.

## 4. Trazabilidad

Se implementará un _Audit Trail_ inmutable. Cada vez que un usuario consulte un dato clasificado como Altamente Confidencial, se registrará el evento sin posibilidad de modificación o eliminación (sin sentencias UPDATE/DELETE en la tabla).
