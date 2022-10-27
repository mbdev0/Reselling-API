from passlib.context import CryptContext

passcontext = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_pass(password:str) -> str:
    return passcontext.hash(password)

def validate_pass(plain_pass:str,hashed_pass:str) -> bool:
    return passcontext.verify(plain_pass, hashed_pass)