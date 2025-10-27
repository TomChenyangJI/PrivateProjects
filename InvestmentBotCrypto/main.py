"""
https://api-gcp.binance.com
https://api1.binance.com
https://api2.binance.com
https://api3.binance.com
https://api4.binance.com
"""
base_url = "https://api.binance.com"

# !/usr/bin/env python3

import base64
import time

import requests
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Set up authentication
API_KEY = '{API_KEY_PLACEHOLDER}'
PRIVATE_KEY_PATH = 'private_key.pem'
#
# # Load the private key.
# # In this example the key is expected to be stored without encryption,
# # but we recommend using a strong password for improved security.
with open(PRIVATE_KEY_PATH, 'rb') as f:
    private_key = load_pem_private_key(data=f.read(),
                                       password=None)


# Set up the request parameters
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': '1.0000000',
    'price': '0.20',
}

# Timestamp the request
timestamp = int(time.time() * 1000)  # UNIX timestamp in milliseconds
params['timestamp'] = timestamp

# Sign the request
payload = '&'.join([f'{param}={value}' for param, value in params.items()])
# signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
params['signature'] = signature

# Send the request
headers = {
    'X-MBX-APIKEY': API_KEY,
}
response = requests.post(
    'https://api.binance.com/api/v3/order',
    headers=headers,
    data=params,
)
print(response.json())
