import sys
import re
from typing import Optional
from passlib.context import CryptContext

from faceapp.data_access.user_data import UserData
from faceapp.entity.user import User
from faceapp.exception import AppException
from faceapp.logger import logging

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginValidation:
    def __init__(self, email_id: str, password: str):
        self.email_id = email_id
        self.password = password
        self.regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

    def validate(self) -> bool:
        # This function validates the user input.
        try:
            msg = ""
            if not self.email_id:
                msg += "Email Id is required"
            if not self.password:
                msg += "Password is required"
            if not self.is_email_valid():
                msg += "Invalid Email Id"
            return msg

        except Exception as e:
            raise e

    def is_email_valid(self) -> bool:
        return bool(re.fullmatch(self.regex, self.email_id))

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt_context.verify(plain_password, hashed_password)

    def validate_login(self) -> dict:
        # This function checks all the validation conditions for user registration.
        if len(self.validate()) != 0:
            return {"status": False, "msg": self.validate()}
        return {"status": True}

    def authenticate_user_login(self) -> Optional[str]:
        # This function authenticates the user and returns the token.
        try:
            logging.info("Authenticating User Details.....")
            if self.validate_login()["status"]:
                userdata = UserData()
                logging.info("Fetching User Details from Database.....")
                user_login_val = userdata.get_user({"email_id": self.email_id})
                if not user_login_val:
                    logging.info("User NOT FOUND while Login")
                    return False
                if not self.verify_password(self.password, user_login_val["password"]):
                    logging.info("Incorrect Password.")
                    return False
                logging.info("User Authenticated Successfully.")
                return user_login_val
            return False

        except Exception as e:
            raise AppException(e, sys) from e


class RegisterValidation:
    """
    This function authenticates the user and returns the status.
    """

    def __init__(self, user: User) -> None:
        try:
            self.user = user
            self.regex = re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            )
            self.uuid = self.user.uuid_
            self.userdata = UserData()
            self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        except Exception as e:
            raise e

    def validate(self) -> bool:
        # This function checks all the validation conditions for user registration.
        try:
            msg = ""
            if self.user.Name is None:
                msg += "Enter Name"

            if self.user.username is None:
                msg += "Enter Username"

            if self.user.email_id is None:
                msg += "Enter Email ID"

            if self.user.ph_no is None:
                msg += "Enter Phone Number"

            if self.user.password1 is None:
                msg += "Enter Password"

            if self.user.password2 is None:
                msg += "Re-enter Password"

            if not self.is_email_valid():
                msg += "Invalid Email"

            if not self.is_password_valid():
                msg += "Password length should be between 8 and 16"

            if not self.is_password_match():
                msg += "Password does not match"

            if not self.is_details_exists():
                msg += "User already exists"

            return msg

        except Exception as e:
            raise e

    def is_email_valid(self) -> bool:
        return bool(re.fullmatch(self.regex, self.user.email_id))

    def is_password_valid(self) -> bool:
        return len(self.user.password1) >= 8 and len(self.user.password2) <= 16

    def is_password_match(self) -> bool:
        return self.user.password1 == self.user.password2

    def is_details_exists(self) -> bool:
        username_val = self.userdata.get_user({"username": self.user.username})
        emailid_val = self.userdata.get_user({"email_id": self.user.email_id})
        uuid_val = self.userdata.get_user({"UUID": self.uuid})
        return username_val is None and emailid_val is None and uuid_val is None

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt_context.hash(password)

    def validate_registration(self) -> bool:
        # This function checks all the validation conditions for user registration.
        if len(self.validate()) != 0:
            return {"status": False, "msg": self.validate()}
        return {"status": True}

    def authenticate_user_registration(self) -> bool:
        # This function saves the user details in the database only after validating the user details.
        try:
            logging.info("Validating the user details during Registration.....")
            if self.validate_registration()["status"]:
                logging.info("Generating the Password Hash.....")
                hashed_password: str = self.get_password_hash(self.user.password1)
                user_data_dict: dict = {
                    "Name": self.user.Name,
                    "username": self.user.username,
                    "password": hashed_password,
                    "email_id": self.user.email_id,
                    "ph_no": self.user.ph_no,
                    "UUID": self.uuid,
                }
                logging.info("Saving User Details in the Database.....")
                self.userdata.save_user(user_data_dict)
                logging.info("Saved User Details in the Database.")
                return {"status": True, "msg": "User Registered Successfully"}

            logging.info("Validation Failed during Registration.")
            return {"status": False, "msg": self.validate()}

        except Exception as e:
            raise e
