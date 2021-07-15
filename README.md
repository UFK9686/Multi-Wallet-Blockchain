# Multi-Wallet-Blockchain
Homework-19

The hd derive wallet is useful in creating one single master key, your BIP39 seed, which then enables you to create multiple child wallets across multiple blockchain networks, to essentially create wallets for all the coins. Generating a single mnemonic keyphrase using https://iancoleman.io/bip39/ website allows you to accomplish this. After you generate your nmenonic key, you simply store it along with your BIP39 seed whenever you want to access your master wallet. Then, you specify the coin type/network, and choose the BIP44 derivation path which will create a list of child wallets for you to work in under the chosen coin network. 

## The following python function was used to create 3 child wallet addresses for each ETH and BTC-test using hd-derive. See screenshot for wallet information.

def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

![Screenshot (19)](https://user-images.githubusercontent.com/79285543/125849289-7916c71a-5d89-46ca-bfc3-fd7c8f32f5bb.png)



## The following code was used to create a function that prepares the transactions:

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
        
## The following code was used to create a function that is ready to deploy the transaction:

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
        
        
## The following codes successfully executed the transfer of 0.000369 BTC from the second generated child wallet (index 1 btc-test) to the first wallet (index 0 btc-test). See screenshot for successful transfer.

print(create_tx(BTCTEST,btc_acc,"mkwqRYLAfeoMJnnb5A9WegujdggyBeEPGD", 0.000369))
print(send_tx(BTCTEST,btc_acc,'mkwqRYLAfeoMJnnb5A9WegujdggyBeEPGD',0.000369))

![Screenshot (20)](https://user-images.githubusercontent.com/79285543/125849349-19ebaeae-f1ff-45fb-99dd-a036514250b0.png)


## The following codes successfully executed the transfer of 25 ETH from the first generated child wallet (index 0 eth) to the second wallet (index 1 eth). See screenshot for successful transfer.

create_tx(ETH,eth_acc,"0x3dFb64A5AdAe2aDece2E252FE5E889d61Ef75122", 25000000000000000000)
send_tx(ETH, eth_acc,"0x3dFb64A5AdAe2aDece2E252FE5E889d61Ef75122", 25000000000000000000)

![Screenshot (21)](https://user-images.githubusercontent.com/79285543/125849465-2405a5f7-6094-4acc-bece-83d83e0a3d54.png)
