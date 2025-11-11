# verifica os diretórios da ivms e gera um relatório local com data e nome do cliente
import os
from datetime import datetime

CLIENTE = "" # nome do cliente
CAMINHO_BASE = r"" # caminho do disco local até o local das gravações
PASTA_RELATORIOS = r"C:\Users\cftv\OneDrive\relatorios_monitoramento_diario" # caminho para a pasta da nuvem

def gerar_relatorio():
    if not os.path.exists(CAMINHO_BASE):
        return f"{CLIENTE};iVMS;Nenhuma;Nenhuma;0"

    datas = []
    
    try:
        for pasta_data in os.listdir(CAMINHO_BASE):
            caminho_data = os.path.join(CAMINHO_BASE, pasta_data)
            if not os.path.isdir(caminho_data): continue

            for pasta_camera in os.listdir(caminho_data):
                caminho_camera = os.path.join(caminho_data, pasta_camera)
                if not os.path.isdir(caminho_camera): continue

                for arq in os.listdir(caminho_camera):
                    arq_path = os.path.join(caminho_camera, arq)
                    if os.path.isfile(arq_path):
                        try:
                            datas.append(datetime.fromtimestamp(os.path.getmtime(arq_path)))
                        except Exception:
                            continue
    except Exception as e:
        print(f"Erro ao ler diretórios em {CAMINHO_BASE}: {e}")
        return f"{CLIENTE};iVMS;Erro;Erro;0"

    if not datas:
        return f"{CLIENTE};iVMS;Nenhuma;Nenhuma;0"

    data_antiga = min(datas).strftime('%d/%m/%Y %H:%M:%S')
    data_recente = max(datas).strftime('%d/%m/%Y %H:%M:%S')
    total = len(set([d.date() for d in datas]))

    return f"{CLIENTE};iVMS;{data_antiga};{data_recente};{total}"

if __name__ == "__main__":
    hoje = datetime.now().strftime('%d-%m-%Y')
    nome_arquivo = f"{CLIENTE.replace(' ', '_')}-{hoje}.txt"
    caminho_final = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    with open(caminho_final, 'w') as f:
        f.write(gerar_relatorio())
