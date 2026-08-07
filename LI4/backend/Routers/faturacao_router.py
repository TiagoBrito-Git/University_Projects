from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_db
from auth import requer_operacao
from Model.PaymentsSubsystem.GestorPagamentos import GestorPagamentos
from Model.RepairSubsystem.GestorOrdensDeServico import GestorOrdensDeServico, OrdemDeServicoDAO
from Model.RepairSubsystem.IntervencaoDAO import IntervencaoDAO
from Model.RepairSubsystem.DiagnosticoDAO import DiagnosticoDAO


class FaturaCreateBody(BaseModel):
    id_os: int
    descricao: str
    valor: float


router = APIRouter(prefix="/fatura", tags=["FATURACAO"])

@router.get("/")
def listar_todas(db=Depends(get_db), _=Depends(requer_operacao("lerFatura"))):
    gestor = GestorPagamentos(db)
    faturas = gestor.listar_faturas()
    return [f.to_dict() for f in faturas]

@router.post("/", status_code=201)
def criar_fatura(
    dados: FaturaCreateBody,
    db=Depends(get_db),
    _=Depends(requer_operacao("pagarFatura")),
):
    gestor = GestorPagamentos(db)
    try:
        fatura_id = gestor.criar_fatura(dados.id_os, {}, dados.valor, "transferência")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Fatura criada com sucesso!", "id": fatura_id}

@router.get("/{id_fatura}/download")
def download_fatura(id_fatura: int, db=Depends(get_db), _=Depends(requer_operacao("lerFatura"))):
    gestor = GestorPagamentos(db)
    pdf_buffer = gestor.obter_pdf_fatura(id_fatura)

    if not pdf_buffer:
        raise HTTPException(status_code=404, detail="Fatura não encontrada")

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=fatura_{id_fatura}.pdf"}
    )

@router.put("/{id_fatura}/pagar")
def pagar_fatura(id_fatura: int, db=Depends(get_db), _=Depends(requer_operacao("pagarFatura"))):
    gestor_pag = GestorPagamentos(db)
    gestor_os = GestorOrdensDeServico(OrdemDeServicoDAO(db), IntervencaoDAO(db), DiagnosticoDAO(db))

    fatura = gestor_pag.consultar_fatura(id_fatura)
    if not fatura:
        raise HTTPException(status_code=404, detail="Fatura não encontrada.")
    if fatura.estado == "paga":
        raise HTTPException(status_code=400, detail="Fatura já foi paga.")

    try:
        try:
            db.rollback()
        except Exception:
            pass
        db.start_transaction()

        cursor = db.cursor()
        cursor.execute("UPDATE fatura SET estado = 'paga' WHERE id = %s", (id_fatura,))
        cursor.close()

        os_atual = gestor_os.consultar_os(fatura.id_os)
        if os_atual and os_atual.estado not in ("Cancelada", "Encerrada"):
            if os_atual.estado == "Em Reparação":
                if not gestor_os.alterar_estado_em_transacao(fatura.id_os, "Aguarda Faturação"):
                    db.rollback()
                    raise HTTPException(status_code=400, detail="Não foi possível transitar para 'Aguarda Faturação'.")
                os_atual = gestor_os.consultar_os(fatura.id_os)

            if os_atual and os_atual.estado != "Faturada":
                if not gestor_os.alterar_estado_em_transacao(fatura.id_os, "Faturada"):
                    db.rollback()
                    raise HTTPException(status_code=400, detail="Não foi possível transitar para 'Faturada'.")
                os_atual = gestor_os.consultar_os(fatura.id_os)

            if os_atual and os_atual.estado != "Encerrada":
                if not gestor_os.alterar_estado_em_transacao(fatura.id_os, "Encerrada"):
                    db.rollback()
                    raise HTTPException(status_code=400, detail="Não foi possível encerrar a OS.")

        db.commit()
        return {"message": "Fatura paga e OS encerrada com sucesso!"}

    except HTTPException:
        try: db.rollback()
        except Exception: pass
        raise
    except Exception:
        try: db.rollback()
        except Exception: pass
        raise