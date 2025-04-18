import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MVPDECK.settings')
django.setup()

from users.models import User

def create_test_users():
    """
    Create test users that match the ones in the frontend authStore.js
    """
    test_users = [
        {
            'email': 'employee@test.com',
            'password': 'employee123',
            'first_name': 'John',
            'last_name': 'Employee',
            'role': 'employee'
        },
        {
            'email': 'manager@test.com',
            'password': 'manager123',
            'first_name': 'Sarah',
            'last_name': 'Manager',
            'role': 'manager'
        },
        {
            'email': 'hr@test.com',
            'password': 'hr123',
            'first_name': 'Bob',
            'last_name': 'HR',
            'role': 'hr'
        },
        {
            'email': 'ceo@test.com',
            'password': 'ceo123',
            'first_name': 'David',
            'last_name': 'CEO',
            'role': 'ceo'
        },
        {
            'email': 'admin@test.com',
            'password': 'admin123',
            'first_name': 'Alice',
            'last_name': 'Admin',
            'role': 'admin'
        }
    ]

    # Keep track of created users
    created_users = []
    existing_users = []

    for user_data in test_users:
        email = user_data['email']
        
        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            existing_users.append(email)
            continue
            
        # Create the user
        try:
            user = User.objects.create_user(
                email=email,
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            # Update leave balances after creation
            user.annual_leave_balance = 14
            user.sick_leave_balance = 10
            user.save()
            
            created_users.append(email)
            print(f"Created user: {email} with role: {user_data['role']}")
        except Exception as e:
            print(f"Error creating user {email}: {str(e)}")

    # Print summary
    if created_users:
        print(f"\nSuccessfully created {len(created_users)} users:")
        for email in created_users:
            print(f"- {email}")
    
    if existing_users:
        print(f"\nSkipped {len(existing_users)} existing users:")
        for email in existing_users:
            print(f"- {email}")
    
    if not created_users and not existing_users:
        print("No users were created or found.")

if __name__ == "__main__":
    print("Creating test users...")
    create_test_users()
    print("\nDone!") 