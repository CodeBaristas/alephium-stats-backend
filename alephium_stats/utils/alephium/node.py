import httpx

from .exceptions import AlephiumNodeRequestError


class AlephiumNode:
    def __init__(self, node_url, api_key):
        self.node_url = node_url
        self.default_headers = {
            "Accept": "application/json",
            "X-API-KEY": api_key,
        }

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
                response = await request_func(url, headers=headers, params=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as err:
                raise AlephiumNodeRequestError from err

    async def get_historic_hashrate(
        self, from_ts: int, to_ts: int | None = None
    ) -> str:
        params = {"fromTs": from_ts, "toTs": to_ts}
        hashrate = await self._send_request(
            "infos/history-hashrate", payload=self.remove_entry_if_none(params)
        )
        return hashrate.get("hashrate")

    async def get_current_hashrate(self, timespan: int | None = None) -> str:
        params = {"timespan": timespan}
        hashrate = await self._send_request(
            "infos/current-hashrate", payload=self.remove_entry_if_none(params)
        )
        return hashrate.get("hashrate")

    async def get_balance_by_address(
        self, address, mempool: bool | None = None
    ) -> dict:
        params = {"address": address, "mempool": mempool}
        balance = await self._send_request(
            f"addresses/{address}/balance", payload=self.remove_entry_if_none(params)
        )
        return balance

    async def get_group_by_address(self, address) -> int:
        group = await self._send_request(f"addresses/{address}/group")
        return group.get("group")

    async def get_current_difficulty(self) -> str:
        difficulty = await self._send_request("infos/current-difficulty")
        return difficulty.get("difficulty")

    async def get_block_flow_chain_info(self, from_group: int, to_group: int) -> int:
        params = {"fromGroup": from_group, "toGroup": to_group}
        block_flow_chain_info = await self._send_request(
            "blockflow/chain-info", payload=params
        )
        return block_flow_chain_info.get("currentHeight")
