"""

@author: Team Mizogg
"""
import requests
import json

def check_xpub(account_extended_public_key):
    try:
        response = requests.get(f'https://api.haskoin.com/btc/xpub/{account_extended_public_key}?derive=normal')
        if response.status_code == 200:
            response_data = response.json()
            balance_info = response_data.get("balance", {})
            confirmed_balance = balance_info.get("confirmed", 0)
            unconfirmed_balance = balance_info.get("unconfirmed", 0)
            received = balance_info.get("received", 0)
            external = response_data["indices"]["external"]

            return confirmed_balance / 10**8, unconfirmed_balance / 10**8, received / 10**8, external
        else:
            self.recoveryFinished.emit(f'Error getting xpub information: {response.status_code}')
    except requests.exceptions.RequestException as e:
        self.recoveryFinished.emit(f'Error sending request for xpub information: {str(e)}')

    # Return 0 if there's any error or if the response is not 200
    return 0, 0, 0, 0
    
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