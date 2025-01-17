from brownie import *
from brownie.network.account import Account
from config import (
    BADGER_DEV_MULTISIG,
    WANT,
    LP_COMPONENT,
    REWARD_TOKEN,
    PROTECTED_TOKENS,
    FEES,
)
from dotmap import DotMap
import pytest
from helpers.constants import MaxUint256


@pytest.fixture
def deployer():
    return accounts[0]

@pytest.fixture
def rando():
    return accounts[6]

## CVX Locker ##
@pytest.fixture
def cvxcrv():
    return "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7"





@pytest.fixture
def deployed():
    """
    Deploys, vault, controller and strats and wires them up for you to test
    """
    deployer = accounts[0]

    strategist = deployer
    keeper = deployer
    guardian = deployer

    governance = accounts.at(BADGER_DEV_MULTISIG, force=True)

    controller = Controller.deploy({"from": deployer})
    controller.initialize(BADGER_DEV_MULTISIG, strategist, keeper, BADGER_DEV_MULTISIG)

    sett = SettV4.deploy({"from": deployer})
    sett.initialize(
        WANT,
        controller,
        BADGER_DEV_MULTISIG,
        keeper,
        guardian,
        False,
        "prefix",
        "PREFIX",
    )

    sett.unpause({"from": governance})
    controller.setVault(WANT, sett)

    ## TODO: Add guest list once we find compatible, tested, contract
    # guestList = VipCappedGuestListWrapperUpgradeable.deploy({"from": deployer})
    # guestList.initialize(sett, {"from": deployer})
    # guestList.setGuests([deployer], [True])
    # guestList.setUserDepositCap(100000000)
    # sett.setGuestList(guestList, {"from": governance})

    ## Start up Strategy
    strategy = MyStrategy.deploy({"from": deployer})
    strategy.initialize(
        BADGER_DEV_MULTISIG,
        strategist,
        controller,
        keeper,
        guardian,
        PROTECTED_TOKENS,
        FEES,
        {"from": deployer}
    )

    ## Tool that verifies bytecode (run independently) <- Webapp for anyone to verify

    ## Set up tokens
    want = interface.IERC20(WANT)
    lpComponent = interface.IERC20(LP_COMPONENT)
    rewardToken = interface.IERC20(REWARD_TOKEN)

    ## Wire up Controller to Strart
    ## In testing will pass, but on live it will fail
    controller.approveStrategy(WANT, strategy, {"from": governance})
    controller.setStrategy(WANT, strategy, {"from": deployer})

    ## Send from a whale of CVX
    whale = accounts.at("0x5F465e9fcfFc217c5849906216581a657cd60605", force=True)
    want.transfer(a[0], 10000 * 10 ** 18, {"from": whale})  ## 10k

    ## NOTE: THIS HAS TO BE DONE IN SETUP JUST FOR THIS STRAT
    ## Approve the Strat for bcrvCVX
    cvxCRVVault = SettV4.at(strategy.CVXCRV_VAULT())
    gov = accounts.at(sett.governance(), force=True)
    cvxCRVVault.approveContractAccess(strategy, {"from": gov})

    return DotMap(
        deployer=deployer,
        controller=controller,
        vault=sett,
        sett=sett,
        cvxCRVVault=cvxCRVVault,
        strategy=strategy,
        governance=governance,
        gov=gov,
        # guestList=guestList,
        want=want,
        lpComponent=lpComponent,
        rewardToken=rewardToken,
    )




@pytest.fixture
def delegation_registry():
    return Contract.from_explorer("0x469788fE6E9E9681C6ebF3bF78e7Fd26Fc015446")


## Contracts ##
@pytest.fixture
def vault(deployed):
    return deployed.vault


@pytest.fixture
def sett(deployed):
    return deployed.sett


@pytest.fixture
def controller(deployed):
    return deployed.controller


@pytest.fixture
def strategy(deployed):
    return deployed.strategy


## CVX
@pytest.fixture
def locker(strategy):
    locker = CvxLocker.at(strategy.LOCKER())

    return locker


@pytest.fixture
def staking(locker):
    return CvxStakingProxy.at(locker.stakingProxy())


## Tokens ##


@pytest.fixture
def want(deployed):
    return deployed.want


@pytest.fixture
def tokens():
    return [WANT, LP_COMPONENT, REWARD_TOKEN]


## Accounts ##
@pytest.fixture
def governance(deployed):
    return accounts.at(deployed.governance, force=True)


@pytest.fixture
def strategist(strategy):
    return accounts.at(strategy.strategist(), force=True)


@pytest.fixture
def settKeeper(vault):
    return accounts.at(vault.keeper(), force=True)


@pytest.fixture
def strategyKeeper(strategy):
    return accounts.at(strategy.keeper(), force=True)




@pytest.fixture
def setup_strat(deployer, sett, strategy, want):
    """
    Convenience fixture that depoists and harvests for us
    """
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount = startingBalance // 2
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    # End Setup

    # Deposit
    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    sett.deposit(depositAmount, {"from": deployer})

    available = sett.available()
    assert available > 0

    sett.earn({"from": deployer})

    chain.sleep(10000 * 13)  # Mine so we get some interest
    return strategy


## Forces reset before each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


