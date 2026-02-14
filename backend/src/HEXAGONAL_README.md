# AI Cloud Cost Auditor - Arquitectura Hexagonal (Clean Architecture)

## 🏗️ Estructura Hexagonal Completa

```
backend/src/
├── domain/                          # CAPA DE DOMINIO (Núcleo del negocio)
│   ├── entities/                    # Entidades puras de negocio
│   │   ├── user.py                  # ✅ Usuario con reglas de negocio
│   │   ├── organization.py          # ✅ Organización
│   │   ├── audit.py                 # ✅ Auditoría con FSM (estados)
│   │   ├── rule.py                  # ✅ Regla con evaluación
│   │   ├── finding.py               # ✅ Finding/Resultado
│   │   └── __init__.py
│   ├── repositories/                # Ports (Interfaces)
│   │   ├── user_repository.py       # ✅ Interface UserRepo
│   │   ├── organization_repository.py
│   │   ├── audit_repository.py
│   │   ├── rule_repository.py
│   │   ├── finding_repository.py
│   │   └── __init__.py
│   ├── services/                    # Servicios de dominio
│   │   ├── auth_service.py          # ✅ Lógica de autenticación
│   │   ├── audit_service.py         # ✅ Procesamiento de auditorías
│   │   └── __init__.py
│   └── exceptions/                  # Excepciones de dominio
│       └── __init__.py              # ✅ Todas las excepciones
│
├── application/                     # CAPA DE APLICACIÓN
│   ├── use_cases/                   # Casos de uso (orquestación)
│   │   ├── register_user.py         # ✅ Registro de usuario
│   │   ├── login_user.py            # ✅ Login
│   │   ├── common_use_cases.py      # ✅ Otros use cases
│   │   └── __init__.py
│   └── dto/                         # Data Transfer Objects (Pydantic)
│       └── __init__.py              # ✅ Todos los DTOs
│
└── infrastructure/                  # CAPA DE INFRAESTRUCTURA
    ├── persistence/
    │   ├── models/                  # SQLAlchemy models
    │   │   └── __init__.py          # ✅ Todos los modelos ORM
    │   └── repositories/            # Implementación de repositorios
    │       └── __init__.py          # ✅ Repos SQLAlchemy + Mappers
    ├── api/
    │   ├── dependencies/            # FastAPI dependencies
    │   │   └── __init__.py          # ✅ DI para use cases
    │   └── routes/                  # Endpoints
    │       ├── auth.py              # ✅ Rutas de auth
    │       ├── organizations.py     # ⏳ TODO
    │       ├── audits.py            # ⏳ TODO
    │       └── rules.py             # ⏳ TODO
    ├── security/
    │   └── jwt.py                   # ✅ JWT utilities
    └── database.py                  # ✅ Database setup

main.py                              # ✅ Entry point
```

---

## 🎯 Principios de Arquitectura Hexagonal

### ✅ **Separación de capas**
- **Domain**: Lógica de negocio pura (sin dependencias externas)
- **Application**: Casos de uso (orquestación)
- **Infrastructure**: Adaptadores (DB, API, etc.)

### ✅ **Dependency Rule**
```
Infrastructure → Application → Domain
(Externa)        (Casos uso)    (Núcleo)
```
El dominio NO depende de nada. Todo apunta hacia adentro.

### ✅ **Ports & Adapters**
- **Ports**: Interfaces en `domain/repositories/`
- **Adapters**: Implementaciones en `infrastructure/persistence/repositories/`

### ✅ **Dependency Injection**
- Manual usando FastAPI `Depends()`
- Configurado en `infrastructure/api/dependencies/`

---

## 📦 Archivos Creados

He creado **30+ archivos** organizados en arquitectura hexagonal:

### Domain (10 archivos)
- 5 entidades con lógica de negocio
- 5 interfaces de repositorios
- 2 servicios de dominio
- 1 archivo de excepciones

### Application (3 archivos)
- 3 archivos de casos de uso
- 1 archivo de DTOs

### Infrastructure (7 archivos)
- 1 archivo de modelos SQLAlchemy
- 1 archivo de repositorios implementados
- 1 archivo de dependencias
- 1 archivo de JWT
- 1 archivo de database
- 1 ruta de auth
- 1 main.py

---

## 🚀 Cómo Implementar

### Paso 1: Estructura de carpetas

```powershell
cd C:\saas-platform\backend\src

# Elimina todo lo antiguo
Remove-Item -Recurse -Force models, schemas, services, middleware, api 2>$null

# Crea la estructura hexagonal
mkdir domain\entities, domain\repositories, domain\services, domain\exceptions
mkdir application\use_cases, application\dto
mkdir infrastructure\persistence\models, infrastructure\persistence\repositories
mkdir infrastructure\api\dependencies, infrastructure\api\routes
mkdir infrastructure\security
```

### Paso 2: Copiar archivos

Descarga todos los archivos que te compartí y cópialos según esta estructura:

```
domain/entities/ →
  - user.py
  - organization.py
  - audit.py
  - rule.py
  - finding.py
  - __init__.py

domain/repositories/ →
  - user_repository.py
  - organization_repository.py
  - audit_repository.py
  - rule_repository.py
  - finding_repository.py
  - __init__.py

domain/services/ →
  - auth_service.py
  - audit_service.py
  - __init__.py

domain/exceptions/ →
  - __init__.py

application/use_cases/ →
  - register_user.py
  - login_user.py
  - common_use_cases.py
  - __init__.py

application/dto/ →
  - __init__.py

infrastructure/persistence/models/ →
  - __init__.py

infrastructure/persistence/repositories/ →
  - __init__.py

infrastructure/api/dependencies/ →
  - __init__.py

infrastructure/api/routes/ →
  - auth.py

infrastructure/security/ →
  - jwt.py

infrastructure/ →
  - database.py

Raíz (src/) →
  - main.py
```

### Paso 3: Actualizar requirements.txt

```txt
# Ya lo tienes, pero asegúrate de tener:
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

### Paso 4: Levantar Docker

```powershell
cd C:\saas-platform
docker-compose down
docker-compose up --build
```

---

## 🧪 Probar la API

### 1. Accede a la documentación
http://localhost:8000/docs

### 2. Registra un usuario

```bash
POST http://localhost:8000/auth/register
{
  "email": "test@example.com",
  "password": "password123",
  "role": "admin"
}
```

### 3. Login

```bash
POST http://localhost:8000/auth/login
{
  "email": "test@example.com",
  "password": "password123"
}
```

### 4. Get current user

```bash
GET http://localhost:8000/auth/me
Headers: Authorization: Bearer <token>
```

---

## ⏳ Pendiente de Implementar

### Rutas que faltan (puedes crearlas siguiendo el patrón de auth.py):

1. **`infrastructure/api/routes/organizations.py`**
   - POST /organizations
   - GET /organizations
   - GET /organizations/{id}

2. **`infrastructure/api/routes/audits.py`**
   - POST /audits/upload
   - GET /audits
   - GET /audits/{id}
   - POST /audits/{id}/process

3. **`infrastructure/api/routes/rules.py`**
   - POST /rules
   - GET /rules
   - PUT /rules/{id}
   - DELETE /rules/{id}

4. **`infrastructure/api/routes/dashboard.py`**
   - GET /dashboard/metrics

---

## 🎓 Ventajas de esta Arquitectura

✅ **Testeable**: Puedes testear el dominio sin base de datos  
✅ **Mantenible**: Lógica de negocio separada de infraestructura  
✅ **Escalable**: Fácil agregar nuevos adaptadores (GraphQL, gRPC)  
✅ **Independiente**: El dominio no conoce FastAPI ni SQLAlchemy  
✅ **Flexible**: Puedes cambiar DB sin tocar el dominio  

---

## 📚 Cómo Agregar Nuevas Funcionalidades

**Ejemplo: Agregar "Delete Organization"**

1. **Domain**: Ya está (Organization.can_be_deleted())
2. **Repository**: Agregar método a interface
3. **Use Case**: Crear `DeleteOrganizationUseCase`
4. **Route**: Agregar endpoint DELETE /organizations/{id}

Siempre sigue el flujo: Route → Use Case → Repository → Domain

---

## ❓ Dudas Comunes

**P: ¿Por qué tantos archivos?**  
R: Separación de responsabilidades. Cada archivo hace UNA cosa.

**P: ¿No es overkill para un MVP?**  
R: Al principio parece más código, pero escala mejor.

**P: ¿Puedo mezclar con la arquitectura anterior?**  
R: NO. Usa una u otra, no mezcles.

---

## 🚀 Próximos Pasos

1. ✅ Implementar rutas faltantes (organizations, audits, rules)
2. ⏳ CSV parser service
3. ⏳ Background tasks para procesar auditorías
4. ⏳ PDF generation
5. ⏳ Tests unitarios del dominio

---

**¿Listo para implementar? Copia los archivos y levanta Docker!** 🎉
