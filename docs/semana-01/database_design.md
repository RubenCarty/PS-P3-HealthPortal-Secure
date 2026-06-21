# Esquema de Base de Datos (Blueprint) — UQ·HealthShield

Este documento define la estructura de datos del sistema, separando estrictamente los datos operativos (texto plano) de la Información de Salud Protegida (PHI), la cual será cifrada cumpliendo la regla de "no cifrar lo que no necesita cifrarse para permitir filtros".

## 1. Aplicación: `accounts` (Autenticación y Roles)

Maneja el acceso y el motor de autorización (ABAC).

- **`id`** (UUID): Llave primaria. _Texto plano_.
- **`username`** / **`email`** (CharField / EmailField): Credenciales de acceso. _Texto plano (Para filtros de login)_.
- **`rol`** (CharField): Nivel de acceso (`paciente`, `medico`, `enfermero`, `admin`, `auditor`). _Texto plano (Requerido por ABAC)_.
- **`totp_secret`** (CharField): Clave para 2FA. _Texto plano / Hash interno_.

## 2. Aplicación: `patients` (Filiación)

Datos personales del paciente.

- **`id`** (UUID): Llave primaria. _Texto plano_.
- **`nombres`** / **`apellidos`** (CharField): Identificadores de búsqueda. _Texto plano (Para filtros en el panel)_.
- **`dni`** (EncryptedField): Documento de identidad. **[PHI - ALTAMENTE CONFIDENCIAL] Cifrado AES-256-GCM**.
- **`telefono`** (EncryptedField): Contacto. **[PHI - ALTAMENTE CONFIDENCIAL] Cifrado AES-256-GCM**.
- **`fecha_nacimiento`** (EncryptedField): Fecha de nacimiento. **[PHI - ALTAMENTE CONFIDENCIAL] Cifrado AES-256-GCM**.

## 3. Aplicación: `records` (Historia Clínica)

Núcleo médico del portal.

- **`id`** (UUID): Llave primaria. _Texto plano_.
- **`patient_id`** / **`doctor_id`** (ForeignKey): Llaves relacionales. _Texto plano (Para filtros ABAC)_.
- **`created_at`** (DateTimeField): Fecha de registro. _Texto plano_.
- **`diagnostico`** (EncryptedField): Evaluación médica. **[PHI - ALTAMENTE CONFIDENCIAL] Cifrado AES-256-GCM**.
- **`medicamentos`** (EncryptedField): Tratamiento prescrito. **[PHI - ALTAMENTE CONFIDENCIAL] Cifrado AES-256-GCM**.
- **`notas`** (EncryptedField): Evolución del paciente. **[PHI - ALTAMENTE CONFIDENCIAL] Cifrado AES-256-GCM**.

## 4. Aplicación: `consent` (Consentimiento Informado)

Registros de acceso otorgados por el paciente.

- **`id`** (UUID): Llave primaria. _Texto plano_.
- **`patient_id`** / **`doctor_id`** (ForeignKey): Relación de autorización. _Texto plano_.
- **`granted_at`** / **`expires_at`** (DateTimeField): Vigencia del acceso. _Texto plano_.
- **`integrity_hash`** (CharField): Firma criptográfica (SHA-256) para evitar manipulación en base de datos.
