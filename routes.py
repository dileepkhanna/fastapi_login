from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide

from database import get_db
from container import Container, UserServiceProtocol, SkillServiceProtocol

# Templates
templates = Jinja2Templates(directory="templates")

# Create routers
auth_router = APIRouter()
job_router = APIRouter()
api_router = APIRouter(prefix="/api")


@auth_router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
@inject
async def login(
    request: Request,
    userid: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    user_service: UserServiceProtocol = Depends(Provide[Container.user_service]),
    db: Session = Depends(get_db)
):
    user = user_service.authenticate(userid, password, phone, db)
    
    if user:
        # Store user info in session
        request.session["user_id"] = user.id
        request.session["user_name"] = user.name
        request.session["userid"] = user.userid
        return RedirectResponse(url="/job-roles", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid credentials"
        })


@auth_router.post("/signup")
@inject
async def signup(
    request: Request,
    name: str = Form(...),
    userid: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    user_service: UserServiceProtocol = Depends(Provide[Container.user_service]),
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


@auth_router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@job_router.get("/job-roles", response_class=HTMLResponse)
@inject
async def job_roles_page(
    request: Request,
    skill_service: SkillServiceProtocol = Depends(Provide[Container.skill_service]),
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


@api_router.get("/skills/{role}")
@inject
async def get_skills(
    role: str,
    skill_service: SkillServiceProtocol = Depends(Provide[Container.skill_service]),
    db: Session = Depends(get_db)
):
    skills = skill_service.get_skills_for_role(role, db)
    return {"skills": skills}