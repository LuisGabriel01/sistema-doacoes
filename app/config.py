import os

class Config:
    DEBUG = True
    DATABASE_FILENAME = 'project.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_FILENAME}'
    MOCK_DIR = 'mock_data'

    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    # Generate a good salt for password hashing using: secrets.SystemRandom().getrandbits(128)
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    # Don't worry if email has findable domain
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}