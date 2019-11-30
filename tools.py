import hashlib
import json
import logging
import os
import pickle
import traceback

node_connected_to_network = "NODE_NEW_CONNECTED_MAIN_INFO"
from_older_node_id = "NODE_FROM_OLD_MESSAGE"
node_request_data = "NODE_GIVE_ME_DATA"
node_send_to_concrete_node_data = "NODE_SEND_DATA_TO_NODE"


def format_json_message(**data):
    new_json_message = {}
    for key, value in data.items():
        new_json_message[str(key)] = value
    return new_json_message


def get_hash(string):
    return hashlib.sha256(hashlib.sha256(string.encode("utf-8")).hexdigest().encode('utf-8')).hexdigest()


def write_new_node(**data):
    node = data["node"]
    wallet_address = node.wallet_address
    message = data['message']
    if not message['_from'] == wallet_address:
        address = message['from_ip_address']
        _from = message["_from"]
        print(f'Received data from {address} ip address and {_from} wallet address')
        with open(node.node_info_filename, 'a+') as file:
            # file.write(f'New data from {address}:\n')
            message = json.dumps(message)
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


def write_old_node(**data):
    log_data = None
    node = data["node"]
    message = data["message"]
    try:
        log_data = get_node_data(node.node_info_filename)
    except FileNotFoundError:
        print(traceback.print_exc())
    if log_data:
        addresses = get_all_addresses(log_data)
        new_address = message['_from']
        if new_address not in addresses:
            write_new_node(**data)
    else:  # means that the node get a message for the first node in it's "life"
        write_new_node(**data)
    return False


def get_node_data(node_log_filename):
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


def handle_data_receiver(**data):
    node = data["node"]
    node_wallet = node.wallet_address
    message = data["message"]
    send_to = message["_from"]
    if node_wallet != send_to:  # means that address won't send data to itself
        header = node_send_to_concrete_node_data
        new_message = "Take my data"
        chain_data = node.get_chain_data
        _from = node_wallet
        json_message = format_json_message(header=header, receiver=send_to, _from=_from, message=new_message, data=chain_data)
        node.send_message_to_nodes(json_message)


def handle_received_node_data(**data):
    node = data["node"]
    message = data["message"]
    receiver = message["receiver"]
    my_address = node.wallet_address
    if my_address == receiver:
        chain_data = message["data"]
        node.writeChainData(chain_data)
    pass


functions = {node_connected_to_network: write_new_node,
             from_older_node_id: write_old_node,
             node_request_data: handle_data_receiver,
             node_send_to_concrete_node_data: handle_received_node_data
             }
