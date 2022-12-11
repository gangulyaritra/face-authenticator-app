import os
import yaml
from datetime import datetime
from dateutil.parser import parse
from dotenv import dotenv_values


class CommonUtils:
    def read_yaml_file(self, file_path: str) -> dict:
        # Read a YAML file and returns the contents as a dictionary.
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    def get_time(self):
        # Return Current Time.
        return datetime.now().strftime("%H:%M:%S").__str__()

    def get_date(self):
        # Return Current Date.
        return datetime.now().date().__str__()

    def get_difference_in_second(self, future_date_time: str, past_date_time: str):
        future_date = parse(future_date_time)
        past_date = parse(past_date_time)
        difference = future_date - past_date
        total_seconds = difference.total_seconds()
        return total_seconds

    def get_difference_in_milisecond(self, future_date_time: str, past_date_time: str):
        total_seconds = self.get_difference_in_second(future_date_time, past_date_time)
        return total_seconds * 1000

    def get_environment_variable(self, variable_name: str):
        # Return Environment Variables.
        if os.environ.get(variable_name) is not None:
            return os.environ.get(variable_name)
        enironment_variable = dotenv_values(".env")
        return enironment_variable[variable_name]
