import os
from datetime import datetime
from faceapp.utils import CommonUtils

PIPELINE_NAME = "faceapp"
PIPELINE_ARTIFACT_DIR = os.path.join(os.getcwd(), "artifact")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Authentication Constants.
SECRET_KEY = CommonUtils().get_environment_variable("SECRET_KEY")
ALGORITHM = CommonUtils().get_environment_variable("ALGORITHM")

# Database Constants.
MONGODB_URL_KEY = CommonUtils().get_environment_variable("MONGODB_URL_KEY")
DATABASE_NAME = CommonUtils().get_environment_variable("DATABASE_NAME")
USER_COLLECTION_NAME = CommonUtils().get_environment_variable("USER_COLLECTION_NAME")
EMBEDDING_COLLECTION_NAME = CommonUtils().get_environment_variable(
    "EMBEDDING_COLLECTION_NAME"
)

# Embedding Constants.
EMBEDDING_SIZE = 128
EMBEDDING_TYPE = 1
SIMILARITY_THRESHOLD = 0.75
DETECTOR_BACKEND = "mtcnn"
ENFORCE_DETECTION = False
EMBEDDING_MODEL_NAME = "Facenet"
