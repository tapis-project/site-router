from tabnanny import check
import jwt
import logging
from service.errors import NoJWTError, InvalidJWTFormatError, InvalidJWTError, JWTNotAuthorizedError
from service import public_key
from service.config import conf

from tapisservice.logs import get_logger
logger = get_logger(__name__)


def do_authn(raw_token: str, check_signature: bool = True) -> dict:
    """
    Check the raw_token value (as derived from X-Tapis-Token header) for a valid JWT; 
    Verifies the signature, unless check_signature is set to false.
    Returns the token claims as a dictionary if valid.
    """    
    logging.info("top of do_auth")
    if not raw_token:
        raise NoJWTError()
    try:
        data = jwt.decode(raw_token, verify=False)
    except Exception as e:
        raise InvalidJWTFormatError(f"Unable to decode JWT ({e})")
    # check the signature 
    if not check_signature:
        return data
    try:
        claims = jwt.decode(raw_token, public_key)
    except Exception as e:
        raise InvalidJWTError(f"Unable to verify signature on x-tapis-token. Debug data: {e}")
    return claims


def check_can_update(raw_token: str) -> bool:
    """Authn and authz check to determine if a request is authorized to revoke a token."""
    claims = do_authn(raw_token)
    
    # get the tenant id of the token -- only service tokens running in the same tenant as this site-router can update
    token_tenant_id = claims['tapis/tenant_id']
    if not conf.service_tenant_id == token_tenant_id:
        raise JWTNotAuthorizedError(f"tenant id of the token ({token_tenant_id}) did not match {conf.service_tenant_id}")

    # check account type
    token_account_type = claims['tapis/account_type']
    if not token_account_type == 'service':
        raise JWTNotAuthorizedError(f"Only service tokens are authorized.")

    # check the target site
    token_target_site = claims['tapis/target_site']
    if not conf.service_site_id == token_target_site:
        raise JWTNotAuthorizedError(f"target site id of the token ({token_target_site}) did not match {conf.service_site_id}")
    
    # check the username -- only tokens and tenants api's are currently authorized to revoke a token
    token_username = claims['tapis/username']
    if not token_username == 'tokens' and not token_username == 'tenants': 
        logger.warn(f"subject {token_username} tried to revoke a token!")
        raise JWTNotAuthorizedError(f"Only the tokens username is authorized.")

    return True