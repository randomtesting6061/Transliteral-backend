from fastapi import APIRouter, Depends, HTTPException, Request
from services.auth_service import verify_access_token

router = APIRouter()

# @router.get("/profile")
# def get_profile(request: Request):
#     """Protected route that requires authentication via cookies."""
#     user = verify_access_token(request)  # ✅ Read token from cookies

#     if not user:
#         raise HTTPException(status_code=401, detail="Unauthorized. Please log in again.")

#     return {"message": "Welcome to your profile!", "user": user}
