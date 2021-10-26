class BaseTapisError(Exception):
    """
    Base Tapis error class. All Error types should descend from this class.
    """
    def __init__(self, msg=None, code=400):
        """
        Create a new TapisError object. 
        :param msg: (str) A helpful string
        :param code: (int) The HTTP return code that should be returned 
        """
        self.msg = msg
        self.code = code


class NoJWTError(BaseTapisError):
    """Raised when no Tapis JWT is found on the request."""
    def __init__(self, msg=None, code=400):
        self.msg = "No Tapis JWT found; be sure to set an access token in the X-Tapis-Token header."
        self.code = code


class InvalidJWTFormatError(BaseTapisError):
    """Raised when the Tapis JWT found on the request has an invalid format and/or cannot be parsed."""
    pass


class InvalidJWTError(BaseTapisError):
    """Raised whenever the Tapis JWT found on the request in otherwise invalid (e.g., is expired, of the wrong type, etc)."""
    pass


class JWTNotAuthorizedError(BaseTapisError):
    """Raised whenever the Tapis JWT found on the request has insufficient authorizations."""
    pass