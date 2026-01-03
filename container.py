from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session
from typing import Protocol, Optional, Dict, List

from database import get_db, User, JobRole, Skill


# Repository Protocols
class UserRepositoryProtocol(Protocol):
    def get_by_userid(self, userid: str, db: Session) -> Optional[User]:
        ...
    
    def create(self, user: User, db: Session) -> bool:
        ...
    
    def authenticate(self, userid: str, password_hash: str, phone: str, db: Session) -> Optional[User]:
        ...


class SkillRepositoryProtocol(Protocol):
    def get_all_job_roles(self, db: Session) -> List[JobRole]:
        ...
    
    def get_skills_by_role(self, role_name: str, db: Session) -> Optional[JobRole]:
        ...


# Service Protocols
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


# Repository Implementations
class UserRepository:
    def get_by_userid(self, userid: str, db: Session) -> Optional[User]:
        return db.query(User).filter(User.userid == userid).first()
    
    def create(self, user: User, db: Session) -> bool:
        try:
            db.add(user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return False
    
    def authenticate(self, userid: str, password_hash: str, phone: str, db: Session) -> Optional[User]:
        return db.query(User).filter(
            User.userid == userid,
            User.password == password_hash,
            User.phone == phone
        ).first()


class SkillRepository:
    def get_all_job_roles(self, db: Session) -> List[JobRole]:
        return db.query(JobRole).all()
    
    def get_skills_by_role(self, role_name: str, db: Session) -> Optional[JobRole]:
        return db.query(JobRole).filter(JobRole.name == role_name).first()


# Service Implementations
class UserService:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self._user_repository = user_repository
    
    def _hash_password(self, password: str) -> str:
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, userid: str, password: str, phone: str, db: Session) -> Optional[User]:
        password_hash = self._hash_password(password)
        return self._user_repository.authenticate(userid, password_hash, phone, db)
    
    def create_user(self, name: str, userid: str, password: str, phone: str, db: Session) -> bool:
        # Check if user already exists
        existing_user = self._user_repository.get_by_userid(userid, db)
        if existing_user:
            return False
        
        # Create new user
        password_hash = self._hash_password(password)
        new_user = User(name=name, userid=userid, password=password_hash, phone=phone)
        return self._user_repository.create(new_user, db)
    
    def get_user_by_userid(self, userid: str, db: Session) -> Optional[User]:
        return self._user_repository.get_by_userid(userid, db)


class SkillService:
    def __init__(self, skill_repository: SkillRepositoryProtocol):
        self._skill_repository = skill_repository
    
    def get_job_roles(self, db: Session) -> List[str]:
        job_roles = self._skill_repository.get_all_job_roles(db)
        return [role.name for role in job_roles]
    
    def get_skills_for_role(self, role: str, db: Session) -> Dict[str, List[str]]:
        job_role = self._skill_repository.get_skills_by_role(role, db)
        if job_role:
            # Group skills by category
            skills_by_category = {}
            for skill in job_role.skills:
                if skill.category not in skills_by_category:
                    skills_by_category[skill.category] = []
                skills_by_category[skill.category].append(skill.name)
            return skills_by_category
        return {}


# Dependency Injection Container
class Container(containers.DeclarativeContainer):
    # Configuration
    config = providers.Configuration()
    
    # Repositories
    user_repository = providers.Factory(UserRepository)
    skill_repository = providers.Factory(SkillRepository)
    
    # Services
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )
    
    skill_service = providers.Factory(
        SkillService,
        skill_repository=skill_repository
    )


# Global container instance
container = Container()