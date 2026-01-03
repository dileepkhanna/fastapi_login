from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from typing import Protocol, Dict, List, Optional
import uvicorn
import hashlib

from database import get_db, create_tables, init_db, User, JobRole, Skill

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Protocol for dependency injection
class UserServiceProtocol(Protocol):
    def authenticate(self, userid: str, password: str, phone: str, db: Session) -> Optional[User]:
        ...
    
    def create_user(self, name: str, userid: str, password: str, phone: str, db: Session) -> bool:
        ...
    
    def get_user_by_userid(self, userid: str, db: Session) -> Optional[User]:
        ...

class SkillServiceProtocol(Protocol):
    def get_job_roles(self, db: Session) -> List[str]:
        ...
    
    def get_skills_for_role(self, role: str, db: Session) -> Dict[str, List[str]]:
        ...

# Service implementations
class UserService:
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, userid: str, password: str, phone: str, db: Session) -> Optional[User]:
        hashed_password = self._hash_password(password)
        user = db.query(User).filter(
            User.userid == userid,
            User.password == hashed_password,
            User.phone == phone
        ).first()
        return user
    
    def create_user(self, name: str, userid: str, password: str, phone: str, db: Session) -> bool:
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.userid == userid).first()
            if existing_user:
                return False
            
            # Create new user
            hashed_password = self._hash_password(password)
            new_user = User(name=name, userid=userid, password=hashed_password, phone=phone)
            db.add(new_user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return False
    
    def get_user_by_userid(self, userid: str, db: Session) -> Optional[User]:
        return db.query(User).filter(User.userid == userid).first()

class SkillService:
    def get_job_roles(self, db: Session) -> List[str]:
        job_roles = db.query(JobRole).all()
        return [role.name for role in job_roles]
    
    def get_skills_for_role(self, role: str, db: Session) -> Dict[str, List[str]]:
        job_role = db.query(JobRole).filter(JobRole.name == role).first()
        if job_role:
            # Group skills by category
            skills_by_category = {}
            for skill in job_role.skills:
                if skill.category not in skills_by_category:
                    skills_by_category[skill.category] = []
                skills_by_category[skill.category].append(skill.name)
            return skills_by_category
        return {}

# Dependency injection
def get_user_service() -> UserServiceProtocol:
    return UserService()

def get_skill_service() -> SkillServiceProtocol:
    return SkillService()

@app.on_event("startup")
async def startup_event():
    create_tables()
    init_db()

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    userid: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    user_service: UserServiceProtocol = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    print(f"Login attempt - UserID: {userid}, Phone: {phone}, Password: {password[:3]}...")
    user = user_service.authenticate(userid, password, phone, db)
    print(f"Authentication result: {user is not None}")
    if user:
        print(f"User found: {user.name}")
        # Store user info in session
        request.session["user_id"] = user.id
        request.session["user_name"] = user.name
        request.session["userid"] = user.userid
        return RedirectResponse(url="/job-roles", status_code=303)
    else:
        print("Authentication failed")
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid credentials"
        })

@app.post("/signup")
async def signup(
    request: Request,
    name: str = Form(...),
    userid: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    user_service: UserServiceProtocol = Depends(get_user_service),
    db: Session = Depends(get_db)
):
    if user_service.create_user(name, userid, password, phone, db):
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "success": "Account created successfully! Please login."
        })
    else:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "User already exists or registration failed"
        })

@app.get("/job-roles", response_class=HTMLResponse)
async def job_roles_page(
    request: Request,
    skill_service: SkillServiceProtocol = Depends(get_skill_service),
    db: Session = Depends(get_db)
):
    # Check if user is logged in
    user_name = request.session.get("user_name")
    if not user_name:
        return RedirectResponse(url="/", status_code=303)
    
    roles = skill_service.get_job_roles(db)
    return templates.TemplateResponse("job_roles.html", {
        "request": request, 
        "roles": roles,
        "user_name": user_name
    })

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/skills/{role}")
async def get_skills(
    role: str,
    skill_service: SkillServiceProtocol = Depends(get_skill_service),
    db: Session = Depends(get_db)
):
    skills = skill_service.get_skills_for_role(role, db)
    return {"skills": skills}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)