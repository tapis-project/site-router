import requests
from service.config import conf

from tapisservice.logs import get_logger
logger = get_logger(__name__)

# get public key of admin tenant where this site-router runs

url = f'{conf.primary_site_admin_tenant_base_url}/v3/tenants/{conf.service_tenant_id}'
logger.debug(f"site-router initializing, determining public key to use from URL: {url}")
rsp = requests.get(url)
rsp.raise_for_status()

public_key = rsp.json()['result']['public_key']
logger.debug(f"site-router using public key: {public_key}")