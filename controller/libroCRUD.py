from typing import List

from fastapi import HTTPException, APIRouter
from db.db import collection
from model.libro import Libro

router = APIRouter()


@router.post("/", response_description="Crear un nuevo libro", response_model=Libro)
async def create_libro(libro: Libro):
    existing_libro = await collection.find_one({"isbn": libro.isbn})
    if existing_libro is not None:
        raise HTTPException(status_code=404, detail="Libro ya existe")
    result = await collection.insert_one(libro.dict())
    libro._id = str(result.inserted_id)
    return libro


@router.get("/", response_description="Listar libros", response_model=List[Libro])
async def read_libros():
    libros = await collection.find().to_list(100)
    for libro in libros:
        libro["_id"] = str(libro["_id"])
    return libros


@router.get("/{isbn}", response_model=Libro)
async def find_libro_by_isbn(isbn: str):
    libro = await collection.find_one({"isbn": isbn})
    if libro:
        return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@router.put("/{isbn}", response_model=Libro)
async def update_libro(isbn: str, libro: Libro):
    updated_libro = await collection.find_one_and_update(
        {"isbn": isbn}, {"$set": libro.dict()}
    )
    if updated_libro:
        return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@router.delete("/{isbn}", response_model=Libro)
async def delete_libro(isbn: str):
    deleted_libro = await collection.find_one_and_delete({"isbn": isbn})
    if deleted_libro:
        return deleted_libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")
