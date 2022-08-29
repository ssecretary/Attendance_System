import time
import jwt
from decouple import config
from typing import Dict

JWT_SECRET = config("secret")
JWT_ALGORITHM = config('algorithm')

def token_response(token:str):
    return {
        "access_token":token
    }

def signJWT(id:str) -> Dict[str,str]:
    payload={
        "user_id":id,
        "expires":time.time()+300
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token:str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as ex:
        return {"Error":str(ex)}