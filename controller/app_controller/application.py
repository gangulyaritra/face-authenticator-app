import os
from typing import List
from fastapi import APIRouter, File, Request
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from controller.auth_controller.authentication import get_current_user
from faceapp.user.user_embedding_val import (
    UserLoginEmbeddingValidation,
    UserRegisterEmbeddingValidation,
)

router = APIRouter(
    prefix="/application",
    tags=["application"],
    responses={"401": {"description": "Not Authorized!!!"}},
)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


@router.post("/")
async def login_embedding(
    request: Request, files: List[bytes] = File(description="Upload Multiple Files")
):
    try:
        user = await get_current_user(request)

        if user is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

        user_embedding_validation = UserLoginEmbeddingValidation(user["uuid"])

        # Compare Embeddings.
        user_simmilariy_status = user_embedding_validation.compare_embedding(files)

        if user_simmilariy_status:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": True, "message": "User Authenticated"},
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": "User NOT Authenticated"},
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": False,
                "message": "Error in Login Embedding in Database",
            },
        )


@router.post("/register_embedding")
async def register_embedding(
    request: Request, files: List[bytes] = File(description="Upload Multiple Files")
):
    try:
        # Get the UUID from the session.
        uuid = request.session.get("uuid")

        if uuid is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

        user_embedding_validation = UserRegisterEmbeddingValidation(uuid)

        # Save the Embeddings.
        user_embedding_validation.save_embedding(files)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": True,
                "message": "Embedding Stored Successfully in Database",
            },
            headers={"uuid": uuid},
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": True,
                "message": "Error in Storing Embedding in Database",
            },
        )
