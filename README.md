# Automação Auditoria CFTV - Via OneDrive

Este projeto foi desenvolvido para atender a uma necessidade real em ambiente corporativo: **monitorar as gravações salvas de sistemas de monitoramento**, como **Intelbras**, **Digifort** e **iVMS**, distribuídos em múltiplos discos locais de várias máquinas.

`Confira a versão mais atualizada desta solução em:` [n33miaz/relatorio-auditoria_gravacoes_cftv](https://github.com/n33miaz/relatorio-auditoria_gravacoes_cftv).

## Motivação

Muitas empresas utilizam sistemas de vigilância que gravam 24h por dia em discos locais. No entanto, **falhas de gravação** (como quedas de energia, problemas de rede ou HDs corrompidos) podem passar despercebidas, comprometendo exigências contratuais.

Para evitar isso, este conjunto de scripts automatiza a **Auditoria Diária**, coleta informações de cada disco e envia um **Relatório por Email**.

---

## Estrutura do Projeto

- `relatorio_*.py`  
  Analisa as pastas de acordo com a estruturação configurada de cada tecnologia de monitoramento, e extrai:
  - Data mais antiga de gravação
  - Data mais recente
  - Quantidade de dias únicos com arquivos
  Salva os dados extraidos em uma pasta local ou de uma nuvem.

- `script_central.py`  
  Responsável por:
  - Coletar os relatórios gerados no dia, salvos em pasta.
  - Montar uma **tabela HTML colorida** com os dados (verde = OK, vermelho = alerta)
  - Enviar o relatório por e-mail usando SMTP
  - Disparar um **e-mail urgente** caso a última gravação seja superior a 2 horas atrás

---

## Exemplo do Relatório

| CLIENTE | TECNOLOGIA | MAIS ANTIGA         | MAIS RECENTE         | STATUS     | QUANTIDADE |
|---------|------------|---------------------|----------------------|------------|------------|
| ACME    | Intelbras  | 01/06/2025 10:12:00 | 04/06/2025 08:30:11  |    OK      | 30          |
| EXEMPLO | Digifort   | 31/05/2025 22:01:00 | 01/06/2025 03:12:04  | ATRASADO   |    **1**   |

*Registros com menos de 30 dias ou com atraso superior a 2h geram alertas.*

---

## Como Usar

1. Configure as variáveis `CLIENTE`, `CAMINHO_BASE` e `PASTA_RELATORIOS` nos arquivos `relatorio_*.py`.
2. Agende os scripts (ex: usando o Agendador de Tarefas do Windows) para gerar os relatórios diariamente.
3. O `script_central.py` deve ser executado após os demais para consolidar os dados e enviar o e-mail.

---

## Observações de Segurança

- Os dados sensíveis foram removidos deste repositório.
- Certifique-se de **proteger sua senha de e-mail** antes de usar em produção (ex: use variáveis de ambiente ou criptografia).

---

## 🧠 Autor

Este projeto foi desenvolvido por mim como parte de uma iniciativa de automação e melhoria de processos no setor de infraestrutura e suporte técnico da empresa JC Gestão de Riscos.

---
