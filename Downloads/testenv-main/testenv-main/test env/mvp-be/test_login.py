import requests
import json

def test_login():
    """
    Test login functionality for all test users
    """
    # Base URL - modify this if your backend is running on a different port
    BASE_URL = "http://localhost:8000"
    
    # Test users
    test_users = [
        {
            'email': 'employee@test.com',
            'password': 'employee123',
            'role': 'employee'
        },
        {
            'email': 'manager@test.com',
            'password': 'manager123',
            'role': 'manager'
        },
        {
            'email': 'hr@test.com',
            'password': 'hr123',
            'role': 'hr'
        },
        {
            'email': 'ceo@test.com',
            'password': 'ceo123',
            'role': 'ceo'
        },
        {
            'email': 'admin@test.com',
            'password': 'admin123',
            'role': 'admin'
        }
    ]
    
    # First let's test if the backend is running
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        if response.status_code in [200, 302]:
            print("[SUCCESS] Backend server is running!\n")
        else:
            print(f"[ERROR] Backend server responded with status code {response.status_code}\n")
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Backend server not running at {BASE_URL}")
        print("Please start your Django server with 'python manage.py runserver'\n")
        return
    
    # Test both login endpoints
    api_endpoints = [
        "/api/login/",  # From users app's urls.py
        "/login/"       # From project urls.py
    ]
    
    all_successful = True
    
    for endpoint in api_endpoints:
        print(f"Testing login endpoint: {endpoint}")
        print("-" * 40)
        
        endpoint_success = False
        
        for user in test_users:
            try:
                login_data = {
                    "email": user['email'],
                    "password": user['password']
                }
                
                response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    data=json.dumps(login_data),
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    print(f"[SUCCESS] Login successful for {user['email']} (role: {user['role']})")
                    print(f"   Access Token: {token_data.get('access', '')[:20]}...")
                    endpoint_success = True
                else:
                    print(f"[ERROR] Login failed for {user['email']}: {response.status_code}")
                    print(f"   Response: {response.text}")
                    all_successful = False
            
            except Exception as e:
                print(f"[ERROR] Error testing login for {user['email']}: {str(e)}")
                all_successful = False
        
        print("\n")
    
    # Print overall summary
    print("=" * 50)
    if all_successful:
        print("[SUCCESS] All login tests passed successfully!")
    else:
        print("[ERROR] Some login tests failed. Please check the output above.")
    print("=" * 50)
    
    # Provide next steps
    print("\nNext steps:")
    if not all_successful:
        print("1. Make sure all test users are created in the database (run create_test_users.py)")
        print("2. Check that your backend server is running")
        print("3. Verify that the role field values in the database match the frontend expectations")
        print("4. Check your login endpoint is correctly implemented in views.py")
    else:
        print("1. Update your frontend API URL to match the working endpoint")
        print("2. Make sure your frontend is sending the right credentials format")
        print("3. Check for CORS issues if you still have problems")

if __name__ == "__main__":
    print("Testing login functionality...\n")
    test_login() 