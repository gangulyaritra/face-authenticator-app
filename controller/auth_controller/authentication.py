from typing import Optional
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse
from fastapi import HTTPException, status, APIRouter, Request, Response

from faceapp.entity.user import User
from faceapp.user.user_val import RegisterValidation, LoginValidation
from faceapp.constant import SECRET_KEY, ALGORITHM


class Login(BaseModel):
    email_id: str
    password: str


class Register(BaseModel):
    Name: str
    username: str
    email_id: str
    ph_no: int
    password1: str
    password2: str


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


async def get_current_user(request: Request):
    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        uuid: str = payload.get("sub")
        username: str = payload.get("username")

        if uuid is None or username is None:
            return logout(request)
        return {"uuid": uuid, "username": username}

    except JWTError as e:
        raise HTTPException(status_code=404, detail="Details Not Found") from e

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Error while fetching Current User"},
        )


def create_access_token(
    uuid: str, username: str, expires_delta: Optional[timedelta] = None
) -> str:
    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        encode = {"sub": uuid, "username": username, "exp": expire}
        return jwt.encode(encode, secret_key, algorithm=algorithm)

    except Exception as e:
        raise e


@router.post("/token")
async def login_for_access_token(response: Response, login) -> dict:
    try:
        user_validation = LoginValidation(login.email_id, login.password)
        user: Optional[str] = user_validation.authenticate_user_login()

        if not user:
            return {"status": False, "uuid": None, "response": response}

        token_expires = timedelta(minutes=15)
        token = create_access_token(
            user["UUID"], user["username"], expires_delta=token_expires
        )
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"status": True, "uuid": user["UUID"], "response": response}

    except Exception as e:
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Failed to set the access token"},
        )
        return {"status": False, "uuid": None, "response": response}


@router.get("/", response_class=JSONResponse)
async def authentication_page(request: Request):
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Authentication Page"}
        )

    except Exception as e:
        raise e


@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    try:
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Login Successful"}
        )
        token_response = await login_for_access_token(response=response, login=login)
        if not token_response["status"]:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": "Incorrect Username and Password"},
            )
        response.headers["uuid"] = token_response["uuid"]
        return response

    except HTTPException:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": "UnKnown Error"},
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": "User NOT Found"},
        )


@router.get("/register", response_class=JSONResponse)
async def authentication_page(request: Request):
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Registration Page"}
        )

    except Exception as e:
        raise e


@router.post("/register", response_class=JSONResponse)
async def register_user(request: Request, register: Register):
    try:
        name = register.Name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # Add UUID to the session.
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_

        # Validation of the user input data to check the format of the data.
        user_registration = RegisterValidation(user)

        validate_regitration = user_registration.validate_registration()

        if not validate_regitration["status"]:
            msg = validate_regitration["msg"]
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )

        # Save the user if the validation is successful.
        validation_status = user_registration.authenticate_user_registration()

        msg = "Registration Successful..... Please Login to continue"
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )

    except Exception as e:
        raise e


@router.get("/logout")
async def logout(request: Request):
    try:
        msg = "Logout Successful"
        response = RedirectResponse(
            url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg}
        )
        response.delete_cookie(key="access_token")
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": True, "message": msg}
        )
        return response

    except Exception as e:
        raise e
