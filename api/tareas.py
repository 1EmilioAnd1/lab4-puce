from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarea(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    completada: bool = False

tareas: List[Tarea] = []

@app.get("/tareas")
async def listar_tareas():
    return tareas

@app.post("/tareas")
async def crear_tarea(tarea: Tarea):
    tarea.id = len(tareas) + 1
    tareas.append(tarea)
    return {"mensaje": "Tarea creada exitosamente", "tarea": tarea}

@app.get("/tareas/{tarea_id}")
async def obtener_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.put("/tareas/{tarea_id}")
async def actualizar_tarea(tarea_id: int, tarea_actualizada: Tarea):
    for i, tarea in enumerate(tareas):
        if tarea.id == tarea_id:
            tarea_actualizada.id = tarea_id
            tareas[i] = tarea_actualizada
            return {"mensaje": "Tarea actualizada", "tarea": tarea_actualizada}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: int):
    for i, tarea in enumerate(tareas):
        if tarea.id == tarea_id:
            del tareas[i]
            return {"mensaje": "Tarea eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
