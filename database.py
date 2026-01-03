from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.mysql import LONGTEXT

# Database configuration
DATABASE_URL = "mysql+pymysql://root:9948318650@localhost/demo_fast"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship between users and skills
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    userid = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    job_role = Column(String(100), nullable=True)
    
    # Many-to-many relationship with skills
    skills = relationship("Skill", secondary=user_skills, back_populates="users")

# Job Role model
class JobRole(Base):
    __tablename__ = "job_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # One-to-many relationship with skills
    skills = relationship("Skill", back_populates="job_role")

# Skill model
class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # Frontend, Backend, Database, etc.
    job_role_id = Column(Integer, ForeignKey("job_roles.id"))
    
    # Many-to-one relationship with job role
    job_role = relationship("JobRole", back_populates="skills")
    
    # Many-to-many relationship with users
    users = relationship("User", secondary=user_skills, back_populates="skills")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Initialize database with sample data
def init_db():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(JobRole).count() > 0:
            return
        
        # Sample job roles and categorized skills
        job_roles_data = {
            "Full Stack Developer": {
                "Frontend Technologies": ["HTML5", "CSS3", "JavaScript", "React", "Vue.js", "TypeScript"],
                "Backend Technologies": ["Node.js", "Python", "Java", "Express.js", "Django", "Spring Boot"],
                "Database": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
                "DevOps & Tools": ["Docker", "Git", "AWS", "Nginx"]
            },
            "Frontend Developer": {
                "Core Technologies": ["HTML5", "CSS3", "JavaScript", "TypeScript"],
                "Frameworks & Libraries": ["React", "Vue.js", "Angular", "jQuery"],
                "Styling": ["Sass", "Less", "Bootstrap", "Tailwind CSS"],
                "Tools & Build": ["Webpack", "Vite", "npm", "Figma", "Adobe XD"]
            },
            "Backend Developer": {
                "Programming Languages": ["Python", "Java", "Node.js", "C#", "Go", "PHP"],
                "Frameworks": ["Django", "Flask", "Spring Boot", "Express.js", ".NET"],
                "Database": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Oracle"],
                "DevOps & Cloud": ["Docker", "Kubernetes", "AWS", "Azure", "Jenkins"]
            },
            "Data Scientist": {
                "Programming": ["Python", "R", "SQL", "Scala"],
                "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch", "Keras"],
                "Data Analysis": ["Pandas", "NumPy", "Matplotlib", "Seaborn"],
                "Tools & Platforms": ["Jupyter", "Tableau", "Power BI", "Apache Spark"]
            },
            "DevOps Engineer": {
                "Containerization": ["Docker", "Kubernetes", "Podman"],
                "Cloud Platforms": ["AWS", "Azure", "Google Cloud", "DigitalOcean"],
                "CI/CD": ["Jenkins", "GitLab CI", "GitHub Actions", "CircleCI"],
                "Infrastructure": ["Terraform", "Ansible", "Chef", "Puppet"],
                "Monitoring": ["Prometheus", "Grafana", "ELK Stack", "Nagios"]
            }
        }
        
        # Create job roles and categorized skills
        for role_name, categories in job_roles_data.items():
            # Create job role
            job_role = JobRole(name=role_name)
            db.add(job_role)
            db.flush()  # Get the ID
            
            # Create skills for each category
            for category, skills_list in categories.items():
                for skill_name in skills_list:
                    skill = Skill(name=skill_name, category=category, job_role_id=job_role.id)
                    db.add(skill)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()