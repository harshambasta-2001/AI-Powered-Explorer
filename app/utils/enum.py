from enum import Enum
from datetime import timedelta

class UserRole(Enum):
    ADMIN="Admin"
    USER="User"

class ContentType(Enum):
    SEARCH="search"
    IMAGE="image"


    
