from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth ,userprofile 
from middleware.auth_middleware import add_auth_middleware # Import other route modules as needed

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI app
app = FastAPI()
add_auth_middleware(app)


# ✅ CORS Configuration (Allow Frontend to Access Backend)
origins = [
    "http://localhost:3000",
      "http://localhost:3001",  # React Frontend (Development)
    "http://127.0.0.1:3000",
    "https://yourfrontend.com"  # Add production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Adjust for production
    allow_credentials=True,  # ✅ Must be `True` for cookies to work
    allow_methods=["*"],
    allow_headers=["*"],
)
# ✅ Include API Routes
app.include_router(auth.router)
app.include_router(userprofile.router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI with CORS Enabled"}
