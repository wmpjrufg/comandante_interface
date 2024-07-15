# DOCUMENTAÇÃO DA API COMMANDER

A princípio a API terá dois endpoint POST para recebimento de dados dos ESP

## POST para id da mesa, peso e bateria

Acesso: URL/api/measures

Método: POST

É necessário informar no cabeçalho da requisição os seguintes parâmetros:

    "Content-Type": "application/json",
    "Authorization": "Bearer senha-api"

Onde a 'senha-api' será fixa, seu valor é:

    herhgydghdnsrtn3t

O corpo da requisição deverá conter os seguintes campos:

    {
        "id": int,
        "bateria": int,
        "peso": int
    }

O id deve ser um número inteiro e tanto o peso quanto a bateria deverão ser inteiros e estar em um intervalo entre 0 e 100, ou seja, as porcentagens.

Exemplo de corpo para envio:

        {
            "id": 1,
            "bateria": 87,
            "peso": 78
        }

## Post id e endereço MAC

Acess: URL/api/alive

Método: POST

É necessário informar no cabeçalho da requisição os seguintes parâmetros:

    ```
    "Content-Type": "application/json",
    "Authorization": "Bearer senha-api"
    ```

Onde a 'senha-api' será fixa, seu valor é:

        herhgydghdnsrtn3t

O corpo da requisição deve conter os seguintes campos:

        {
            "id": int,
            "mac":""
        }

Onde id deve ser um número inteiro e mac deve ser uma string contendo o Endereço MAC do dispositivo.

Exemplo de corpo para envio:

        {
            "id": 1,
            "mac":"00:1B:C9:4B:E3:57"
        }
