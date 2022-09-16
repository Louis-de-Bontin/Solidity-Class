from brownie import FundMe, MockV3Aggregator, network, accounts, config
from scripts.helpful import get_account


def fund():
    print(f'Len fund me = {len(FundMe)}')
    fund_me = FundMe[-1]
    print(f'Funding {fund_me.address}')
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f'The current entry fee is {entrance_fee}')
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
