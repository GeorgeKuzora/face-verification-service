import logging

from fastapi import FastAPI

from app.api.handlers import router

app = FastAPI()

app.include_router(router=router)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
