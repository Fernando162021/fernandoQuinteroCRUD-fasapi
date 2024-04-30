from fastapi import FastAPI, HTTPException
from db.db import client
from controller.libroCRUD import router as libros_router


app = FastAPI()
app.include_router(libros_router, tags=["libros"], prefix="/libros")
# MongoDB connection URL
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()



