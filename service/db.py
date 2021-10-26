import datetime
import json
import logging
from os import O_LARGEFILE
import redis
from service.config import conf
from service.errors import BaseTapisError



def get_redis_connection(db):
    return redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, db=db)


# db access
tokens_store = get_redis_connection(db=conf.redis_token_db)


def add_token_to_store(jwt: str, claims: dict) -> int:
    """
    add a jwt to the tokens store; 
    returns the expiry of the db record.
    """
    expires_at = datetime.datetime.fromtimestamp(claims['exp'], datetime.timezone.utc)
    expires_in = expires_at - datetime.datetime.now(datetime.timezone.utc)
    # set the db ttl to the token ttl plus an additional one hour (3600 seconds) to account for clock skew, etc.
    db_ttl = expires_in.seconds + 3600
    try:
        tokens_store.set(jwt, json.dumps({'claims': claims}), ex=db_ttl)
    except Exception as e:
        logging.error(f"Got exception trying to store record; details: {e}")
        raise BaseTapisError("Unable to save token to database; token has NOT been revoked. Please try request again.")
    return db_ttl


def check_if_token_revoked(jwt: str) -> bool:
    """
    check tokens_store to determine if jwt is present; i.e., has been revoked.
    Returns true if it finds the token (i.e., if the token has been revoked.
    Returns false if the token is not found (i.e., has not been revoked).
    """
    
    try:
        val = tokens_store.get(jwt.encode())
        if val:
            logging.info("found token.")
            return True
        else:
            logging.info("did not find token")
            return False
    except Exception as e:
        logging.critical(f"Got exception trying to check database for expired token. e: {e}")
        # if we cannot check the database for revoked tokens, we must assume ALL tokens are revoked
        # and so we return False here
        return True




users_store = get_redis_connection(db=conf.redis_user_db)


