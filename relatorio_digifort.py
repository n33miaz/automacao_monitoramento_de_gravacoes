# verifica os diretórios da digifort e gera um relatório local com data e nome do cliente
import os
from datetime import datetime

CLIENTE = "" # nome do cliente
CAMINHO_BASE = r"" # caminho do disco local até o local das gravações
PASTA_RELATORIOS = r"C:\Users\cftv\OneDrive\relatorios_monitoramento_diario" # caminho para a pasta da nuvem

def gerar_relatorio():
    datas = []

    for camera in os.listdir(CAMINHO_BASE):
        camera_path = os.path.join(CAMINHO_BASE, camera, "Dados")
        if not os.path.isdir(camera_path): continue

        try:
            arquivos = [f for f in os.listdir(camera_path) if f.endswith(".dar")]
        except PermissionError:
            continue

        for arquivo in arquivos:
            arq_path = os.path.join(camera_path, arquivo)
            try:
                datas.append(datetime.fromtimestamp(os.path.getmtime(arq_path)))
            except Exception:
                continue

    if not datas:
        return f"{CLIENTE};Digifort;Nenhuma;Nenhuma;0"

    data_antiga = min(datas).strftime('%d/%m/%Y %H:%M:%S')
    data_recente = max(datas).strftime('%d/%m/%Y %H:%M:%S')
    total = len(set([d.date() for d in datas]))

    return f"{CLIENTE};Digifort;{data_antiga};{data_recente};{total}"

if __name__ == "__main__":
    hoje = datetime.now().strftime('%d-%m-%Y')
    nome_arquivo = f"{CLIENTE.replace(' ', '_')}-{hoje}.txt"
    caminho_final = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    with open(caminho_final, 'w') as f:
        f.write(gerar_relatorio())
