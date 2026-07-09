#http/sse transport for docker/

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
import uvicorn
from server import server


sse = SseServerTransport('/messages')

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive,request._send
    ) as streams:
        await server.run(
            streams[0],streams[1],
            server.create_initialization_options()
        )

app = Starlette(
    routes=[
        Route("/sse",endpoint=handle_sse),
        Mount("/messages",app = sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

