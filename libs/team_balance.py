"""

@author: Team Mizogg
"""
import requests
import json
def check_balance(address):
    try:
        response = requests.get(f"https://api.haskoin.com/btc/address/{address}/balance")
        if response.status_code == 200:
            data = response.json()
            confirmed_balance = data.get("confirmed", 0)
            unconfirmed_balance = data.get("unconfirmed", 0)
            tx_count = data.get("txs", 0)
            received = data.get("received", 0)

            # Convert satoshis to BTC
            balance = confirmed_balance / 10**8
            totalSent = unconfirmed_balance / 10**8
            totalReceived = received / 10**8
            return balance, totalReceived, totalSent, tx_count
        else:
            print('API request failed with status code:', response.status_code)
    except json.JSONDecodeError:
        print('Error decoding JSON response from API')