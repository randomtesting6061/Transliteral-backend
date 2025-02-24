

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from services.auth_service import verify_access_token

def add_auth_middleware(app: FastAPI):
    """JWT Authentication Middleware"""

    @app.middleware("http")
    async def jwt_authentication_middleware(request: Request, call_next):
        """Step 2: Check JWT Token"""
        public_routes = ["/login", "/register", "/docs", "/openapi.json"]

        if request.url.path in public_routes:
            return await call_next(request)  # ✅ Skip authentication for public routes

        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

        token = token.split(" ")[1]  # Extract the actual token
        payload = verify_access_token(token)

        if not payload:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        request.state.user = payload 
        print(payload,'payload this one') # ✅ Attach user info to request
        return await call_next(request)  # ✅ Continue processing
