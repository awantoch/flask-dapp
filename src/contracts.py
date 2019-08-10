import time
import json
import os

from pathlib import Path
from crypto import w3

# parse ABI from compiled contract and initialize contract interface variable
def init_abi(contract_meta):
    file_path = f"build/contracts/{contract_meta['name']}.json"
    with open(Path(file_path)) as json_file:
        json_data = json.load(json_file)

    return w3.eth.contract(address=contract_meta['address'], abi=json_data['abi'])
