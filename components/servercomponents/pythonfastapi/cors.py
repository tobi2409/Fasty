from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["!!allow_origins!!"],
    allow_methods = ["!!allow_methods!!"],
    allow_headers = ["!!allow_headers!!"]
)
