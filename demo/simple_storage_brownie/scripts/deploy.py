from brownie import accounts, config, SimpleStorage, network
import os


def deploy_simple_storage():
    # account = accounts.load('metamask_test')
    # account = accounts.add(config['wallets']['from_key'])
    account = get_account()
    print(f'Account : {account}')
    simple_storage_contract = SimpleStorage.deploy({'from': account})
    print(f'SimpleStorage contract address: {simple_storage_contract.address}')

    stored_value = simple_storage_contract.retrieve()
    print(f'Stored value: {stored_value}')

    tx = simple_storage_contract.store(15, {'from': account})
    tx.wait(1)

    updated_value = simple_storage_contract.retrieve()
    print(f'Updated value: {updated_value}')


def get_account():
    if (network.show_active == 'development'):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def main():
    deploy_simple_storage()
