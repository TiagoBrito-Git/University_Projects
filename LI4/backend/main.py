from Routers.auth_router import router as auth_router
from Routers.utilizadores_router import router as utilizadores_router
from Routers.trotinetes_router import router as trotinetes_router
from Routers.os_router import router as os_router
from Routers.stock_router import router as stock_router
from Routers.clientes_router import router as client_router
from Routers.faturacao_router import router as faturacao_router
from Routers.relatorio_router import router as relatorio_router

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# --- App -------------------------------------------------------------------------------
app = FastAPI(title="TrotiFix API", version="1.0.0")


# --- Permitir pedido de qualquer origem ------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Tratamento global de erros --------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro interno no servidor: {str(exc)}"}
    )

# --- Routers ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(utilizadores_router)
app.include_router(trotinetes_router)
app.include_router(os_router)
app.include_router(stock_router)
app.include_router(client_router)
app.include_router(faturacao_router)
app.include_router(relatorio_router)



# --- Health check ----------------------------------------------------------------------
@app.get("/", tags=["Sistema"])
def root():
    return {"status": "ok", "sistema": "TrotiFix API a funcionar!", "versão": "1.0.0"}

@app.get("/health", tags=["Sistema"])
def health(request: Request):
    return {"status": "ok"}