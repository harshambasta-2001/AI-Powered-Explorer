from fastapi import FastAPI
# from slowapi.errors import RateLimitExceeded
# from app.core.limiter import limiter, rate_limit_exceeded_handler
from app.routes import user as user_router
from app.routes import task as task_router
from app.database import Base
import re

# from config.settings import get_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

class RegexCORSMiddleware(CORSMiddleware):
    def is_allowed_origin(self, origin: str) -> bool:
        for pattern in self.allow_origins:
            if re.fullmatch(pattern, origin):
                return True
        return False


allowed_origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://192.168.0.113:3000",
]

app.add_middleware(
    RegexCORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(task_router.router, prefix="/dashboard", tags=["task"])