from brownie import Election, network
from scripts.helper_scripts import get_account


def main():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    print(f"Election contract deployed on {network.show_active()} network at : {election_contract.address}")
