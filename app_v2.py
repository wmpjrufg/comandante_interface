from flask import Flask, request, jsonify, make_response, render_template
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Constantes
QUANT_WEIGHT = 20  # Quantidade máxima de dados armazenados de cada mesa
MAX_TIME = 300  # segundos
MAX_TIME_ALIVE = 120  # segundos
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
PASSWORD = 'herhgydghdnsrtn3t'

global data_list
data_list_json = []
alive_list = []
data_list = []

def check_password(auth_header):
    if auth_header is None or not auth_header.startswith("Bearer "):
        return 1
    token = auth_header.split(" ")[1]
    if (token != PASSWORD):
        return 0
    else:
        return 2

# função para remover dados antigos
def remove_oldest_data():
    now = datetime.today()
    for table in data_list:
        for index, horario in enumerate(table['horarios']):
            delay = (now - horario)
            if(delay > timedelta(seconds=MAX_TIME)):
                del table['horarios'][index]
                del table['pesos'][index]
                del table['bateria'][index]

def remove_not_alive():
    now = datetime.today()
    for table in alive_list:
        delay = (now - table['horario'])
        if(delay > timedelta(seconds=MAX_TIME_ALIVE)):
            del table

# remove os dados mais antigos quando atinge um limite de dados armazenados
def remove_excess(id):
    table = [item for item in data_list if item["id"] == id]
    table = table[0]
    while(len(table['pesos']) > QUANT_WEIGHT):
        table['horarios'].pop(0)
        table['pesos'].pop(0)
        table['bateria'].pop(0)

@app.route("/api/measures", methods=['GET'])
def get_all_measures():
    return make_response(
        jsonify(data_list)
    )

# RECEBE OS PESOS E BATERIA DE CADA MESA
@app.route('/api/measures', methods=['POST'])
def receive_weights():
    auth_header = request.headers.get('Authorization')
    validation = check_password(auth_header)
    if(validation == 2):
        global data_list_json
        try:
            data = request.get_json()
            if(data['id'] != ""):
                chaves_necessarias = ["id", "bateria", "peso"]
                for chave in chaves_necessarias:
                    if chave not in data:
                        print(f"A chave '{chave}' está faltando.")
                        raise ValueError("O JSON deve conter os campos 'id', 'bateria' e 'peso'")
            
            id = int(data['id'])
            horarios = []
            pesos = []
            bateria = []
        
            horarios.append(datetime.today())
            pesos.append(data['peso'])
            bateria.append(data['bateria'])
                
            if(any(item['id'] == id for item in data_list)):
                for item in data_list:
                    if item['id'] == id:
                        item['horarios'].extend(horarios)
                        item['pesos'].extend(pesos)
                        item['bateria'].extend(bateria)
                        break
            else:
                data_list.append({'id': id, 'horarios': horarios, 'pesos': pesos, 'bateria': bateria})

            remove_excess(id)
            remove_oldest_data()

            data_list_ord = sorted(data_list, key=lambda item: item['id'])
            data_list_json = jsonify(data_list_ord).get_json()

            return make_response(
                jsonify(message="Dados recebidos com sucesso", data=data), 200
            )
        except Exception as e:
            return make_response(
                jsonify({"error": str(e)}), 400
            )
    else:
        if(validation == 1):
            return make_response(
                jsonify({"message": "Token ausente ou inválido"}), 401
            )
        else:
            return make_response(
                jsonify({"message": "Senha inválida"}), 401
            )

@app.route('/api/alive', methods=['POST'])
def alive_equipment():
    auth_header = request.headers.get('Authorization')
    validation = check_password(auth_header)
    if(validation == 2):
        global alive_list
        try:
            data = request.get_json()
            if(data['id'] != ""):
                chaves_necessarias = ["id", "mac"]
                for chave in chaves_necessarias:
                    if chave not in data:
                        print(f"A chave '{chave}' está faltando.")
                        raise ValueError("O JSON deve conter os campos 'id' e 'mac'")
            
            id = int(data['id'])
            horario = datetime.today()
            mac = data['mac']
                
            if(any(item['id'] == id for item in alive_list)):
                for item in alive_list:
                    if item['id'] == id:
                        item['horario'] = horario
                        item['mac'] = mac
                        break
            else:
                alive_list.append({'id': id, 'mac': mac, 'horario': horario})

            remove_not_alive()
            return make_response(
                jsonify(message="Dados recebidos com sucesso", data=data), 200
            )
        except Exception as e:
            return make_response(
                jsonify({"error": str(e)}), 400
            )
    else:
        if(validation == 1):
            return make_response(
                jsonify({"message": "Token ausente ou inválido"}), 401
            )
        else:
            return make_response(
                jsonify({"message": "Senha inválida"}), 401
            )

# FRONT-END ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    return render_template('index_table.html')

@app.route('/api/get_data')
def get_data():
    return jsonify(data_list_json)

if __name__ == '__main__':
    app.run(debug=True)
