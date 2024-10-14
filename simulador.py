import threading
import requests
import time
import random
import json
import numpy as np
from datetime import datetime, timedelta

def tag_simulador(tempo, bateria, thread_id):
    """
    Simulador da TAG comander.
    """
    # gera um número aleatório
    r = np.random.rand()
    w_0 = .945

    # perfil de peso
    # perfil rápido
    if r < 0.5:
        lambda_r = 0.08
        peso = w_0 * np.exp(-lambda_r * tempo)
    # perfil devagar
    else:
        lambda_d = 0.1
        peso = w_0 * np.exp(-lambda_d * tempo)

    data_atual = datetime.now()
    horario = data_atual
    # horario = data_atual + timedelta(minutes=tempo)

    pacote_dados =  {
                      "id": str(thread_id),
                      "bateria": bateria,
                      "peso": round(peso,2)*100
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
    cont = 0
    bateria = 100
    while True:
        dados_peso = tag_simulador(cont, bateria, i)
        enviar_dados(url, headers, dados_peso)
        dic["id"] = dados_peso["id"]  # Atualiza o id (se necessário)
        dic["bateria"].append(dados_peso["bateria"])
        dic["peso"].append(dados_peso["peso"])
        time.sleep(random.randint(2, 5))
        if(bateria <= 0):
            bateria = 100
        else:
            bateria -= 1

        if (dados_peso["peso"] <= 5):
            cont = 0
        else:
            cont = cont + 1

if __name__ == '__main__':
    # url = "https://nilsonleao.pythonanywhere.com/api/measures"  # URL do servidor Flask local
    url = "http://127.0.0.1:5000/api/measures"
    headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer herhgydghdnsrtn3t'
    }

    dic = {
        "id": '',
        "bateria": [],
        "peso": []
    }

    threads = []

    for i in range(1,11):
        thread = threading.Thread(target=thread_func, args=(url, headers, dic, i))
        threads.append(thread)
        thread.start()

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    print(dic)