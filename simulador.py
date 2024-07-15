import threading
import requests
import time
import random
import json
import numpy as np
from datetime import datetime, timedelta

def tag_simulador(tempo, thread_id):
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
                      "id": str(thread_id),
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
        print(f"Dados enviados com sucesso pela thread {dados['id']}!")
        print("Resposta da API:", response.json())
    else:
        print(f"Falha ao enviar dados pela thread {dados['id']}")
        print("Status Code:", response.status_code)
        print("Resposta da API:", response.json())

def thread_func(url, headers, dic, i):
    """
    Função para ser executada em uma thread.
    """
    while True:
        dados_consumo = tag_simulador(i, i)
        enviar_dados(url, headers, dados_consumo)
        dic["id"] = dados_consumo["id"]  # Atualiza o id (se necessário)
        dic["horario"].append(dados_consumo["horario"])
        dic["consumo"].append(dados_consumo["consumo"])
        time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    url = "https://comandante.pythonanywhere.com/api/dados"  # URL do servidor Flask local
    headers = {
        "Content-Type": "application/json"
    }

    dic = {
        "id": '',
        "horario": [],
        "consumo": []
    }

    threads = []

    for i in range(10):
        thread = threading.Thread(target=thread_func, args=(url, headers, dic, i))
        threads.append(thread)
        thread.start()

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    print(dic)
