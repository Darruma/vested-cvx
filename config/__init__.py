## Ideally, they have one file with the settings for the strat and deployment
## This file would allow them to configure so they can test, deploy and interact with the strategy

BADGER_DEV_MULTISIG = "0xb65cef03b9b89f99517643226d76e286ee999e77"

WANT = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"  ## CVX
LP_COMPONENT = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B"  ## CVX // Technically we don't have an LP component
REWARD_TOKEN = "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7"  ## cvxCRV

PROTECTED_TOKENS = [WANT, LP_COMPONENT, REWARD_TOKEN]
## Fees in Basis Points
DEFAULT_GOV_PERFORMANCE_FEE = 1000
DEFAULT_PERFORMANCE_FEE = 1000
DEFAULT_WITHDRAWAL_FEE = 50

FEES = [DEFAULT_GOV_PERFORMANCE_FEE, DEFAULT_PERFORMANCE_FEE, DEFAULT_WITHDRAWAL_FEE]

REGISTRY = "0xFda7eB6f8b7a9e9fCFd348042ae675d1d652454f"  # Multichain BadgerRegistry
