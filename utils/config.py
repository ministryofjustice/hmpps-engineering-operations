import os


class Base_Config:
    """This class pulls in environment variables"""

    def __init__(self):
        self.environment_type = os.getenv(
            'TG_ENVIRONMENT_TYPE', default='dev')
