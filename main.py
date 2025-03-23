from fastapi import FastAPI
from controllers import database_controller, account_controller,healthprofile_controller,healthcare_controller,rating_controller, admin_controller
app = FastAPI()

app.include_router(database_controller.router, prefix="/api", tags=["Database"])
app.include_router(account_controller.router,prefix='/api/account', tags=['Account'])
app.include_router(healthprofile_controller.router,prefix="/api/healthprofile",tags=["HealthProfile"])
app.include_router(healthcare_controller.router, prefix="/api/healthcare", tags=["Healthcare Centers"])
app.include_router(rating_controller.router, prefix="/api/rating", tags=["Ratings"])
app.include_router(admin_controller.router, prefix="/api/admin", tags=["Admin"])