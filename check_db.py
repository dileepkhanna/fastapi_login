from database import SessionLocal, User, JobRole, Skill

def check_database():
    """Check database contents"""
    db = SessionLocal()
    try:
        # Check users
        users = db.query(User).all()
        print(f"Users in database: {len(users)}")
        for user in users:
            print(f"  - {user.userid} (Phone: {user.phone})")
        
        # Check job roles
        job_roles = db.query(JobRole).all()
        print(f"\nJob roles in database: {len(job_roles)}")
        for role in job_roles:
            print(f"  - {role.name}")
        
        # Check skills
        skills = db.query(Skill).all()
        print(f"\nSkills in database: {len(skills)}")
        
        # Show skills by job role
        for role in job_roles:
            role_skills = [skill.name for skill in role.skills]
            print(f"\n{role.name} skills: {', '.join(role_skills)}")
            
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database()