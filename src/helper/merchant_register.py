import base64
import hmac
import hashlib
import secrets
import os
import json
from src.config import config
from src.connect import session
from src.schema.checkout import Checkout
from sqlalchemy import select
from src.models.merchant import Merchants

def register_merchant():
    partner_code = create_partner_code()
    api_key = generate_api_key()
    return { 'partner_code': partner_code, 'api_key': api_key}

async def authorize_merchant(partner_code):
    result = await session.execute(select(Merchants).filter_by(**{'partner_code':partner_code}))
    list = result.fetchall()
    await session.close()
    return True if (len(list) > 0) else False

def create_signature(body, api_key):
    message = json.dumps(body) + api_key
    signature = hmac.new(config.SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    return signature

def create_partner_code():
    partner_code = secrets.token_hex(16)
    return partner_code

# Generate a random API key
def generate_api_key():
    return base64.urlsafe_b64encode(os.urandom(32)).decode()