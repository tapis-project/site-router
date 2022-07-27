from typing import SupportsRound, Union
from fastapi import FastAPI, Response, status
from fastapi.params import Header
from jsonschema.validators import meta_schemas
from redis import client
from service.models import TokenBody, ErrorResponse, SuccessResponse
from service.auth import check_can_update, do_authn
from service.config import conf
from service.db import add_token_to_store, check_if_token_revoked, check_db_connectivity

from tapisservice.logs import get_logger
logger = get_logger(__name__)

app = FastAPI()


@app.get('/v3/site-router/hello', response_model=SuccessResponse)
async def hello():
    """
    Basic health check
    """
    return SuccessResponse(message=f'site-router serving site {conf.service_site_id} ready.')

@app.get('/v3/site-router/ready', response_model=SuccessResponse)
async def ready():
    """
    Health check that includes checking communication with db.
    """
    check_db_connectivity()
    return SuccessResponse(message=f'site-router serving site {conf.service_site_id} ready.')


@app.post("/v3/site-router/tokens/revoke", response_model=Union[ErrorResponse, SuccessResponse])
async def revoke_token(token: TokenBody, response: Response, x_tapis_token: str = Header(None)):
    logger.debug("top of /v3/site-router/tokens/revoke")
    try:
        authorized = check_can_update(x_tapis_token)
    except Exception as e:
        response.status_code = e.code
        return ErrorResponse(message=e.msg)
    if not authorized:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return ErrorResponse(message='Not authorized.')
    logger.debug("revoke request is authorized.")
    try:
        claims = do_authn(token.token, check_signature=False)
    except Exception as e:
        response.status_code = e.code
        return ErrorResponse(message=f"The token to be revoked is invalid; additional data: {e.msg}")
    try:
        add_token_to_store(token.token, claims)
    except Exception as e:
        response.status_code = e.code
        return ErrorResponse(message=e.msg)
    return SuccessResponse(message=f"Token {claims['jti']} has been revoked.")


@app.get("/v3/site-router/tokens/check", response_model=Union[ErrorResponse, SuccessResponse])
async def check_token(response: Response, x_tapis_token: str = Header(None)):
    if not x_tapis_token:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponse(message='X-Tapis-Token not found.')
    try:
        is_revoked = check_if_token_revoked(x_tapis_token)
    except Exception as e:
        response.status_code = e.code
        return ErrorResponse(message=f"Could not determine token status; additional data: {e.msg}")
    if is_revoked:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponse(message='X-Tapis-Token is revoked.')
    else:
        return SuccessResponse(message='X-Tapis-Token is not revoked.')


    
