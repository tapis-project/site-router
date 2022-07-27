# site-router
Tapis server deployed at the edge of a site for API routing and basic auth checks


## Basic Usage

Revoke a token (note that is requires a valid JWT representing either the tenants or tokens service, as 
these are the only services allowed to revoke tokens):

```
curl -H "X-tapis-token: $tokens_jwt" localhost:8000/v3/site-router/tokens/revoke -X POST -H "content-type: application/json" -d '{"token": "$some_jwt"}' 
```

Note that the JWT must be valid or attempting to revoke it will result in an error.

Check if a token is revoked:
```
curl -H "X-tapis-token: $some_jwt" localhost:8000/v3/site-router/check
```

## Local Development

A Makefile is included to automate the steps required to build and run the service locally. Check the file for the commands to run. 