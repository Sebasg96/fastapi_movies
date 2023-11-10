from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from JWTmanager import create_token, validate_token
from fastapi import status, HTTPException

#validation
#Creamos uno clase que hereda de  HTTPBearer de Fastpai, esta clase superior tiene un metodo __call__ que nos ayuda a validar 
# retorna credenciales del metodo 
#creamos la excepcion que lanzara si las credenciales no son validas
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@jep.gov.co':
            raise HTTPException(status_code= 403, detail= 'Credenciales invalidas')