import requests

def test_server_login():
    url = "http://localhost:8002/login"
    data = {
        "userid": "testuser",
        "password": "test123",
        "phone": "1234567890"
    }
    
    try:
        response = requests.post(url, data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 303:
            print("✅ Login successful - redirecting to job-roles")
        else:
            print("❌ Login failed")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_server_login()