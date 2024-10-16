from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pwd: str):
    return pwd_context.hash(pwd)

def verify_password(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)