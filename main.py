from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from routes import docs
from routes.sso import router as SsoRouter
from database import initiate_database

# 自訂 Swagger 文件
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI 第三方登入 APIs",
        version="1.0.0",
        description="這是第三方登入",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

def get_application():
    app = FastAPI()
    app.openapi = custom_openapi

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(docs.router)
    app.include_router(SsoRouter, tags=["第三方登入"], prefix="/sso")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    return app

app = get_application()

@app.on_event("startup")
async def start_database():
    await initiate_database()
