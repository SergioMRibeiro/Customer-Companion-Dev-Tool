
# Customer Companion Dev Tool

Uma ferramenta para auxiliar no dia a dia dos devs que mexem com diversos ambientes VtexIo.

## Requisitos

 - python 3
 - vtex CLI

## Rodando o projeto

Na pasta raiz execute o comando o comando abaixo apenas a primeira vez que tiver rodando o projeto para criar um virtural enviroment .
  
`$ python -m venv venv`
  
Os comandos a seguir são comuns para rodar o projeto. O próximo irá entrar na venv criada:
  
`$ venv\Scripts\activate`
`(venv)$ pip install -e .`

Dessa forma irá criar o ambiente do programa e poderá executar outros comandos como para faze-lo rodar. (OBS.: certifique de criar o arquivo configs.json caso ele não exista.)
  
`(venv)$ appStart`

Por fim, e de modo opcional, para sair da venv pode rodar o comando:

`deactivate`

## Funcionalidades do sistema

![Imagem Exemplo da Ferramenta](https://private-user-images.githubusercontent.com/68062136/345688193-6c794a67-e015-4942-a948-97bfbac2b6c4.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjAwOTk2ODMsIm5iZiI6MTcyMDA5OTM4MywicGF0aCI6Ii82ODA2MjEzNi8zNDU2ODgxOTMtNmM3OTRhNjctZTAxNS00OTQyLWE5NDgtOTdiZmJhYzJiNmM0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA3MDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNzA0VDEzMjMwM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWY3NTRjMTFjNThiNzM2OWNmOTdlZWZhYzNmNTA5NmJjNjlmMTM0MTY2Y2I5YjI2ZWFhNDc5NTBmMjRmMTFjYzMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.bHl7IKbL5lgL9y-GIl5ssacYHPeCghwF7buR7Eh1Eb4)

1.  Criar lista de vendor
2.  Acessar diferentes vendors
3.  Listar workspace existente na loja
4. Listar apps instalados
5. Verificar ambiente logado
6.  Deletar vendor da lista
7.  Exibir resultados de comandos



