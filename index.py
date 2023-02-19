import os

os.system("pip install eth-account")

import requests
from multiprocessing.pool import ThreadPool as Pool
import time
import secrets
from eth_account import Account

url = "https://mainnet.infura.io/v3/34d9c06fc4ff435cafb3283a1705606a"

def check():
    while True:
        private = secrets.token_hex(32)
        private_key = "0x" + private
        account = Account.from_key(private_key)

        try:
            response = requests.post(url, json={
                "method": "eth_getBalance",
                "params": [
                    account.address,
                    "latest"
                ],
                "id": 42,
                "jsonrpc": "2.0"
            }).json()

            balance = int(response["result"], 16)
            name = private_key + " : " + str(balance)

            if balance != 0:
                open(name, "a").close()

            print(name)

            time.sleep(0.5)
        except Exception as e:
            print("Private key:", private_key, "Error: ", e)
            break

threads = 16

pool = Pool(threads)
for _ in range(threads):
    pool.apply_async(check, ())
pool.close()
pool.join()
