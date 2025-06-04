import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# configurações
PASTA_RELATORIOS = r"C:\Users\-\OneDrive-\relatorios_monitoramento_diario"
REMETENTE = "remetente.exemplo@gmail.com.br"
DESTINATARIO = "destinatario.exemplo@gmail.com.br"
COPIA = "emaildecopia.exemplo@gmail.com.br"
ASSUNTO = "Relatório Diário de Gravações"
ASSUNTO_URGENTE = "⚠️ URGENTE: Inconsistência nas Gravações"

# função para montar a tabela HTML com destaque em vermelho se < 30
def gerar_tabela_html(dados):
    html = """
    <html>
    <head>
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 12px;
            text-align: center;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: auto;
        }
        th {
            background-color: #28a745;
            color: white;
            padding: 8px;
            border: 1px solid #ddd;
            font-weight: bold;
        }
        td {
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #2e2e2e;
            color: white;
        }
        .alerta {
            color: red;
            font-weight: bold;
        }
    </style>
    </head>
    <body>
        <h4 style="text-align: center;">Auditoria Diária Discos Locais</h4>
        <table>
            <tr>
                <th>CLIENTE</th>
                <th>TECNOLOGIA</th>
                <th>MAIS ANTIGA</th>
                <th>MAIS RECENTE</th>
                <th>QUANTIDADE</th>
            </tr>
    """
    for cliente, tecnologia, antiga, recente, qtd in dados:
        qtd_style = "alerta" if int(qtd) < 30 else ""
        html += f"""
            <tr>
                <td>{cliente}</td>
                <td>{tecnologia}</td>
                <td>{antiga}</td>
                <td>{recente}</td>
                <td class="{qtd_style}">{qtd}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """
    return html

# função para verificar se há alguma gravação com mais de 2h de diferença
def verificar_gravacoes_recentes(dados):
    inconsistencias = []
    agora = datetime.now()

    for cliente, tecnologia, _, mais_recente, _ in dados:
        try:
            data_hora = datetime.strptime(mais_recente, '%d/%m/%Y %H:%M:%S')
            diferenca = agora - data_hora
            if diferenca > timedelta(hours=2):
                inconsistencias.append((cliente, tecnologia, mais_recente, diferenca))
        except ValueError:
            continue  # pula se o formato estiver errado
    return inconsistencias

# envia o e-mail com tabela normal
def enviar_email(html):
    msg = MIMEMultipart('alternative')
    msg['From'] = REMETENTE
    msg['To'] = DESTINATARIO
    msg['Cc'] = COPIA
    msg['Subject'] = ASSUNTO

    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as servidor:
            servidor.starttls()
            servidor.login(REMETENTE, '') # senha do email do remetente aqui
            servidor.send_message(msg)
        print("✅ E-mail diário enviado.")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

# envia e-mail urgente se houver inconsistência
def enviar_email_urgente(lista_inconsistencias):
    corpo = """
    <html>
    <body style="font-family: Arial; font-size: 12px; text-align: center;">
        <h3 style="color:red;">Arquivos de Gravação nos Discos Locais</h3>
        <p>Foram detectadas gravações com atraso superior a 2 horas.</p>
        <table style="margin:auto; border-collapse: collapse; width: 100%;">
            <tr style="background-color: #ff4d4d; color: white;">
                <th>CLIENTE</th>
                <th>TECNOLOGIA</th>
                <th>MAIS RECENTE</th>
                <th>DIFERENÇA</th>
            </tr>
    """
    for cliente, tecnologia, datahora, diferenca in lista_inconsistencias:
        corpo += f"""
            <tr style="background-color:#f2f2f2;">
                <td>{cliente}</td>
                <td>{tecnologia}</td>
                <td>{datahora}</td>
                <td>{str(diferenca).split('.')[0]}</td>
            </tr>
        """

    corpo += """
        </table>
        <p style="color:red;"><b>Peço que à equipe de suporte verifique o que está ocorrendo, com prioridade.</b></p>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = REMETENTE
    msg['To'] = DESTINATARIO
    msg['Cc'] = COPIA
    msg['Subject'] = ASSUNTO_URGENTE

    msg.attach(MIMEText(corpo, 'html'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as servidor:
            servidor.starttls()
            servidor.login(REMETENTE, '') # senha do email do remetente aqui
            servidor.send_message(msg)
        print("⚠️ E-mail de urgência enviado.")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail urgente: {e}")

# função para ler os arquivos .txt do dia
def ler_arquivos_do_dia():
    hoje = datetime.now().strftime('%d-%m-%Y')
    dados = []

    for nome_arquivo in os.listdir(PASTA_RELATORIOS):
        if nome_arquivo.endswith(f"{hoje}.txt"):
            caminho_arquivo = os.path.join(PASTA_RELATORIOS, nome_arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                linha = f.read().strip()
                partes = linha.split(";")
                if len(partes) == 5:
                    dados.append(partes)
    return dados

# execução principal
if __name__ == "__main__":
    dados = ler_arquivos_do_dia()
    if not dados:
        print("Nenhum relatório encontrado para o dia.")
    else:
        html = gerar_tabela_html(dados)
        enviar_email(html)

        # Verificação de urgência
        inconsistencias = verificar_gravacoes_recentes(dados)
        if inconsistencias:
            enviar_email_urgente(inconsistencias)
