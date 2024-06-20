import requests
import json
import numpy as np
from datetime import datetime, timedelta

def tag_simulador(tempo):
    """
    Simulador da TAG comander.
    """

    # gera um número aleatório
    r = np.random.rand()
    w_0 = .945

    # perfil de consumo
    # perfil rápido
    if r < 0.5:
        lambda_r = 0.08
        consumo = w_0 * np.exp(-lambda_r * tempo)
    # perfil devagar
    else:
        lambda_d = 0.1
        consumo = w_0 * np.exp(-lambda_d * tempo)

    data_atual = datetime.now()
    horario = data_atual + timedelta(minutes=tempo)

    pacote_dados =  {
                      "id": "1",
                      "horario": horario.strftime('%Y-%m-%d %H:%M:%S'),
                      "consumo": consumo
                    }
        
    return pacote_dados

def enviar_dados(url, headers, dados):
    """
    Envia os dados para a API via requisição POST.
    """
    response = requests.post(url, headers=headers, data=json.dumps(dados))
    
    if response.status_code == 200:
        print("Dados enviados com sucesso!")
        print("Resposta da API:", response.json())
    else:
        print("Falha ao enviar dados")
        print("Status Code:", response.status_code)
        print("Resposta da API:", response.json())

if __name__ == '__main__':
    url = "http://127.0.0.1:5000/api/dados"  # URL do servidor Flask local
    headers = {
        "Content-Type": "application/json"
    }

    dic = {
        "id": '',
        "horario": [],
        "consumo": []
        }

    for i in range(10):
        dados_consumo = tag_simulador(i)
        enviar_dados(url, headers, dados_consumo)
        dic["id"] = dados_consumo["id"]  # Atualiza o id (se necessário)
        dic["horario"].append(dados_consumo["horario"])
        dic["consumo"].append(dados_consumo["consumo"])
    print(dic)
