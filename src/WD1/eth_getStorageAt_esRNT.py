import time

from eth_utils import keccak
from web3 import Web3

# RPC_URL = ""
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.public.blastapi.io'))
contract_address = Web3.to_checksum_address('0xdA7377CB2B33DB3eA425a9301237A2295a76306b')





def get_storage_slot(slot):
    """使用 eth_getStorage_at 获取指定插槽的值，并转换为整数"""
    slot_hex = f"0x{slot:064x}"  # 转换为 64 位十六进制
    value = w3.eth.get_storage_at(contract_address, slot_hex)  # 返回 HexBytes
    return int.from_bytes(value, "big")  # 转换为整数

def read_locks():
    # 获取数组长度（插槽 0）
    length = get_storage_slot(0)
    print(f"Array length: {length}")

    # 计算数组数据的起始插槽
    base_slot = int.from_bytes(keccak(int(0).to_bytes(32, "big")), "big")

    # 遍历所有元素
    for i in range(length):
        # 每个 LockInfo 占 2 个插槽
        slot1 = base_slot + (i * 2)      # user 和 startTime
        slot2 = base_slot + (i * 2) + 1  # amount

        # 读取第一个插槽（user 和 startTime）
        data1 = get_storage_slot(slot1)
        # user: 低 20 字节 (160 位)，右对齐
        user = Web3.to_checksum_address(f"0x{data1:064x}"[-40:])
        # startTime: 高 8 字节 (64 位)，左移后提取
        start_time = (data1 >> 160) & 0xFFFFFFFFFFFFFFFF  # 直接对整数操作
        # 读取第二个插槽（amount）
        amount = get_storage_slot(slot2)

        # 打印结果
        print(f"locks[{i}]: user: {user}, startTime: {start_time}, amount: {amount}")

def main():
    time_start = time.time()
    read_locks()
    time_end = time.time()
    time_elapsed = time_end - time_start
    print(f"Time elapsed: {time_elapsed}")

if __name__ == "__main__":
    main()