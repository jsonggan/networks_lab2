from fastapi import Response, Header
from typing import Optional

# verify the bearer token
def admin_home(response: Response, authorization: Optional[str] = Header(None)):
    if authorization is None:
        response.status_code = 401
        return {"messsage": "Authorization header missing"}
    
    token_type, _, token = authorization.partition(' ')
    if token_type.lower() != "bearer" or not token:
        response.status_code = 401
        return {"message": "Invalid or missing bearer token"}
    
    # insecure way to include bearer token in this way, but for the simplicity of this project, we don't overcomplicated thing
    if token != "Oo9mzIKFlWiP8JTblDFTc886ysXHexuHADVqU5RMcifjJpyXEOuxP0TIdgQOiVeJ":
        response.status_code = 403
        return {"message": "Invalid token!"}
    
    return {"message": "Welcome admin!"}