from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import Request
from app.models.user import User
from app.schemas.user import *
from app.utils.helper_functions import *
from app.utils.oauth import *
from app.database import *

router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def create_user(request: Request,user: UserCreate):

    try:
        with DBFactory() as db:
 
            # password = generate_password()
            hashed_password = hash(user.password)
            # user.password = hashed_password

            new_user = {"email":user.email,"username":user.username,"password_hash":hashed_password,"role":user.role.value}
            response = User.create_user(db,**new_user)
            # db.add(new_user)
            # db.commit()
            # db.refresh(new_user)
        

            return {"message":"User Created Successfully"}
    
    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error



@router.post('/login/', response_model=Token, status_code=status.HTTP_200_OK)
async def login(request: Request,user_credentials: UserLogin):
    try:
        with DBFactory() as db:
            user = db.query(User).filter(
                User.email == user_credentials.email).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

            if not verify(user_credentials.password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


            access_token = create_access_token(data={"user_id": user.id,"role":user.role,"name":user.username,"email_id":user.email})
            refresh_token = create_refresh_token(data={"user_id": user.id})

            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error


@router.post("/refresh/", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(request: Request):
    try:
        refresh_token = request.headers.get("Authorization")
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")
        
        new_access_token = refresh_access_token(refresh_token.split(" ")[1])
        return {"access_token": new_access_token, "refresh_token": refresh_token.split(" ")[1], "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/users/",status_code=status.HTTP_200_OK)
async def get_all_users(current_user: int = Depends(get_current_user)):
    try:
        with DBFactory() as db:
            if current_user.role != "Admin":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            users=User.get_all_users(db)
            list_users=[]
            for user in users:
                user_dic={
                    "id":user.id,
                    "username":user.username,
                    "role":user.role
                }
                list_users.append(user_dic)
            return list_users

    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error