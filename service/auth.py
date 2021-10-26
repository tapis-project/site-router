import jwt
import logging
from service.errors import NoJWTError, InvalidJWTFormatError, InvalidJWTError, JWTNotAuthorizedError
from service import public_key
from service.config import conf


def do_authn(raw_token: str) -> dict:
    """
    check the raw_token value (as derived from X-Tapis-Token header) for a valid JWT; 
    verify the signature and return the token claims as a dictionary if valid.
    """    
    logging.info("top of do_auth")
    if not raw_token:
        raise NoJWTError()
    try:
        data = jwt.decode(raw_token, verify=False)
    except Exception as e:
        raise InvalidJWTFormatError(f"Unable to decode JWT ({e})")
    # check the token type
    token_type = data['tapis/token_type']
    if not token_type == 'access':
        raise InvalidJWTError(f"Invalid token type: {token_type}.")
    # check the signature 
    try:
        claims = jwt.decode(raw_token, public_key)
    except Exception as e:
        raise InvalidJWTError(f"Unable to verify signature on token. Debug data: {e}")
    return claims


def check_can_update(raw_token: str) -> bool:
    """Authn and authz check to determine if a request is authorized to udpate."""
    claims = do_authn(raw_token)
    
    # get the tenant id of the token -- only service tokens running in the same tenant as this site-router can update
    token_tenant_id = claims['tapis/tenant_id']
    if not conf.service_tenant_id == token_tenant_id:
        raise JWTNotAuthorizedError(f"tenant id of the token ({token_tenant_id}) did not match {conf.serivce_tenant_id}")

    # check account type
    token_account_type = claims['tapis/account_type']
    if not token_account_type == 'service':
        raise JWTNotAuthorizedError(f"Only service tokens are authorized.")

    # check the target site
    token_target_site = claims['tapis/target_site']
    if not conf.service_site_id == token_target_site:
        raise JWTNotAuthorizedError(f"target site id of the token ({token_target_site}) did not match {conf.serivce_site_id}")
    
    # check the username -- only tokens api is currently authorized to update.
    token_username = claims['tapis/username']
    if not token_username == 'tokens' and not token_username == 'tenants': # todo -- remove tenants
        raise JWTNotAuthorizedError(f"Only the tokens username is authorized.")

    return True