from passlib.context import CryptContext


#Run this in terminal:
# openssl rand -hex 32 to get key

KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINS = 60
passcontext = CryptContext(schemes=['bcrypt'],deprecated="auto")
