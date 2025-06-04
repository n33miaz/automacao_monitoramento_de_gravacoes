# verifica os diretórios da intelbras e gera um relatório local com data e nome do cliente
import os
from datetime import datetime

CLIENTE = "" # nome do cliente
CAMINHO_BASE = r"" # caminho do disco local até o local das gravações
PASTA_RELATORIOS = r"C:\Users\-\OneDrive\relatorios_monitoramento_diario" # caminho para a pasta da nuvem

def gerar_relatorio():
    if not os.path.exists(CAMINHO_BASE):
        return f"{CLIENTE};Intelbras;Nenhuma;Nenhuma;0"

    datas = []

    for ano in os.listdir(CAMINHO_BASE):
        for mes in os.listdir(os.path.join(CAMINHO_BASE, ano)):
            for dia in os.listdir(os.path.join(CAMINHO_BASE, ano, mes)):
                dia_path = os.path.join(CAMINHO_BASE, ano, mes, dia)
                if not os.path.isdir(dia_path): continue

                for arq in os.listdir(dia_path):
                    arq_path = os.path.join(dia_path, arq)
                    if os.path.isfile(arq_path):
                        try:
                            datas.append(datetime.fromtimestamp(os.path.getmtime(arq_path)))
                        except Exception:
                            continue

    if not datas:
        return f"{CLIENTE};Intelbras;Nenhuma;Nenhuma;0"

    data_antiga = min(datas).strftime('%d/%m/%Y %H:%M:%S')
    data_recente = max(datas).strftime('%d/%m/%Y %H:%M:%S')
    total = len(set([d.date() for d in datas]))

    return f"{CLIENTE};Intelbras;{data_antiga};{data_recente};{total}"

if __name__ == "__main__":
    hoje = datetime.now().strftime('%d-%m-%Y')
    nome_arquivo = f"{CLIENTE.replace(' ', '_')}-{hoje}.txt"
    caminho_final = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    with open(caminho_final, 'w') as f:
        f.write(gerar_relatorio())
