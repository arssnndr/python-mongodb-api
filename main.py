from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
import os
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from database import db
from models import UserModel, UserUpdate, UserResponse

# Initialize FastAPI app
app = FastAPI(
    title="Python MongoDB REST API",
    description="A simple REST API with CRUD operations using FastAPI and MongoDB",
    version="1.0.0"
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    success = db.connect()
    if not success:
        raise Exception("Failed to connect to database")
    
    # Create unique index on email field
    collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
    collection.create_index("email", unique=True)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    db.close_connection()

# Helper function to format user data
def format_user(user) -> dict:
    """Format user data for response"""
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"],
        "city": user.get("city")
    }

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Python MongoDB REST API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )

# CREATE - Add new user
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel):
    """Create a new user"""
    try:
        collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
        
        # Convert to dict and remove the id field for insertion
        user_dict = user.dict(by_alias=True, exclude_unset=True)
        if "_id" in user_dict:
            del user_dict["_id"]
        
        # Insert user
        result = collection.insert_one(user_dict)
        
        # Get the created user
        created_user = collection.find_one({"_id": result.inserted_id})
        
        return format_user(created_user)
        
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

# READ - Get all users
@app.get("/users", response_model=List[UserResponse])
async def get_all_users(skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    try:
        collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
        
        users = list(collection.find().skip(skip).limit(limit))
        
        return [format_user(user) for user in users]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )

# READ - Get user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a user by ID"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
        
        user = collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return format_user(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )

# UPDATE - Update user by ID
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update a user by ID"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
        
        # Get update data (exclude unset fields)
        update_data = user_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Update user
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get updated user
        updated_user = collection.find_one({"_id": ObjectId(user_id)})
        
        return format_user(updated_user)
        
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

# DELETE - Delete user by ID
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user by ID"""
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
        
        # Delete user
        result = collection.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )

# GET users count
@app.get("/users/count")
async def get_users_count():
    """Get total count of users"""
    try:
        collection = db.get_collection(os.getenv("COLLECTION_NAME", "users"))
        count = collection.count_documents({})
        return {"count": count}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error counting users: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

