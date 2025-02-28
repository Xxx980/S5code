import asyncio

from eth_hash.backends.pycryptodome import keccak256
from web3 import Web3
import web3.eth
from web3 import AsyncWeb3, WebSocketProvider
from web3.utils.subscriptions import (
    NewHeadsSubscription,
    NewHeadsSubscriptionContext,
    LogsSubscription,
    LogsSubscriptionContext,
)


# -- declare handlers --
async def new_heads_handler(
        handler_context: NewHeadsSubscriptionContext,
) -> None:
    # 获取区块头
    header = handler_context.result

    # 提取区块高度 (number) 和 区块哈希 (hash)
    block_number = header.get("number", "N/A")
    block_hash = header.get("hash", "N/A")

    # 打印区块高度和区块哈希
    print(f"New Block:\n  - Height: {int(block_number,16)}\n  - Hash: {block_hash}\n")


async def log_handler(
        handler_context: LogsSubscriptionContext,
) -> None:
    log_receipt = handler_context.result

    from_address = Web3.to_checksum_address("0x" + log_receipt["topics"][1].hex()[24:])  # 获取发送方地址
    to_address = Web3.to_checksum_address("0x" + log_receipt["topics"][2].hex()[24:])  # 获取接收方地址
    value = int(log_receipt["data"].hex(), 16)  # 转账金额（以 Wei 为单位）
    print(f"USDC Transfer received - From: {from_address}  - To: {to_address}  - Value: {value / 10 ** 6} USDC")

# -- manage subscriptions --
async def sub_manager():
    # Initialize provider
    w3 = await AsyncWeb3(WebSocketProvider("wss://ethereum-rpc.publicnode.com"))


    try:
        await w3.subscription_manager.subscribe(
            [
                NewHeadsSubscription(
                    label="new-heads-mainnet",
                    handler=new_heads_handler  # 区块头处理器
                ),
                LogsSubscription(
                    label="transfer",# 标签
                    handler=log_handler, #用于区分消息接受
                    address=Web3.to_checksum_address("0xdac17f958d2ee523a2206206994597c13d831ec7"),
                    topics=["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]
                ),

            ]
        )

        # Listen for events
        await w3.subscription_manager.handle_subscriptions()

    except Exception as e:
        print(f"An error occurred while subscribing to events: {e}")

asyncio.run(sub_manager())
