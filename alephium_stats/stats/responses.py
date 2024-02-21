from sqlmodel import SQLModel


class StatsBalanceGroupOut(SQLModel):
    balance: str
    balance_hint: str
    locked_balance: str
    locked_balance_hint: str
    utxo_num: int
    group: int


class StatsCurrentHashrateOut(SQLModel):
    hashrate: str


class StatsHistoryHashrateOut(SQLModel):
    hashrate: str


class StatsCurrentDifficultyOut(SQLModel):
    difficulty: str


class StatsBlockFlowChainInfoOut(SQLModel):
    current_height: int


class ChainOut(SQLModel):
    chain_from: int
    chain_to: int
    value: int


class StatsInfoHeightsOut(ChainOut):
    height: int


class StatsAverageBlockTimes(ChainOut):
    duration: int


class StatsAllChartsHashratesOut(SQLModel):
    timestamp: int
    hashrate: int
    value: int


class StatsChartsTransactionCountOut(SQLModel):
    timestamp: int
    total_count_all_chains: int


class StatsAlphSupply(SQLModel):
    supply: int


class StatsTotalTransactions(SQLModel):
    amount: int
