from scripts.helpful import get_account, LOCAL_BLOCKCHAIN_ENVIRONNMENTS, network
from scripts.deploy import deploy_found_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_found_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONNMENTS:
        pytest.skip('only for local testing')
