import io
import sys
import numpy as np
from ast import Bytes
from typing import List
from PIL import Image
from deepface import DeepFace
from deepface.commons.functions import detect_face

from faceapp.constant import (
    DETECTOR_BACKEND,
    EMBEDDING_MODEL_NAME,
    ENFORCE_DETECTION,
    SIMILARITY_THRESHOLD,
)
from faceapp.data_access.user_embedding_data import UserEmbeddingData
from faceapp.exception import AppException
from faceapp.logger import logging


class UserLoginEmbeddingValidation:
    def __init__(self, uuid_: str) -> None:
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()
        self.user = self.user_embedding_data.get_user_embedding(uuid_)

    def validate(self) -> bool:
        try:
            if self.user["UUID"] is None:
                return False
            return self.user["user_embed"] is not None
        except Exception as e:
            raise e

    @staticmethod
    def generate_embedding(img_array: np.ndarray) -> np.ndarray:
        try:
            # Generate embedding from the image array.
            faces = detect_face(
                img_array,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=ENFORCE_DETECTION,
            )
            # Generate embedding from the face.
            return DeepFace.represent(
                img_path=faces[0],
                model_name=EMBEDDING_MODEL_NAME,
                enforce_detection=False,
            )
        except Exception as e:
            raise AppException(e, sys) from e

    @staticmethod
    def generate_embedding_list(files: List[Bytes]) -> List[np.ndarray]:
        # Generate an embedding list from an image array.
        embedding_list = []
        for contents in files:
            img = Image.open(io.BytesIO(contents))
            # Read the image array.
            img_array = np.array(img)
            # Detect faces.
            embed = UserLoginEmbeddingValidation.generate_embedding(img_array)
            embedding_list.append(embed)
        return embedding_list

    @staticmethod
    def average_embedding(embedding_list: List[np.ndarray]) -> List:
        # Function to calculate the average embedding of the list of embeddings.
        avg_embed = np.mean(embedding_list, axis=0)
        return avg_embed.tolist()

    @staticmethod
    def cosine_simmilarity(db_embedding, current_embedding) -> bool:
        # Function to calculate cosine similarity between two embeddings.
        try:
            return np.dot(db_embedding, current_embedding) / (
                np.linalg.norm(db_embedding) * np.linalg.norm(current_embedding)
            )
        except Exception as e:
            raise AppException(e, sys) from e

    def compare_embedding(self, files: bytes) -> bool:
        try:
            if self.user:
                logging.info("Validating User Embedding.....")
                if self.validate() == False:
                    return False
                logging.info("Embedding Validation Successful.")

                logging.info("Generating Embedding List.....")
                embedding_list = UserLoginEmbeddingValidation.generate_embedding_list(
                    files
                )
                logging.info("Embedding List Generated.")

                logging.info("Calculating Average Embedding.....")
                avg_embedding_list = UserLoginEmbeddingValidation.average_embedding(
                    embedding_list
                )
                logging.info("Average Embedding Calculated.")

                # Get Embedding from the Database.
                db_embedding = self.user["user_embed"]

                logging.info("Calculating Cosine Similarity.....")
                simmilarity = UserLoginEmbeddingValidation.cosine_simmilarity(
                    db_embedding, avg_embedding_list
                )
                logging.info("Cosine Similarity Calculated.")

                if simmilarity >= SIMILARITY_THRESHOLD:
                    logging.info("User Authenticated Successfully.")
                    return True
                else:
                    logging.info("User Authentication Failed.")
                    return False

            logging.info("User Authentication Failed.")
            return False

        except Exception as e:
            raise AppException(e, sys) from e


class UserRegisterEmbeddingValidation:
    def __init__(self, uuid_: str) -> None:
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()

    def save_embedding(self, files: bytes):
        try:
            embedding_list = UserLoginEmbeddingValidation.generate_embedding_list(files)
            avg_embedding_list = UserLoginEmbeddingValidation.average_embedding(
                embedding_list
            )
            self.user_embedding_data.save_user_embedding(self.uuid_, avg_embedding_list)

        except Exception as e:
            raise AppException(e, sys) from e
