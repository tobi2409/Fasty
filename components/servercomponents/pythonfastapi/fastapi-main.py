from fastapi import FastAPI, Header, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], #TODO: vorerst nur so möglich, da file-Protokol vom Browser nicht unterstützt wird
    allow_methods = ["*"],
    allow_headers = ["*"]
)
