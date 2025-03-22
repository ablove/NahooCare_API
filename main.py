from fastapi import FastAPI
from controllers import database_controller, account_controller
app = FastAPI()

app.include_router(database_controller.router, prefix="/api", tags=["Database"])
app.include_router(account_controller.router,prefix='/api/account', tags=['Account'])