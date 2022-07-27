from pydantic import BaseModel


# ----------------------
# Request Body Models
# ----------------------

class TokenBody(BaseModel):
    token: str


# -----------------------
# Error Response Models
# -----------------------

class ErrorResponse(BaseModel):
    status: str = "error"
    version: str = '0.1.0'
    result: None = None
    metadata: dict = {}
    message: str


# --------------------------
# Success Response Models
# --------------------------

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    version: str = '0.1.0'
    metadata: dict = {}


# ------------------------
# Data Access Objects
# ------------------------
class RevokedTokenDAO(BaseModel):
    raw_jwt: str
    claims: dict

    def save_to_db():
        pass

