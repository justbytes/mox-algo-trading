import boa
from moccasin.config import get_config
from boa.contracts.abi.abi_contract import ABIContract
from typing import Tuple

STARTING_ETH_BALANCE = int(1000e18)
STARTING_USDC_BALANCE = int(100e6)
STARTING_WETH_BALANCE = int(1e18)

def _add_eth_balance():
    boa.env.set_balance(boa.env.eoa, STARTING_ETH_BALANCE)

def _add_token_balance(usdc, weth, active_network):
   
    weth.deposit(value=STARTING_WETH_BALANCE)
    our_address = boa.env.eoa
    
    with boa.env.prank(usdc.owner()):
        usdc.updateMasterMinter(our_address)
        
    usdc.configureMinter(our_address, STARTING_USDC_BALANCE)
    usdc.mint(our_address, STARTING_USDC_BALANCE)
    
    
    
def setup_script() -> Tuple[ABIContract,ABIContract,ABIContract,ABIContract]:
    print("Starting setup script")
    
    active_network = get_config().get_active_network()
    
    usdc = active_network.manifest_named("usdc")
    weth = active_network.manifest_named("weth")

    if active_network.is_local_or_forked_network():
        _add_eth_balance()
        _add_token_balance(usdc, weth, active_network)


 
def moccasin_main():
    setup_script()