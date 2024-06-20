from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Dicionário para acumular os dados recebidos
dic = {
    "id": '',
    "horario": [],
    "consumo": []
}

@app.route('/api/dados', methods=['POST'])
def receber_dados():
    dados = request.json
    # print("Dados recebidos:", dados)
    
    # Acumula os dados recebidos no dicionário
    dic["id"] = dados["id"]
    dic["horario"].append(dados["horario"])
    dic["consumo"].append(dados["consumo"])
    
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
    return jsonify(dic), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
