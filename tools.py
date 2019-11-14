import hashlib
import os


def get_hash(string):
    return hashlib.sha256(hashlib.sha256(string.encode("utf-8")).hexdigest().encode('utf-8')).hexdigest()


def fun(**data):
    if not data['message_from'] == data['wallet_address']:
        address = data['from_addr']
        _from = data['deserealizedJson']["from"]
        print(f'Received data from {address} ip address and {_from} wallet address')
        with open(data['node_chain_filename'], 'a+') as file:
            file.write(f'New data from {address}:\n')
            message = data['deserealizedJson']
            file.write(f'{str(message)}\n')
            file.flush()
            os.fsync(file.fileno())
            return True
    return False


functions = {"NODE_MAIN_INFO": fun}
