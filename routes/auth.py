from fastapi import APIRouter, Depends, HTTPException, Response,Request
from fastapi.responses import JSONResponse
from database import SessionLocal
from sqlalchemy.orm import Session
from schema.userschema import Userschemamodel
from models.usermodel import User
from utils.hashing import Hash
from services.auth_service import create_access_token, verify_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: Userschemamodel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user already registered")
    
    user_data = data.dict()
    hashed_password = Hash.bcrypt(data.password)
    user_data['password'] = hashed_password
    new_user = User(**user_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



@router.post("/login")
def loginstuff(data: Userschemamodel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == data.username).first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    is_valid = Hash.verify(data.password, existing_user.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token({"sub": existing_user.username})
    print("Generated Token:", access_token)  # Debugging

    return JSONResponse(content={"access_token": access_token, "message": "Login successful"})



@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response





@router.get("/protected-route")
def protected_route(request: Request):  # ✅ Required to access `request.state.user`
    """Protected route that relies on middleware authentication"""
    
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    print(request.state.user,'huu')

    return {"message": "You are authenticated!", "user": request.state.user}


