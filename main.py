from fastapi import FastAPI
from controller.poll_controller import router as poll_router
from controller.user_poll_controller import router as user_poll_router
from controller.company_poll_controller import router as company_poll_router


from repository.database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(poll_router)
app.include_router(user_poll_router)
app.include_router(company_poll_router)
