from brownie import FundMe, MockV3Aggregator, network, accounts, config
from scripts.helpful import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONNMENTS


def deploy_found_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONNMENTS:
        price_feed_address = config['networks'][network.show_active()][
            'eth_usd_price_feed'
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        for contract in MockV3Aggregator:
            print(contract.latestRoundData())

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config['networks'][network.show_active()].get('verify'),
    )
    print(f'Contract deployed to {fund_me.address}')
    return fund_me


def main():
    deploy_found_me()
