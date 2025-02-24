# Log Analyzer
Fiz esse analisador de logs de segurança em Python pra identificar riscos, como tentativas de login falhas, e salvar tudo num banco SQLite. Ele tem uma interface gráfica legal pra digitar logs e ver os resultados rapidinho.

## O que ele faz
- Lê logs que você digita ou carrega de arquivos.
- Identifica logs suspeitos (tipo "failed login") e calcula o nível de risco.
- Armazena os dados num banco SQLite pra consulta futura.
- Mostra logs de alto risco em vermelho e todos os logs em cinza.
- Exporta um relatório detalhado pro Desktop com um clique.

## Como usar
1. Instale o Python 3 no seu PC.
2. Instale as bibliotecas necessárias com: `pip install customtkinter`.
3. Baixe o arquivo `log_analyzer_gui.py` e rode com `python log_analyzer_gui.py`.
4. Digite logs na área de texto (ex.: "Failed login attempt from 192.168.1.1") e clique em "Analisar Logs".

## Tecnologias
- Python 3
- SQLite (banco de dados embutido)
- customtkinter (interface gráfica moderna)

## Pra contribuir
Se quiser ajudar, melhorar ou sugerir algo, é só abrir um pull request ou criar uma issue aqui no repositório. Ideias são bem-vindas!

## Quem fez
- [Márcio Ferreira] - [www.github.com/euuCode]

## Licença
Este projeto está sob a [MIT License](LICENSE).
