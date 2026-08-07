"""
Script para gerar os três relatórios mensais manualmente (mês atual).
Uso:
    cd src
    source ../venv/bin/activate
    python gerar_relatorios.py
"""
from tasks import task_gerar_economico, task_gerar_stock, task_gerar_performance

tarefas = [
    ("Económico",   task_gerar_economico),
    ("Stock",       task_gerar_stock),
    ("Performance", task_gerar_performance),
]

print("A gerar relatórios mensais...\n")

for nome, tarefa in tarefas:
    print(f"  [{nome}] ", end="", flush=True)
    try:
        resultado = tarefa()
        if resultado.get("status") == "sucesso":
            print(f"OK (id={resultado['id']})")
        else:
            print(f"ERRO — {resultado.get('message')}")
    except Exception as e:
        print(f"EXCEÇÃO — {e}")

print("\nConcluído.")
