import requests
from service.config import conf

# get public key of admin tenant where this site-router runs

rsp = requests.get(f'{conf.primary_site_admin_tenant_base_url}/v3/tenants/{conf.service_tenant_id}')
rsp.raise_for_status()

public_key = rsp.json()['result']['public_key']