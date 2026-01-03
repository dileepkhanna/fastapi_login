from database import SessionLocal, User
import hashlib

def test_login():
    db = SessionLocal()
    try:
        # Test credentials
        userid = "testuser"
        password = "test123"
        phone = "1234567890"
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"Input password: {password}")
        print(f"Hashed password: {hashed_password}")
        
        # Query the user
        user = db.query(User).filter(
            User.userid == userid,
            User.password == hashed_password,
            User.phone == phone
        ).first()
        
        if user:
            print(f"✅ Login successful! User: {user.name}")
            print(f"   UserID: {user.userid}")
            print(f"   Phone: {user.phone}")
        else:
            print("❌ Login failed!")
            
            # Check if user exists with userid
            user_by_id = db.query(User).filter(User.userid == userid).first()
            if user_by_id:
                print(f"User exists: {user_by_id.name}")
                print(f"Stored password hash: {user_by_id.password}")
                print(f"Input password hash:  {hashed_password}")
                print(f"Password match: {user_by_id.password == hashed_password}")
                print(f"Phone match: {user_by_id.phone == phone}")
            else:
                print("User not found with this userid")
                
    finally:
        db.close()

if __name__ == "__main__":
    test_login()