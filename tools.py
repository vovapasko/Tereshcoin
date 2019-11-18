import hashlib
import json
import logging
import os
import traceback

node_connected_to_network = "NODE_NEW_CONNECTED_MAIN_INFO"
from_older_node_id = "NODE_FROM_OLD_MESSAGE"


def get_hash(string):
    return hashlib.sha256(hashlib.sha256(string.encode("utf-8")).hexdigest().encode('utf-8')).hexdigest()


def log_new_node(**data):
    if not data['message_from'] == data['wallet_address']:
        address = data['deserealizedJson']['from_ip_address']
        _from = data['deserealizedJson']["_from"]
        print(f'Received data from {address} ip address and {_from} wallet address')
        with open(data['node_log_filename'], 'a+') as file:
            # file.write(f'New data from {address}:\n')
            message = json.dumps(data['deserealizedJson'])
            file.write(f'{str(message)}\n')
            file.flush()
            os.fsync(file.fileno())
            file.close()
        return True
    return False


def get_all_addresses(data):
    addr = []
    for datum in data:
        addr.append(datum['_from'])
    return addr


def log_old_node(**data):
    log_data = None
    try:
        log_data = get_log_data(data['node_log_filename'])
    except FileNotFoundError:
        print(traceback.print_exc())
    if log_data:
        addresses = get_all_addresses(log_data)
        new_address = data['message_from']
        if new_address not in addresses:
            log_new_node(**data)
    else:  # means that the node get a message for the first node in it's "life"
        log_new_node(**data)
    return False


def get_log_data(node_log_filename):
    try:
        file = open(node_log_filename, "r")
        data_str = file.read().split("\n")
        if data_str[0] == '':  # means that there are no data in log file
            return None
        del data_str[-1]
        json_dict_arr = []
        for string in data_str:
            new_json = json.loads(string)
            json_dict_arr.append(new_json)
        return json_dict_arr
    except Exception:
        print(traceback.print_exc())
        return None


functions = {node_connected_to_network: log_new_node,
             from_older_node_id: log_old_node}
