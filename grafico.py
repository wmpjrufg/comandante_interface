from flask import Flask, jsonify, render_template
import numpy as np
import random
import time

app = Flask(__name__)

# Lista para armazenar os dados gerados
dados = []

# Função para gerar os dados em degraus
def gerar_degraus(n, valores_iniciais=[0.6, 0.3, 0]):
    sequencia = []
    id_sequence = random.randint(1, 5)  # Gerar um ID aleatório entre 1 e 5
    while len(sequencia) < n:
        for i in range(len(valores_iniciais) - 1):
            start = valores_iniciais[i]
            end = valores_iniciais[i+1]
            step_size = (start - end) / 10
            valores = np.linspace(start, end, num=10, endpoint=False) + np.random.uniform(-step_size, step_size, 10)
            sequencia.extend(valores)
            if len(sequencia) >= n:
                break
    sequencia = sequencia[:n]
    return {'ID': id_sequence, 'valores': sequencia}

def gerar_dado():
    dados_degraus = gerar_degraus(1)
    valor = dados_degraus['valores'][0]
    status = 'cheio'
    if valor <= 0:
        status = 'desligado'
    elif valor <= 0.2:
        status = 'necessita de reposição'
    
    return {'ID': dados_degraus['ID'], 'valor': valor, 'status': status}

@app.route('/')
def index():
    return render_template('index.html', dados=dados)

@app.route('/gerar_dado')
def gerar_e_mostrar_dado():
    novo_dado = gerar_dado()
    for dado in dados:
        if dado['ID'] == novo_dado['ID']:
            dado['valor'] = novo_dado['valor']
            dado['status'] = novo_dado['status']
            break
    else:
        dados.append(novo_dado)
    return jsonify(novo_dado)

def atualizar_dados():
    while True:
        novo_dado = gerar_dado()
        for dado in dados:
            if dado['ID'] == novo_dado['ID']:
                dado['valor'] = novo_dado['valor']
                dado['status'] = novo_dado['status']
                break
        else:
            dados.append(novo_dado)
        time.sleep(5)

if __name__ == '__main__':
    import threading
    threading.Thread(target=atualizar_dados).start()
    app.run(debug=True)
