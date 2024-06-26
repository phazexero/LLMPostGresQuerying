import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from dotenv import load_dotenv
from config.db.database import database
from routes.routes import router as main_router  # Import the central router
import os

load_dotenv()

# ROOT_PATH = os.environ.get("ROOT_PATH", "/")

# app = FastAPI(title="APIs for Reports", description="Export Reports API",
#               root_path=f"{ROOT_PATH}", openapi_url='/openapi.json', docs_url=None, redoc_url=None)
app = FastAPI(title="APIs for Reports", description="Export Reports API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the central router in the app
app.include_router(main_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(openapi_url=openapi_url, title="APIs for Reports")


# Dependency to connect and disconnect to/from the database


@app.on_event("startup")
async def startup_db_client():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
