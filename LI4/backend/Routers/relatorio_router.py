import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel
from database import get_db
from auth import requer_operacao

from Model.ReportSubsystem.GestorRelatorios import GestorRelatorios
from Model.ReportSubsystem.RelatorioDAO import RelatorioDAO


router = APIRouter(prefix="/relatorios", tags=["RELATÓRIOS"])


class RelatorioResponse(BaseModel):
    id: int
    nome_arquivo: str
    tipo_relatorio: str

    class Config:
        from_attributes = True


def _gestor(db=Depends(get_db)) -> GestorRelatorios:
    return GestorRelatorios(RelatorioDAO(db))


@router.get("/", response_model=List[RelatorioResponse])
def listar_relatorios(
    gestor: GestorRelatorios = Depends(_gestor),
    _=Depends(requer_operacao("lerRelatorio")),
):
    relatorios = gestor.listar_relatorios()
    return [
        RelatorioResponse(id=r.id, nome_arquivo=r.titulo, tipo_relatorio=r.tipo)
        for r in relatorios
    ]


@router.get("/{id}/download")
def download_relatorio(
    id: int,
    gestor: GestorRelatorios = Depends(_gestor),
    _=Depends(requer_operacao("lerRelatorio")),
):
    caminho = gestor.get_caminho_relatorio(id)

    if not caminho:
        raise HTTPException(status_code=404, detail="Relatório não encontrado na base de dados.")

    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Ficheiro PDF não encontrado no servidor.")

    return FileResponse(
        path=caminho,
        filename=os.path.basename(caminho),
        media_type="application/pdf",
    )


