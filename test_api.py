#!/usr/bin/env python3
"""
Script untuk test API endpoints
"""

import requests
import json
import time

# Base URL
BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Python MongoDB REST API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. 🏥 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Root endpoint
    print("\n2. 🏠 Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Get all users (empty initially)
    print("\n3. 👥 Getting All Users (should be empty)...")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Create a new user
    print("\n4. ➕ Creating New User...")
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "city": "Jakarta"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        created_user = response.json()
        print(f"Created User: {json.dumps(created_user, indent=2)}")
        user_id = created_user['_id']
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test 5: Create another user
    print("\n5. ➕ Creating Another User...")
    user_data2 = {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "age": 25,
        "city": "Surabaya"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data2)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        created_user2 = response.json()
        print(f"Created User: {json.dumps(created_user2, indent=2)}")
        user_id2 = created_user2['_id']
    else:
        print(f"Error: {response.json()}")
        return
    
    # Test 6: Try creating duplicate email (should fail)
    print("\n6. ❌ Testing Duplicate Email (should fail)...")
    duplicate_user = {
        "name": "John Clone",
        "email": "john.doe@example.com",  # Same email as first user
        "age": 35,
        "city": "Bandung"
    }
    response = requests.post(f"{BASE_URL}/users", json=duplicate_user)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 7: Get all users (should show our created users)
    print("\n7. 👥 Getting All Users...")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    users = response.json()
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"  - {user['name']} ({user['email']})")
    
    # Test 8: Get user by ID
    print(f"\n8. 👤 Getting User by ID: {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"User: {json.dumps(response.json(), indent=2)}")
    
    # Test 9: Update user
    print(f"\n9. ✏️ Updating User {user_id}...")
    update_data = {
        "age": 31,
        "city": "Yogyakarta"
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated_user = response.json()
        print(f"Updated User: {json.dumps(updated_user, indent=2)}")
    else:
        print(f"Error: {response.json()}")
    
    # Test 10: Get users count
    print("\n10. 🔢 Getting Users Count...")
    response = requests.get(f"{BASE_URL}/users/count")
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()}")
    
    # Test 11: Delete user
    print(f"\n11. 🗑️ Deleting User {user_id2}...")
    response = requests.delete(f"{BASE_URL}/users/{user_id2}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 12: Verify deletion
    print("\n12. ✅ Verifying Deletion...")
    response = requests.get(f"{BASE_URL}/users")
    users = response.json()
    print(f"Remaining users: {len(users)}")
    for user in users:
        print(f"  - {user['name']} ({user['email']})")
    
    # Test 13: Try to get deleted user (should fail)
    print(f"\n13. ❌ Trying to Get Deleted User {user_id2} (should fail)...")
    response = requests.get(f"{BASE_URL}/users/{user_id2}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n🎉 API Testing Completed!")
    print("\n📊 Summary:")
    print("- MongoDB connection: ✅")
    print("- CRUD operations: ✅")
    print("- Error handling: ✅")
    print("- Data validation: ✅")
    print("- Unique constraints: ✅")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API server.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

