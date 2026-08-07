from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime
from database import get_db
from auth import requer_operacao, get_utilizador_atual
from Model.RepairSubsystem.GestorOrdensDeServico import GestorOrdensDeServico, OrdemDeServicoDAO
from Model.SecuritySubsystem.GestorSeguranca import GestorDeSeguranca, UtilizadorDAO
from Model.ClientSubsystem.GestorClientes import GestorClientes, ClienteDAO, TrotineteDAO, Cliente, Trotinete
from Model.StockSubsystem.GestorStock import GestorStock, PecaDAO
from Model.RepairSubsystem.IntervencaoDAO import IntervencaoDAO
from Model.RepairSubsystem.DiagnosticoDAO import DiagnosticoDAO
from Model.RepairSubsystem.Intervencao import Intervencao as IntervencaoModel
from Model.PaymentsSubsystem.GestorPagamentos import GestorPagamentos



router = APIRouter(prefix="/os", tags=["OS"])

class OSResponse(BaseModel):
    id: int
    data_abertura: date
    data_conclusao: Optional[date] = None
    descricao: str
    estado: str
    trotinete: str
    numero_serie: str
    nome_cliente: str
    email_cliente: Optional[str] = None
    tecnico: str

    class Config:
        from_attributes = True


class OSCreate(BaseModel):
    descricao: str
    nif_cliente: str
    n_serie_trotinete: str
    id_tecnico: int

class OSALTER(BaseModel):
    descricao: str

class OS_STATE(BaseModel):
    id: int
    estado: str
    tipo_pagamento: str = "dinheiro"

class DecisaoCliente(BaseModel):
    decisao: str  # "Aprovado" | "Rejeitado"


class IntervencaoCreate(BaseModel):
    descricao: str
    tempo: float
    pecas: dict


class DiagnosticoCreate(BaseModel):
    descricao: str
    tempo_estimado: float
    pecas: dict[int,int]


def _gestor_os(db=Depends(get_db)) -> GestorOrdensDeServico:
    return GestorOrdensDeServico(OrdemDeServicoDAO(db), IntervencaoDAO(db), DiagnosticoDAO(db))

def _gestor_clientes(db=Depends(get_db)) -> GestorClientes:
    return GestorClientes(ClienteDAO(db), TrotineteDAO(db))

def _gestor_utilizadores(db=Depends(get_db)) -> GestorDeSeguranca:
    return GestorDeSeguranca(UtilizadorDAO(db))

def _gestor_stock(db=Depends(get_db)) -> GestorStock:
    return GestorStock(PecaDAO(db))

@router.get("/config")
def obter_config(_=Depends(requer_operacao("lerOS"))):
    return {
        "taxa_mao_obra": GestorOrdensDeServico.TAXA_MAO_OBRA,
        "taxa_diagnostico": GestorOrdensDeServico.TAXA_DIAGNOSTICO,
    }


@router.get("/", response_model=List[OSResponse])
def listar_os(
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    gestor_cli: GestorClientes = Depends(_gestor_clientes),
    gestor_seg: GestorDeSeguranca = Depends(_gestor_utilizadores),
    _=Depends(requer_operacao("lerOS")),
):
    ordens = gestor_os.listar_ordens_de_servico()
    res = []

    for os in ordens:
        trotinete = gestor_cli.consultar_trotinete(os.id_trotinete)
        n_serie = trotinete.get_numero_serie() if trotinete else "Desconhecida"
        nome_trotinete = trotinete.get_modelo() if trotinete else "Desconhecida"

        tecnico = gestor_seg.consultarUtilizador(os.id_tecnico)
        nome_tecnico = tecnico.nome if tecnico else "Desconhecido"

        cliente = gestor_cli.consultar_cliente(os.id_cliente)
        nome_cliente = cliente.get_nome() if cliente else "Desconhecido"
        email_cliente = cliente.get_email() if cliente else None

        res.append(OSResponse(
            id=os.id,
            data_abertura=os.data_abertura,
            data_conclusao=os.data_conclusao,
            descricao=os.descricao,
            estado=os.estado,
            trotinete=nome_trotinete,
            numero_serie=n_serie,
            nome_cliente=nome_cliente,
            email_cliente=email_cliente,
            tecnico=nome_tecnico,
        ))

    return res


@router.post("/", status_code=201)
def criar_os(
    dados: OSCreate,
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    gestor_cli: GestorClientes = Depends(_gestor_clientes),
    user=Depends(get_utilizador_atual),
    _=Depends(requer_operacao("criarOS")),
):
    c: Cliente = gestor_cli.consultar_cliente_nif(dados.nif_cliente)
    if c is None:
        raise HTTPException(status_code=404, detail=f"Erro: Cliente com NIF {dados.nif_cliente} não existe.")

    t: Trotinete = gestor_cli.consultar_trotinete_numero_serie(dados.n_serie_trotinete)
    if t is None:
        raise HTTPException(status_code=404, detail=f"Erro: Trotinete com nº série '{dados.n_serie_trotinete}' não existe.")

    try:
        gestor_os.criar_ordem_de_servico(
            None,
            dados.descricao,
            t.get_id(),
            dados.id_tecnico,
            c.get_id(),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "OS criada com sucesso!"}


@router.put("/{id}")
def editar_os(
    id: int,
    dados: OSALTER,
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    _=Depends(requer_operacao("editarOS")),
):
    try:
        sucesso = gestor_os.atualizar_ordem_de_servico(id, None, dados.descricao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Ordem de Serviço com ID {id} não encontrada.")
    return {"message": "OS atualizada com sucesso!"}


@router.put("/{id}/proximo_estado")
def editar_state_os(
    id: int,
    dados: OS_STATE,
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    _=Depends(requer_operacao("editarOS")),
):
    sucesso = gestor_os.alterar_estado_ordem_de_servico(id, dados.estado)
    if not sucesso:
        raise HTTPException(status_code=400, detail=f"Transição de estado inválida para OS {id}.")
    return {"message": "Estado atualizado com sucesso!"}


@router.put("/{id}/avancar")
def avancar_estado_os(
    id: int,
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    _=Depends(requer_operacao("editarOS")),
):
    sucesso = gestor_os.avancar_estado_ordem_de_servico(id)
    if not sucesso:
        raise HTTPException(status_code=400, detail=f"Não é possível avançar o estado da OS {id}.")
    return {"message": "Estado avançado com sucesso!"}


@router.put("/{id}/decisao-cliente")
def registar_decisao_cliente(
    id: int,
    dados: DecisaoCliente,
    db=Depends(get_db),
    _=Depends(requer_operacao("editarOS")),
):
    if dados.decisao not in ("Aprovado", "Rejeitado"):
        raise HTTPException(status_code=400, detail="Decisão inválida. Use 'Aprovado' ou 'Rejeitado'.")

    gestor_os = GestorOrdensDeServico(OrdemDeServicoDAO(db), IntervencaoDAO(db), DiagnosticoDAO(db))
    gestor_pagamentos = GestorPagamentos(db)

    os_atual = gestor_os.consultar_os(id)
    if not os_atual:
        raise HTTPException(status_code=404, detail=f"Ordem de Serviço com ID {id} não encontrada.")
    if os_atual.estado != "Aguarda Resposta":
        raise HTTPException(status_code=400, detail=f"OS {id} não está em 'Aguarda Resposta' (estado atual: '{os_atual.estado}').")

    dados_fatura = gestor_os.preparar_dados_finalizacao(id, "Cancelada") if dados.decisao == "Rejeitado" else None

    try:
        try:
            db.rollback()
        except Exception:
            pass
        db.start_transaction()

        cursor = db.cursor()
        cursor.execute(
            "UPDATE diagnostico SET decisaoCliente = %s, dataDecisao = %s WHERE idOS = %s",
            (dados.decisao, datetime.now().date(), id),
        )
        cursor.close()

        if dados.decisao == "Aprovado":
            if not gestor_os.alterar_estado_em_transacao(id, "Em Reparação"):
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Transição de estado inválida para OS {id}.")
            db.commit()
            return {"message": "Decisão registada. OS avançou para 'Em Reparação'."}
        else:
            if not gestor_os.alterar_estado_em_transacao(id, "Cancelada"):
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Transição de estado inválida para OS {id}.")
            gestor_pagamentos.criar_fatura_em_transacao(
                id_os=dados_fatura["id_os"],
                pecas=dados_fatura["pecas"],
                total_mao_obra=dados_fatura["mao_de_obra"],
                tipo_pagamento="dinheiro",
            )
            db.commit()
            return {"message": "Decisão registada. OS cancelada."}

    except HTTPException:
        try: db.rollback()
        except Exception: pass
        raise
    except Exception:
        try: db.rollback()
        except Exception: pass
        raise


@router.put("/{id}/resposta")
def completar_os(
    id: int,
    dados: OS_STATE,
    db=Depends(get_db),
    _=Depends(requer_operacao("editarOS")),
):
    if dados.estado not in ("Cancelada", "Aguarda Faturação"):
        raise HTTPException(
            status_code=400,
            detail="Estado inválido para finalização.",
        )

    gestor_os = GestorOrdensDeServico(OrdemDeServicoDAO(db), IntervencaoDAO(db), DiagnosticoDAO(db))
    gestor_pagamentos = GestorPagamentos(db)

    dados_fatura = gestor_os.preparar_dados_finalizacao(id, dados.estado)
    if dados_fatura is None:
        raise HTTPException(status_code=404, detail=f"Ordem de Serviço com ID {id} não encontrada.")

    try:
        try:
            db.rollback()
        except Exception:
            pass
        db.start_transaction()

        if not gestor_os.alterar_estado_em_transacao(id, dados.estado):
            db.rollback()
            raise HTTPException(status_code=400, detail="Transição de estado inválida.")

        id_fatura = gestor_pagamentos.criar_fatura_em_transacao(
            id_os=dados_fatura["id_os"],
            pecas=dados_fatura["pecas"],
            total_mao_obra=dados_fatura["mao_de_obra"],
            tipo_pagamento=dados.tipo_pagamento,
        )

        db.commit()
        return {"message": "OS finalizada com sucesso!", "id_fatura": id_fatura}

    except HTTPException:
        try:
            db.rollback()
        except Exception:
            pass
        raise
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
        raise


@router.put("/{id}/intervencao")
def registar_intervencao(
    id: int,
    dados: IntervencaoCreate,
    db=Depends(get_db),
    user=Depends(get_utilizador_atual),
    _=Depends(requer_operacao("editarOS")),
):
    gestor_os = GestorOrdensDeServico(OrdemDeServicoDAO(db), IntervencaoDAO(db), DiagnosticoDAO(db))
    gestor_stock = GestorStock(PecaDAO(db))

    # Validate inputs and build part map before opening the transaction
    custo_pecas = 0.0
    pecas_formatadas = {}
    for p_id, p_qt in dados.pecas.items():
        if not isinstance(p_qt, dict) or "quantidade" not in p_qt:
            raise HTTPException(status_code=400, detail=f"Formato inválido para peça {p_id}. Esperado: {{\"quantidade\": int}}.")
        quantidade = p_qt["quantidade"]
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise HTTPException(status_code=400, detail=f"Quantidade inválida para peça {p_id}. Deve ser um inteiro positivo.")
        peca = gestor_stock.consultarStock(p_id)
        if not peca:
            raise HTTPException(status_code=404, detail=f"Erro: Peça com id {p_id} não existe.")
        preco_unitario = float(peca.preco)
        custo_pecas += preco_unitario * quantidade
        pecas_formatadas[p_id] = {"quantidade": quantidade, "preco_unitario": preco_unitario}

    os_atual = gestor_os.consultar_os(id)
    if not os_atual:
        raise HTTPException(status_code=404, detail="Erro: OS não existe.")
    if os_atual.estado != "Em Reparação":
        raise HTTPException(status_code=400, detail="Erro: A OS não está no estado 'Em Reparação'.")

    custo_total = custo_pecas + dados.tempo * GestorOrdensDeServico.TAXA_MAO_OBRA

    nova_intervencao = IntervencaoModel(
        -1, dados.descricao, dados.tempo, datetime.now(),
        id, user["id_utilizador"], custo_total, pecas_formatadas,
    )

    try:
        try:
            db.rollback()
        except Exception:
            pass
        db.start_transaction()
        cursor = db.cursor()

        # Lock each part row and re-verify stock inside the transaction
        for p_id, p_info in pecas_formatadas.items():
            cursor.execute("SELECT stock FROM pecas WHERE id = %s FOR UPDATE", (int(p_id),))
            row = cursor.fetchone()
            if row is None:
                db.rollback()
                raise HTTPException(status_code=404, detail=f"Erro: Peça com id {p_id} não existe.")
            if row[0] < p_info["quantidade"]:
                db.rollback()
                peca = gestor_stock.consultarStock(p_id)
                nome = peca.nome if peca else str(p_id)
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para '{nome}' (disponível: {row[0]}).")

        # Insert intervention and decrement stock atomically
        IntervencaoDAO(db).inserir_sem_commit(nova_intervencao, cursor)
        for p_id, p_info in pecas_formatadas.items():
            cursor.execute(
                "UPDATE pecas SET stock = stock - %s WHERE id = %s",
                (p_info["quantidade"], int(p_id)),
            )

        cursor.close()
        db.commit()
        return {"message": "Intervenção criada com sucesso!"}

    except HTTPException:
        try:
            db.rollback()
        except Exception:
            pass
        raise
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
        raise


@router.put("/{id}/diagnostico")
def registar_diagnostico(
    id: int,
    dados: DiagnosticoCreate,
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    gestor_stock: GestorStock = Depends(_gestor_stock),
    user=Depends(get_utilizador_atual),
    _=Depends(requer_operacao("editarOS")),
):
    custo_pecas = 0
    pecas_formatadas = {}

    for p_id, p_qt in dados.pecas.items():
        if not isinstance(p_qt, int) or p_qt <= 0:
            raise HTTPException(status_code=400, detail=f"Quantidade inválida para peça {p_id}. Deve ser um inteiro positivo.")
        peca = gestor_stock.consultarStock(p_id)
        if not peca:
            raise HTTPException(status_code=404, detail=f"Erro: Peça com id {p_id} não existe.")

        preco_unitario = float(peca.preco)
        custo_pecas += preco_unitario * p_qt
        pecas_formatadas[p_id] = {
            "quantidade": p_qt,
            "preco_unitario": preco_unitario,
        }

    sucesso = gestor_os.criar_diagnostico(
        id, user["id_utilizador"], dados.descricao, custo_pecas, pecas_formatadas, dados.tempo_estimado
    )

    match sucesso:
        case -1:
            raise HTTPException(status_code=404, detail=f"Erro: OS com ID {id} não existe.")
        case -2:
            raise HTTPException(status_code=400, detail="Erro ao criar diagnóstico.")
        case -3:
            raise HTTPException(status_code=400, detail="Erro: A OS não está em 'Aguarda Diagnóstico'.")
        case _:
            return {"message": "Diagnóstico criado com sucesso!"}


@router.get("/{id}/detalhes")
def get_detalhes_completos(
    id: int,
    gestor_os: GestorOrdensDeServico = Depends(_gestor_os),
    _=Depends(requer_operacao("lerOS")),
):
    detalhes = gestor_os.obter_detalhes_completos_os(id)
    if not detalhes:
        raise HTTPException(status_code=404, detail=f"Ordem de Serviço com ID {id} não encontrada.")
    return detalhes
