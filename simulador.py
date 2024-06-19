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


if __name__ == '__main__':
    dic = {
            "id": '',
            "horario": [],
            "consumo": []
          }
    
    for i in range(10):
        dados_consumo = tag_simulador(i)
        dic["id"] = dados_consumo["id"]  # Atualiza o id (se necessário)
        dic["horario"].append(dados_consumo["horario"])
        dic["consumo"].append(dados_consumo["consumo"])