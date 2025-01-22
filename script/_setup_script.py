import boa
from moccasin.config import get_active_network, Network
from boa.contracts.abi.abi_contract import ABIContract
from typing import Tuple

STARTING_ETH_BALANCE = int(1000e18)
STARTING_USDC_BALANCE = int(100e6)
STARTING_WETH_BALANCE = int(1e18)


def _add_eth_balance():
    boa.env.set_balance(boa.env.eoa, STARTING_ETH_BALANCE)


def _add_token_balance(usdc: ABIContract, weth: ABIContract, active_network: Network):
    my_address = boa.env.eoa
    with boa.env.prank(usdc.owner()):
        usdc.updateMasterMinter(my_address)
    usdc.configureMinter(my_address, STARTING_USDC_BALANCE)
    usdc.mint(my_address, STARTING_USDC_BALANCE)
    weth.deposit(value=STARTING_WETH_BALANCE)


def setup_script() -> Tuple[ABIContract, ABIContract, ABIContract, ABIContract]:
    active_network = get_active_network()

    print("Starting setup script...")
    usdc = active_network.manifest_named("usdc")
    weth = active_network.manifest_named("weth")
    
    
    if active_network.is_local_or_forked_network():
        _add_eth_balance()
        _add_token_balance(usdc, weth, active_network)
        
    print("This part takes a while...")
    aavev3_protocol_data_provider = active_network.manifest_named("aavev3_protocol_data_provider")
    a_tokens = aavev3_protocol_data_provider.getAllATokens()
    for a_token in a_tokens:
        if "WETH" in a_token[0]:
            a_weth = active_network.manifest_named("weth", address=a_token[1])
        if "USDC" in a_token[0]:
            a_usdc = active_network.manifest_named("usdc", address=a_token[1])
    
    return usdc, weth, a_usdc, a_weth