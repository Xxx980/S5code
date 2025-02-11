import rsa
import hashlib


# 生成 RSA 公私钥对
def generate_keys():
    public_key, private_key = rsa.newkeys(512)  # 生成 512 位 RSA 密钥
    return public_key, private_key


# 计算哈希值并检查前四个字符是否为 '0000'
def proof_of_work(nickname):
    nonce = 0
    while True:
        combined = f"{nickname}{nonce}"
        hash_value = hashlib.sha256(combined.encode()).hexdigest()
        if hash_value[:4] == '0000':  # 哈希值前四个字符是 '0000'
            return nonce, hash_value
        nonce += 1


# 使用私钥对数据进行签名
def sign_data(private_key, data):
    return rsa.sign(data.encode(), private_key, 'SHA-256')


# 使用公钥验证签名
def verify_signature(public_key, data, signature):
    try:
        rsa.verify(data.encode(), signature, public_key)
        return True
    except rsa.VerificationError:
        return False


# 主程序逻辑
def main():
    # 生成公私钥对
    public_key, private_key = generate_keys()

    # 假设昵称是 "user123"
    nickname = "xiaozihao"

    # 找到符合 POW 条件的 nonce
    nonce, hash_value = proof_of_work(nickname)
    print(f"找到符合 POW 条件的 nonce: {nonce}, 哈希值: {hash_value}")

    # 生成签名
    combined_data = f"{nickname}{nonce}"
    signature = sign_data(private_key, combined_data)

    # 验证签名
    is_verified = verify_signature(public_key, combined_data, signature)
    if is_verified:
        print("签名验证成功！")
    else:
        print("签名验证失败！")


if __name__ == "__main__":
    main()
