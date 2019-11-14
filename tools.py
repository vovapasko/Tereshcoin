import hashlib
import logging
import os

node_connected_to_network = "CONNECTED_NODE_MAIN_INFO"


def get_hash(string):
    return hashlib.sha256(hashlib.sha256(string.encode("utf-8")).hexdigest().encode('utf-8')).hexdigest()


def log_new_node(**data):
    if not data['message_from'] == data['wallet_address']:
        address = data['from_addr']
        _from = data['deserealizedJson']["_from"]
        print(f'Received data from {address} ip address and {_from} wallet address')
        with open(data['node_log_filename'], 'a+') as file:
            file.write(f'New data from {address}:\n')
            message = data['deserealizedJson']
            file.write(f'{str(message)}\n')
            file.flush()
            os.fsync(file.fileno())
            file.close()
        return True
    return False


functions = {node_connected_to_network: log_new_node}
