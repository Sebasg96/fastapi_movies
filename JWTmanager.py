from jwt import encode, decode

def create_token(data: dict):
    token : str = encode(payload=data, key='test_key',algorithm='HS256')
    return token 

def validate_token(token:str):
    data : dict = decode(token, key='test_key', algorithms=['HS256'])
    return data