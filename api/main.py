import logging

from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from routes import deliveryman, orders, balance

from models.db_session import global_init, create_session

description = """All requests require a header in the following format: {'Authorization': 'Bearer jwt_token'}

JWT Payload structure:

    deliveryman_id: internal ID
    expires: the expiration time of the JWT
    admin: True or False (used for certain endpoints) not necessary"""

app = FastAPI(title="Deliveryman API", description=description)
app.include_router(deliveryman.router, prefix="/deliveryman", tags=["deliveryman"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(balance.router, prefix="/balance", tags=["balance"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    async with create_session() as sess:
        request.state.session = sess
        response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.on_event('startup')
async def startup_event():
    await global_init()
