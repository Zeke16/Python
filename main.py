from fastapi import FastAPI, status, HTTPException
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from bson import ObjectId
from models.Developer import Developer

app = FastAPI()
developers = []


async def conn():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://127.0.0.1:27017")
    db = client["dbeta"]
    return db


@app.get("/")
def welcome():
    return "Bienvenido a la app"


@app.get("/developers")
async def get_developers():
    try:
        db = await conn()
        developers = await db.developers.find().to_list(1000)
        for developer in developers:
            developer["_id"] = str(developer["_id"])
        return JSONResponse(status_code=200, content={"data": developers})
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": err})


@app.post("/developers")
async def create_developer(developer: Developer):
    try:
        db = await conn()
        await db.developers.insert_one(jsonable_encoder(developer))
        return JSONResponse(status_code=201, content={"message": "Registro creado"})
    except:
        return JSONResponse(status_code=500, content={"message": "Error al registrar"})


@app.put("/developers/{id}")
async def update_developer(developer: Developer, id: str):
    try:
        db = await conn()
        developers = await db.developers.find_one({"_id": ObjectId(id)})
        if not developers:
            return JSONResponse(status_code=400, content={"message": f"registro con id {id} no existe"})

        await db.developers.update_one({"_id": ObjectId(id)}, {"$set": jsonable_encoder(developer)})
        return JSONResponse(status_code=203, content={"message": "Registro actualizado"})
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar"})


@app.delete("/developers/{id}")
async def delete_developer(id: str):
    try:
        db = await conn()
        developers = await db.developers.find_one({"_id": ObjectId(id)})
        if not developers:
            return JSONResponse(status_code=400, content={"message": f"registro con id {id} no existe"})
        await db.developers.delete_one({"_id": ObjectId(id)})
        return JSONResponse(status_code=201, content={"message": "Registro eliminado"})
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar"})


@app.get("/developers/{id}")
async def get_one_developer(id: str):
    try:
        db = await conn()
        developers = await db.developers.find_one({"_id": ObjectId(id)})
        if not developers:
            return JSONResponse(status_code=400, content={"message": f"registro con id {id} no existe"})
        developers["_id"] = str(developers["_id"])
        return JSONResponse(status_code=200, content={"data": developers})
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"error": err})
