import base64

def login(username: str, password: str) -> []:
    return [base64.b64encode(username.encode('utf-8')).decode('utf-8'), base64.b64encode(password.encode('utf-8')).decode('utf-8')]