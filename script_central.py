import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PASTA_RELATORIOS = r"C:\Users\cftv\OneDrive\relatorios_monitoramento\diario"

REMETENTE = "suporte1.ti@emailexemplo.com.br"
DESTINATARIOS = ["informatica@emailexemplo.com.br", "cftv@emailexemplo.com.br", "coordenador.cftv@emailexemplo.com.br"]
COPIA = ["gerente.ti@emailexemplo.com.br", "gerente.cftv@emailexemplo.com.br"] 
ASSUNTO = "Auditoria Gravações CFTV" 

ASSINATURA_HTML = """
    <div style="margin-top: 25px;">
        <img src="https://i.ibb.co/tMn5RNkz/Assinatura-Neemias1.jpg" alt="Assinatura Neemias Cormino" style="width: 550px; height: auto;" />
    </div>
"""

# funcao para montar a tabela HTML
def gerar_tabela_html(dados):
    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; font-size: 12px; text-align: center; }
        table { border-collapse: collapse; width: 90%; margin: auto; }
        th { background-color: #28a745; color: white; padding: 8px; border: 1px solid #ddd; font-weight: bold; }
        td { border: 1px solid #ddd; padding: 8px; background-color: #2e2e2e; color: white; }
        .alerta-qtd { color: red; font-weight: bold; }
        .status-ok { color: #28a745; font-weight: bold; }
        .status-atrasado { color: #dc3545; font-weight: bold; }
    </style>
    </head>
    <body>
        <h4 style="text-align: center;">Auditoria Diária Discos Locais Mini PC's do CFTV</h4>
        <table>
            <tr>
                <th>CLIENTE</th>
                <th>TECNOLOGIA</th>
                <th>MAIS ANTIGA</th>
                <th>MAIS RECENTE</th>
                <th>STATUS</th> 
                <th>QUANTIDADE</th>
            </tr>
    """
    agora = datetime.now()
    for cliente, tecnologia, antiga, recente, qtd in sorted(dados):
        qtd_style = "alerta-qtd" if int(qtd) < 30 else ""
        
        status_text = "OK"
        status_class = "status-ok"
        try:
            data_recente = datetime.strptime(recente, '%d/%m/%Y %H:%M:%S')
            if (agora - data_recente) > timedelta(hours=2):
                status_text = "Atrasado"
                status_class = "status-atrasado"
        except (ValueError, TypeError): 
            status_text = "Inválido"
            status_class = "status-atrasado"
            
        html += f"""
            <tr>
                <td>{cliente}</td>
                <td>{tecnologia}</td>
                <td>{antiga}</td>
                <td>{recente}</td>
                <td class="{status_class}">{status_text}</td> 
                <td class="{qtd_style}">{qtd}</td>
            </tr>
        """

    html += f"""
        </table>
        {ASSINATURA_HTML}
    </body>
    </html>
    """
    return html

def enviar_email_diario(html):
    msg = MIMEMultipart('alternative')
    msg['From'] = REMETENTE
    msg['To'] = ", ".join(DESTINATARIOS)
    msg['Cc'] = ", ".join(COPIA)
    msg['Subject'] = ASSUNTO
    msg.attach(MIMEText(html, 'html'))
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as servidor:
            servidor.starttls()
            servidor.login(REMETENTE, "senha") 
            servidor.send_message(msg)
        print(f"Email '{ASSUNTO}' enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail '{ASSUNTO}': {e}")


def ler_arquivos_do_dia():
    hoje = datetime.now().strftime('%d-%m-%Y')
    dados = []
    if not os.path.exists(PASTA_RELATORIOS):
        print(f"Erro: A pasta de relatórios '{PASTA_RELATORIOS}' não foi encontrada.")
        return dados

    for nome_arquivo in os.listdir(PASTA_RELATORIOS):
        if nome_arquivo.endswith(f"-{hoje}.txt"):
            caminho_arquivo = os.path.join(PASTA_RELATORIOS, nome_arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                linha = f.read().strip()
                partes = linha.split(";")
                if len(partes) == 5:
                    dados.append(partes)
    return dados


if __name__ == "__main__":
    dados = ler_arquivos_do_dia()
    if not dados:
        print("Nenhum relatório encontrado para o dia.")
    else:
        html = gerar_tabela_html(dados)
        enviar_email_diario(html)
    # input("\nPressione ENTER para fechar...")