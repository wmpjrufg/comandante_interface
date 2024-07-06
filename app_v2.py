from flask import Flask, request, jsonify, make_response, render_template
from flask_socketio import SocketIO, send, emit

from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
socketio = SocketIO(app)

#Constantes
QUANT_WEIGHT = 4 #Quantidade máxima de dados armazenados de cada mesa
MAX_TIME = 300 #seconds
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

global data_list
data_list_json = []
data_list = []

# Função para verificar e converter a data
def verify_convert_date (date_string):
    try:
        return datetime.strptime(date_string, DATE_FORMAT)
    except ValueError:
        return None

#função para remover dados antigos
def remove_oldest_data():
    now =  datetime.today() - timedelta(hours=0,minutes=0, seconds= 0)
    #now = datetime(2024, 5, 27, 12, 12)
    for table in data_list:
        for index, horario in enumerate(table['horarios']):
            delay = (now - horario)
            if(delay > timedelta(seconds=MAX_TIME)):
                del table['horarios'][index]
                del table['consumos'][index]

# remove os dados mais antigos quando atinge um limite  de dados armazenados:
def remove_excess(id):
    table = [item for item in data_list if item["id"] == id]
    table = table[0]
    #print((table['consumos']))
    while(len(table['consumos']) > QUANT_WEIGHT):
        table['horarios'].pop(0)
        table['consumos'].pop(0)



@app.route("/measures", methods=['GET'])
def get_all_measures():
    #print(data_list)
    return make_response(
        jsonify(data_list)
    )



@app.route('/measures', methods=['POST'])
def receive_weights():
     global data_list_json
     try:
        data = request.get_json()
        #print(data)
        # Verificar se o JSON contém os campos esperados

        if(data['id'] != ""):
            chaves_necessarias = ["id", "horario", "consumo"]
            for chave in chaves_necessarias:
                if chave not in data:
                    print(f"A chave '{chave}' está faltando.")
                    raise ValueError("O JSON deve conter os campos 'id', 'horario' e 'consumo'")
        
        #Converte as strings de tempo em Date
        id = int(data['id'])
        horarios = []
        consumos = []
       
        convert_date = verify_convert_date(data['horario'])#converte para date

        if(convert_date != None):
            horarios.append(convert_date)
            consumos.append(data['consumo'])
        else:
            raise ValueError("Uma das datas informadas não correspondem com o formato")
            
        # Verifica se o Id já existe, se existe atualiza, caso contrário adiciona
        if(any(item['id'] == id for item in data_list)):
            for item in data_list:
                if item['id'] == id:
                    item['horarios'].extend(horarios)
                    item['consumos'].extend(consumos)
                    break
        else:
            data_list.append({'id': id, 'horarios':horarios, 'consumos': consumos})

        remove_excess(id)

        remove_oldest_data()
        #Tratando lista e enviando
        #data_list =  dict(sorted(data_list.items(), key=lambda item: item[1]['id']))
        print('dados:')
        
        data_list_ord = sorted(data_list, key=lambda item: item['id'])
        print(data_list_ord)
        data_list_json = jsonify(data_list_ord).get_json()
        socketio.emit('message', data_list_json) #envia os dados assim q eles são atualizados
        #print(data_list_json)
        return make_response(
            jsonify( message= "Dados recebidos com sucesso", 
                     data=data), 200
        )
     except Exception as e:
        return make_response(
            jsonify({"error": str(e)}), 400
        )


@app.route('/')
def index():
    # return render_template('teste_mesas_icon.html')
    return render_template('teste_garrafa_css.html')

@socketio.on('connect')
def handle_connect():
    global data_list_json
    print('Client connected')
    #print(data_list_json)
    emit('message', data_list_json)  # Envia a mensagem ao cliente


if __name__ == '__main__':
    socketio.run(app, debug=True)