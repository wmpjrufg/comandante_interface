from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Dicionário para acumular os dados recebidos, organizado por ID
dados_por_id = {}

@app.route('/api/dados', methods=['POST'])
def receber_dados():
    dados = request.json
    id = dados["id"]
    
    # Se o ID ainda não estiver no dicionário, inicializa uma nova entrada
    if id not in dados_por_id:
        dados_por_id[id] = {
            "horario": [],
            "consumo": []
        }
    
    # Acumula os dados recebidos no dicionário apropriado
    dados_por_id[id]["horario"].append(dados["horario"])
    dados_por_id[id]["consumo"].append(dados["consumo"])
    
    return jsonify(dados), 200

@app.route('/')
def index():
    return render_template_string("""
        <!doctype html>
        <title>Dados Recebidos</title>
        <h1>Dados Recebidos</h1>
        <form id="form">
            <button type="button" onclick="mostrarDados()">Mostrar Dados</button>
        </form>
        <pre id="dados"></pre>
        <script>
            function mostrarDados() {
                fetch('/dados')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('dados').innerText = JSON.stringify(data, null, 2);
                });
            }
        </script>
    """)

@app.route('/dados', methods=['GET'])
def mostrar_dados():
    return jsonify(dados_por_id), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
