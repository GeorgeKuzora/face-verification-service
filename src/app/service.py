import logging

from fastapi import FastAPI

app = FastAPI()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
