# site-router
Lightweight Tapis server deployed at the edge of a site for API routing and basic auth checks


## Basic Usage

Revoke a token:

```
curl -H "X-tapis-token: $tokens_jwt" localhost:8000/v3/site-router/tokens/revoke -X POST -d "content-type: application/json" -d '{"token": "$some_jwt"}' 
```


Check if a token is revoked:
```
curl -H "X-tapis-token: $some_jwt" localhost:8000/v3/site-router/check
```
