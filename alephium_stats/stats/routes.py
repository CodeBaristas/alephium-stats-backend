from fastapi import APIRouter

from ..common import alph_explorer, alph_node

# NOTE: deactivated for presentation
# from ..common import limiter
from ..deps import ApiKey
from .responses import (
    StatsAllChartsHashratesOut,
    StatsAlphSupply,
    StatsAverageBlockTimes,
    StatsBalanceGroupOut,
    StatsBlockFlowChainInfoOut,
    StatsChartsTransactionCountOut,
    StatsCurrentDifficultyOut,
    StatsCurrentHashrateOut,
    StatsHistoryHashrateOut,
    StatsInfoHeightsOut,
    StatsTotalTransactions,
)
from .types import SupplyType, TimeInterval

router = APIRouter(prefix="/stats")


def remove_entry_if_none(params_: dict) -> dict:
    params = {key: value for key, value in params_.items() if value is not None}
    return params


@router.get("/addresses", response_model=StatsBalanceGroupOut)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_balance_and_group_by_address(
    address: str,
    mempool: bool | None = None,
    api_key=ApiKey,
):
    balance_ = await alph_node.get_balance_by_address(address=address, mempool=mempool)
    group_ = await alph_node.get_group_by_address(address=address)

    return StatsBalanceGroupOut(
        balance=str(balance_.get("balance")),
        balance_hint=str(balance_.get("balanceHint")),
        locked_balance=str(balance_.get("lockedBalance")),
        locked_balance_hint=str(balance_.get("lockedBalanceHint")),
        utxo_num=balance_.get("utxoNum"),
        group=group_,
    )


@router.get("/info/hashrate/current", response_model=StatsCurrentHashrateOut)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_current_hashrate(timespan: int | None = None, api_key=ApiKey):
    hashrate_ = await alph_node.get_current_hashrate(timespan=timespan)
    return StatsCurrentHashrateOut(hashrate=hashrate_)


@router.get("/info/hashrate/historic", response_model=StatsHistoryHashrateOut)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_historic_hashrate(
    from_ts: int,
    to_ts: int | None = None,
    api_key=ApiKey,
):
    hashrate_ = await alph_node.get_historic_hashrate(from_ts=from_ts, to_ts=to_ts)
    return StatsHistoryHashrateOut(hashrate=hashrate_)


@router.get("/info/current-difficulty", response_model=StatsCurrentDifficultyOut)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_current_difficulty(
    api_key=ApiKey,
):
    difficulty_ = await alph_node.get_current_difficulty()
    return StatsCurrentDifficultyOut(difficulty=difficulty_)


@router.get("/blockflow/chain-info", response_model=StatsBlockFlowChainInfoOut)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_block_flow_chain_info(
    from_group: int,
    to_group: int,
    api_key=ApiKey,
):
    chain_info_ = await alph_node.get_block_flow_chain_info(
        from_group=from_group, to_group=to_group
    )
    return StatsBlockFlowChainInfoOut(current_height=chain_info_)


@router.get("/info/heights", response_model=list[StatsInfoHeightsOut])
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_info_heights(
    api_key=ApiKey,
):
    info_heights_ = await alph_explorer.get_info_heights()
    return info_heights_


@router.get("/charts/hashrates", response_model=list[StatsAllChartsHashratesOut])
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_all_charts_hashrates(
    from_ts: int,
    to_ts: int,
    interval_type: TimeInterval,
    api_key=ApiKey,
):
    all_charts_hashrates_ = await alph_explorer.get_all_charts_hashrates(
        from_ts=from_ts, to_ts=to_ts, interval_type=interval_type.value
    )
    return all_charts_hashrates_


@router.get(
    "/charts/transactions-count", response_model=list[StatsChartsTransactionCountOut]
)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_all_charts_transaction_count(
    from_ts: int,
    to_ts: int,
    interval_type: TimeInterval,
    per_chain: bool,
    api_key=ApiKey,
):
    transaction_counts_ = await alph_explorer.get_charts_transaction_count(
        from_ts=from_ts,
        to_ts=to_ts,
        interval_type=interval_type.value,
        per_chain=per_chain,
    )

    return transaction_counts_


@router.get("/alph-supply", response_model=StatsAlphSupply)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_alph_supply(
    supply_type: SupplyType,
    api_key=ApiKey,
):
    supply_type_ = await alph_explorer.get_alph_supply_type(
        supply_type=supply_type.value
    )
    return StatsAlphSupply(supply=supply_type_)


@router.get("/total-transactions", response_model=StatsTotalTransactions)
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_total_transactions(
    api_key=ApiKey,
):
    total_transactions_ = await alph_explorer.get_total_transactions()
    return StatsTotalTransactions(amount=total_transactions_)


@router.get("/average-blocktimes", response_model=list[StatsAverageBlockTimes])
# NOTE: deactivated for presentation
# @limiter.limit("5/minute")
async def get_average_block_times(
    api_key=ApiKey,
):
    average_block_times_ = await alph_explorer.get_average_block_times()
    return average_block_times_
