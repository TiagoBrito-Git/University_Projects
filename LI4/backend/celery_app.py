from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "relatorios",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]  # Adicione esta linha para registrar as tarefas
)

celery_app.conf.timezone = "Europe/Lisbon"

celery_app.conf.beat_schedule = {
    "gerar-relatorio-mensal-economico": {
        "task": "gerar_relatorio_economico_task",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
    "gerar-relatorio-mensal-stock": {
        "task": "gerar_relatorio_stock_task",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
    "gerar-relatorio-mensal-performance": {
        "task": "gerar_relatorio_performance_task",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
}