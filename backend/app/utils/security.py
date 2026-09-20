from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)

def create_access_token():
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub":"admin","exp":expire}, SECRET_KEY, algorithm=ALGORITHM)
