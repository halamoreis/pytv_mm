# pytv_mm
Python HTTP Video Streamer


# Implementação de funcionalidades
Criei essa área para a gente fazer um controle do que está sendo feito e do que está pendente. Dessa forma também podemos dividir melhor as tarefas.

Server
- Transmissor.

Client
- Thread do player;
- Thread do gerenciador de download de segmentos (controle de buffer).


# Git Basics
- Ver as alterações no seu código:
git status

- Adicionar arquivos a serem posteriormente um commit:
git add nome_do_arquivo

- Fazer o commit
git commit -m "Mensagem do commit."

- Enviar o commit para o repositório:
git push origin master

- Buscar as alterações que foram feitas por commit de outros colaboradores no repositório (atualizar seu repositório com outras alterações)
git pull origin master


Lembrando que a ordem é:

1 - Adicionar arquivos;

2 - Gerar o commit;

3 - Enviar o commit ao repositório remoto (github)

Obs.: O fato de apenas gerar o commit não quer dizer que ele já foi para o repositório remoto. O seu commit só vai estar disponível para os outros colaboradores quando você efetuar o envio (comando push).
