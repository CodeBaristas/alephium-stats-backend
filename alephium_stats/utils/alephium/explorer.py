import httpx

from .exceptions import (
    AlephiumExplorerRequestError,
    AlephiumExplorerWrongAlphTypeError,
    AlephiumExplorerWrongTimeIntervalError,
)
from .types import SupplyType, TimeInterval


class AlephiumExplorer:
    def __init__(self, node_url):
        self.node_url = node_url
        self.default_headers = {}

    def remove_entry_if_none(self, params_: dict) -> dict:
        params = {key: value for key, value in params_.items() if value is not None}
        return params

    async def _send_request(self, endpoint, method="GET", payload=None, headers=None):
        if headers is None:
            headers = self.default_headers
        else:
            headers.update(self.default_headers)

        url = f"{self.node_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                request_func = client.post if method == "POST" else client.get
                response = await request_func(url, params=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as err:
                raise AlephiumExplorerRequestError from err

    async def get_info_heights(self) -> list:
        info_heights = await self._send_request("infos/heights")

        res = []
        for info_height in info_heights:
            data = {
                "chain_from": info_height.get("chainFrom"),
                "chain_to": info_height.get("chainTo"),
                "height": info_height.get("height"),
                "value": info_height.get("value"),
            }
            res.append(data)
        return res

    async def get_all_charts_hashrates(
        self, from_ts: int, to_ts: int, interval_type: str
    ) -> list:
        if not any(interval_type == item.value for item in TimeInterval):
            raise AlephiumExplorerWrongTimeIntervalError

        params = {"fromTs": from_ts, "toTs": to_ts, "interval-type": interval_type}
        chart_hashrates = await self._send_request("charts/hashrates", payload=params)

        res = []
        for info_height in chart_hashrates:
            data = {
                "timestamp": info_height.get("timestamp"),
                "hashrate": info_height.get("hashrate"),
                "value": info_height.get("value"),
            }
            res.append(data)
        return res

    async def get_charts_transaction_count(
        self, from_ts: int, to_ts: int, interval_type: str, per_chain: bool
    ) -> list:
        if not any(interval_type == item.value for item in TimeInterval):
            raise AlephiumExplorerWrongTimeIntervalError

        params = {"fromTs": from_ts, "toTs": to_ts, "interval-type": interval_type}
        if per_chain:
            transaction_counts = await self._send_request(
                "charts/transactions-count-per-chain", payload=params
            )
        else:
            transaction_counts = await self._send_request(
                "charts/transactions-count", payload=params
            )

        res = []
        for transaction_count in transaction_counts:
            data = {
                "timestamp": transaction_count.get("timestamp"),
                "total_count_all_chains": transaction_count.get("totalCountAllChains"),
            }
            res.append(data)
        return res

    async def get_alph_supply_type(self, supply_type: str) -> int:
        if not any(supply_type == item.value for item in SupplyType):
            raise AlephiumExplorerWrongAlphTypeError

        supply = await self._send_request(f"infos/supply/{supply_type}-alph")
        return supply

    async def get_total_transactions(self) -> int:
        transactions = await self._send_request("infos/total-transactions")
        return transactions

    async def get_average_block_times(self) -> list:
        average_block_times = await self._send_request("infos/average-block-times")

        res = []
        for average_block_time in average_block_times:
            data = {
                "chain_from": average_block_time.get("chainFrom"),
                "chain_to": average_block_time.get("chainTo"),
                "value": average_block_time.get("value"),
                "duration": average_block_time.get("duration"),
            }
            res.append(data)
        return res
