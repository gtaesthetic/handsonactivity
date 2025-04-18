import requests
import json
import datetime

def test_claims_leave():
    """
    Test claims and leave functionality for test users
    """
    # Base URL - modify this if your backend is running on a different port
    BASE_URL = "http://localhost:8000"
    
    # Test users with different roles
    test_users = [
        {
            'email': 'employee@test.com',
            'password': 'employee123',
            'role': 'employee'
        },
        {
            'email': 'hr@test.com',
            'password': 'hr123',
            'role': 'hr'
        }
    ]
    
    # First let's test if the backend is running
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        if response.status_code in [200, 302]:
            print("[SUCCESS] Backend server is running!\n")
        else:
            print(f"[ERROR] Backend server responded with status code {response.status_code}\n")
            return
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Backend server not running at {BASE_URL}")
        print("Please start your Django server with 'python manage.py runserver'\n")
        return
    
    # Login users and get authentication tokens
    tokens = {}
    for user in test_users:
        login_data = {
            "email": user['email'],
            "password": user['password']
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/login/",
                data=json.dumps(login_data),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                tokens[user['email']] = token_data.get('access', '')
                print(f"[SUCCESS] Login successful for {user['email']} (role: {user['role']})")
            else:
                print(f"[ERROR] Login failed for {user['email']}: {response.status_code}")
                print(f"   Response: {response.text}")
                return
        except Exception as e:
            print(f"[ERROR] Error during login for {user['email']}: {str(e)}")
            return
    
    print("\n" + "=" * 50)
    print("TESTING CLAIMS FUNCTIONALITY")
    print("=" * 50)
    
    # 1. Test submitting a claim as employee
    employee_token = tokens.get('employee@test.com')
    hr_token = tokens.get('hr@test.com')
    
    if not employee_token or not hr_token:
        print("[ERROR] Missing tokens for test users")
        return
    
    # Submit a new claim
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    claim_data = {
        "claim_type": "medical",
        "amount": 1500,
        "currency": "PHP",
        "bill_no": "TEST123",
        "bill_date": today.strftime("%Y-%m-%d"),
        "supplier": "Test Hospital",
        "claimant": "Test Employee",
        "claim_date": today.strftime("%Y-%m-%d"),
        "claim_due_date": tomorrow.strftime("%Y-%m-%d"),
        "remarks": "Test claim submission"
    }
    
    print("\nSubmitting a new claim as employee...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/claims/new/",
            data=json.dumps(claim_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {employee_token}"
            }
        )
        
        if response.status_code == 201:
            claim_response = response.json()
            claim_id = claim_response.get('id')
            print(f"[SUCCESS] Claim submitted successfully! Claim ID: {claim_id}")
            
            # 2. Test approving the claim as HR
            print("\nApproving the claim as HR...")
            approve_data = {
                "action": "approve"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/claims/{claim_id}/approve_reject/",
                data=json.dumps(approve_data),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {hr_token}"
                }
            )
            
            if response.status_code == 200:
                print(f"[SUCCESS] Claim approved successfully!")
            else:
                print(f"[ERROR] Failed to approve claim: {response.status_code}")
                print(f"   Response: {response.text}")
        else:
            print(f"[ERROR] Failed to submit claim: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Error testing claim submission/approval: {str(e)}")
    
    print("\n" + "=" * 50)
    print("TESTING LEAVE FUNCTIONALITY")
    print("=" * 50)
    
    # For leave type, we'll use ID 1 since there's no endpoint to fetch leave types
    # Note: If using in production, make sure this ID exists in the database
    leave_type_id = 1
    print(f"\n[INFO] Using leave type ID: {leave_type_id} for testing")
    print("[INFO] Make sure this leave type exists in your database.")
    print("[INFO] If test fails, create a leave type with this ID in the admin panel.")
    
    # Submit a leave request
    start_date = (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    
    leave_data = {
        "leave_type": leave_type_id,
        "start_date": start_date,
        "end_date": end_date,
        "reason": "Test leave request"
    }
    
    print("\nSubmitting a new leave request as employee...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/leaves/submit/",
            data=json.dumps(leave_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {employee_token}"
            }
        )
        
        if response.status_code == 201:
            leave_response = response.json()
            leave_id = leave_response.get('id')
            print(f"[SUCCESS] Leave request submitted successfully! Leave ID: {leave_id}")
            
            # Approve the leave request as HR
            print("\nApproving the leave request as HR...")
            approve_data = {
                "action": "approve"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/leaves/{leave_id}/approve_reject/",
                data=json.dumps(approve_data),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {hr_token}"
                }
            )
            
            if response.status_code == 200:
                print(f"[SUCCESS] Leave request approved successfully!")
            else:
                print(f"[ERROR] Failed to approve leave request: {response.status_code}")
                print(f"   Response: {response.text}")
        else:
            print(f"[ERROR] Failed to submit leave request: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Error testing leave submission/approval: {str(e)}")
    
    # Print overall summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print("These tests attempted to:")
    print("1. Submit a claim as an employee")
    print("2. Approve the claim as HR")
    print("3. Submit a leave request as an employee")
    print("4. Approve the leave request as HR")
    print("\nCheck the console output above for detailed results.")

if __name__ == "__main__":
    print("Testing claims and leave functionality...\n")
    test_claims_leave() 