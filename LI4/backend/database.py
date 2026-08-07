import os
import threading
import mysql.connector
from mysql.connector import pooling

# Configurações da ligação à base de dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "api_user"),
    "password": os.getenv("DB_PASSWORD", "api123"),
    "database": os.getenv("DB_NAME", "scooterfix"),
    "port": int(os.getenv("DB_PORT", "3306")),
}


_pool = None
_pool_lock = threading.Lock()

def get_pool():
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = pooling.MySQLConnectionPool(
                    pool_name="scooterfix_pool",
                    pool_size=30,
                    **DB_CONFIG
                )
    return _pool

# Cede uma ligação do pool a cada pedido HTTP e garante que é devolvida no final (mesmo com erros)
def get_db():
    connection = get_pool().get_connection()
    try:
        yield connection
    finally:
        try:
            connection.rollback()  # garante que não há transação pendente ao devolver ao pool
        except Exception:
            pass
        connection.close()