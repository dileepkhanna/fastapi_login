# Job Portal - Clean Architecture with Dependency Injection

A FastAPI application implementing Clean Architecture with proper dependency injection using containers.

## Architecture Overview

### 🏗️ **Clean Architecture Layers**

```
┌─────────────────────────────────────────┐
│                Routes                   │ ← HTTP Layer
├─────────────────────────────────────────┤
│               Services                  │ ← Business Logic
├─────────────────────────────────────────┤
│             Repositories                │ ← Data Access
├─────────────────────────────────────────┤
│               Database                  │ ← Data Layer
└─────────────────────────────────────────┘
```

### 📁 **Project Structure**

```
├── main.py              # FastAPI app setup & DI wiring
├── container.py         # DI Container with all dependencies
├── routes.py           # HTTP route handlers
├── database.py         # Database models & connection
├── templates/          # Jinja2 HTML templates
├── static/            # CSS, JS, images
└── requirements.txt   # Python dependencies
```

## 🔧 **Dependency Injection Implementation**

### **1. Repository Layer**
```python
class UserRepositoryProtocol(Protocol):
    def get_by_userid(self, userid: str, db: Session) -> Optional[User]: ...
    def create(self, user: User, db: Session) -> bool: ...
    def authenticate(self, userid: str, password_hash: str, phone: str, db: Session) -> Optional[User]: ...

class UserRepository:
    # Implementation of data access logic
```

### **2. Service Layer**
```python
class UserServiceProtocol(Protocol):
    def authenticate(self, userid: str, password: str, phone: str, db: Session) -> Optional[User]: ...
    def create_user(self, name: str, userid: str, password: str, phone: str, db: Session) -> bool: ...

class UserService:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self._user_repository = user_repository
    # Business logic implementation
```

### **3. DI Container**
```python
class Container(containers.DeclarativeContainer):
    # Repositories
    user_repository = providers.Factory(UserRepository)
    skill_repository = providers.Factory(SkillRepository)
    
    # Services (with repository injection)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    skill_service = providers.Factory(SkillService, skill_repository=skill_repository)
```

### **4. Route Layer**
```python
@auth_router.post("/login")
@inject
async def login(
    request: Request,
    userid: str = Form(...),
    user_service: UserServiceProtocol = Depends(Provide[Container.user_service]),
    db: Session = Depends(get_db)
):
    # Route handler logic
```

## 🎯 **Benefits of This Architecture**

### **1. Separation of Concerns**
- **Routes**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Repositories**: Handle data access
- **Container**: Manage dependencies

### **2. Testability**
```python
# Easy to mock for testing
container.user_repository.override(providers.Factory(MockUserRepository))
container.user_service.override(providers.Factory(MockUserService))
```

### **3. Maintainability**
- Clear boundaries between layers
- Easy to modify implementations
- Protocol-based interfaces ensure contracts

### **4. Extensibility**
- Add new repositories/services easily
- Swap implementations without changing dependent code
- Configure different environments

## 🚀 **Features**

- **User Authentication**: Login/Signup with session management
- **Job Role Selection**: Browse different job roles
- **Skills Management**: Select skills by category with visual feedback
- **Responsive UI**: Bootstrap-based responsive design
- **Password Security**: SHA256 hashing
- **Session Management**: Secure user sessions

## 📊 **Database Schema**

- **users**: id, name, userid, password, phone, job_role
- **job_roles**: id, name, description
- **skills**: id, name, category, job_role_id
- **user_skills**: Many-to-many relationship table

## 🛠️ **Installation & Setup**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python main.py
```

3. **Access the application:**
```
http://localhost:8002
```

## 🧪 **Testing Credentials**

- **Name**: John Doe
- **User ID**: testuser
- **Password**: test123
- **Phone**: 1234567890

## 🔄 **Dependency Flow**

```
Container → Services → Repositories → Database
    ↓
  Routes (via FastAPI Depends + @inject)
    ↓
HTTP Requests/Responses
```

This architecture ensures loose coupling, high testability, and clean separation of concerns following SOLID principles.