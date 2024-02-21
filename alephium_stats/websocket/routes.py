from fastapi import APIRouter, WebSocket
from fastapi_websocket_pubsub import PubSubEndpoint
from fastapi_websocket_rpc.rpc_channel import RpcChannel


# fastapi pubsub, uses fastapi_websocket_rpc in the background and waits for responses, which
# lead to blocking calls if a client is not answering (wtf?), we patch the mether which waits
# for a client to respond, super hacky
# fmt: off
async def wait_for_response(self, promise, timeout):
    pass
RpcChannel.wait_for_response = wait_for_response
# fmt: on


async def on_connect(channel):
    """Automatically subscribes to the block_data topic"""
    await channel.on_message(
        {
            "request": {
                "method": "subscribe",
                "arguments": {"topics": ["block_data"]},
            }
        }
    )


router = APIRouter(prefix="/streams")
endpoint = PubSubEndpoint(on_connect=[on_connect])
endpoint.register_route(router, path="/pubsub")


@router.websocket("/blocks")
async def websocket_rpc_endpoint(websocket: WebSocket):
    await endpoint.main_loop(websocket)


@router.post("/trigger")
async def trigger_route_block_data(data: dict):
    await endpoint.publish(["block_data"], data=data)
