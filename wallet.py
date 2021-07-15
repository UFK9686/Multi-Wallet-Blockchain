# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os

# Import constants.py and necessary functions from bit and web3
from bit import *
from web3 import Web3
from constants import *
from pathlib import Path
from getpass import getpass
from dotenv import load_dotenv
from eth_account import Account 
from bit.network import NetworkAPI
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from bit import Key, PrivateKey, PrivateKeyTestnet


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Create a function called `derive_wallets`
def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

from pprint import pprint 

# Creates a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST),
}

pprint(coins)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.

def priv_key_to_account(coin, priv_key):
    if coin == 'BTCTEST':
        return PrivateKeyTestnet(priv_key)
    elif coin == 'ETH':
        return Account.privateKeyToAccount(priv_key)
    

eth_PrivateKey = coins["eth"][0]['privkey']
btc_PrivateKey = coins['btc-test'][1]['privkey']
print(eth_PrivateKey)
print(btc_PrivateKey)

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    
eth_acc = priv_key_to_account(ETH,eth_PrivateKey)
btc_acc = priv_key_to_account(BTCTEST,btc_PrivateKey)
print(eth_acc)
print(btc_acc)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    global tx_data
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        tx_data = {
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
        return tx_data

    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)]) 

    
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    if coin == "eth": 
        trx_eth = create_tx(coin,account, recipient, amount)
        sign = account.signTransaction(trx_eth)
        result = w3.eth.sendRawTransaction(sign.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        trx_btctest= create_tx(coin,account,recipient,amount)
        sign_trx_btctest = account.sign_transaction(trx_btctest)
        from bit.network import NetworkAPI
        NetworkAPI.broadcast_tx_testnet(sign_trx_btctest)       
        return sign_trx_btctest
    
    
# create BTC transaction
print(create_tx(BTCTEST,btc_acc,"mkwqRYLAfeoMJnnb5A9WegujdggyBeEPGD", 0.000369))

# send BTC transaction
print(send_tx(BTCTEST,btc_acc,'mkwqRYLAfeoMJnnb5A9WegujdggyBeEPGD',0.000369))

# ETH transactions
#check  balance of the account
w3.eth.getBalance("0x02194a55DDA1B029F70220D53f099F38c629ab36")

# create eth transaction
create_tx(ETH,eth_acc,"0x3dFb64A5AdAe2aDece2E252FE5E889d61Ef75122", 25000000000000000000)

# send eth transaction
send_tx(ETH, eth_acc,"0x3dFb64A5AdAe2aDece2E252FE5E889d61Ef75122", 25000000000000000000)


