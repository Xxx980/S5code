from  web3 import  Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8333'))


gasprice = w3.eth.gas_price
print(gasprice)