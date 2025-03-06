import json
from asyncio import wait_for

from web3 import Web3


w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b6bf7d3508c941499b10025c0776eaf8'))
print(w3.is_connected())
# print(w3.eth.get_block_number())


def main():
    contract_Address = Web3.to_checksum_address('0xdAC17F958D2ee523a2206206994597C13D831ec7')
    with open("usdt_abi.json", "r") as f:
        abi = json.load(f)
    latest_block = w3.eth.get_block_number()


    contract = w3.eth.contract(contract_Address, abi=abi)
    event = contract.events.Transfer().get_logs(from_block=latest_block,to_block = int(latest_block) + 1000)
    # print(event)
    data =[]
    for logs in event:
        address = logs['args']['from']
        to  = logs['args']['to']
        value = logs['args']['value']
        hash = logs['transactionHash']
        data.append([address, to, value, hash])
        # print(address, to, value, hash.hex())
    print(data)


if __name__ == '__main__':
    main()



