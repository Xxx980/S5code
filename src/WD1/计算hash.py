from hashlib import sha256
import time

nick_name = 'xiaozihao'
start_with_num = '0000'


def get_hash(nick_name, start_with_num):
    time_start = time.time()

    nonce = 0

    while True:
        hash = sha256((nick_name + f'{nonce}').encode('utf-8')).hexdigest()
        if hash.startswith(start_with_num):
            time_end = time.time()
            print(f'花费时间：{time_end - time_start}')
            print(f'哈希内容:{nick_name + str(nonce)}')
            print(f'哈希值：{hash}')
            break

        nonce += 1


def main():
    get_hash(nick_name, start_with_num)
    start_with_num_new = start_with_num + '0'

    get_hash(nick_name, start_with_num_new)


if __name__ == '__main__':
    main()
