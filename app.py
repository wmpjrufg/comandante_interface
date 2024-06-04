from flask import Flask, request, jsonify, make_response

from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#Constantes
QUANT_WEIGHT = 2 #Quantidade máxima de dados armazenados de cada mesa
MAX_TIME = 300 #seconds
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

global data_list
data_list = []

# Função para verificar e converter a data
def verify_convert_date (date_string):
    try:
        return datetime.strptime(date_string, DATE_FORMAT)
    except ValueError:
        return None

#função para remover dados antigos
def remove_oldest_data():
    #now =  datetime.today()
    now = datetime(2024, 5, 27, 12, 12)
    for table in data_list:
        for item in table['weights']:
            delay = (now - item['datetime'])
            if(delay > timedelta(seconds=MAX_TIME)):
                table['weights'].remove(item)

# remove os dados mais antigos quando atinge um limite  de dados armazenados:
def remove_excess(id):
    table = [item for item in data_list if item["id"] == id]
    table = table[0]
    print((table['weights']))
    while(len(table['weights']) > QUANT_WEIGHT):
        table['weights'].pop(0)



@app.route("/measures", methods=['GET'])
def get_all_measures():
    #print(data_list)
    return make_response(
        jsonify(data_list)
    )

@app.route('/measures', methods=['POST'])
def receive_weights():
     try:
        data = request.get_json()

        # Verificar se o JSON contém os campos esperados
        if(data['id'] != ""):
            for i in range(len(data['weights'])):
                if not all(key in data['weights'][i] for key in['datetime', 'value']):
                    raise ValueError("O JSON deve conter os campos 'datetime' e 'value'")
        
        #Converte as strings de tempo em Date
        id = data['id']
        weights = [] 
        for weight in data['weights']:
            convert_date = verify_convert_date(weight['datetime'])#converte para date

            if(convert_date != None):
                weights.append({'datetime': convert_date, 'value': weight['value'] })
            else:
                raise ValueError("Uma das datas informadas não correspondem com o formato")
            
        # Verifica se o Id já existe, se existe atualiza, caso contrário adiciona
        if(any(item['id'] == id for item in data_list)):
            for item in data_list:
                if item['id'] == id:
                    item['weights'].extend(weights)
                    break
        else:
            data_list.append({'id': id, 'weights':weights})

        remove_excess(id)

        remove_oldest_data()

        return make_response(
            jsonify( message= "Dados recebidos com sucesso", 
                     data=data), 200
        )
     except Exception as e:
        return make_response(
            jsonify({"error": str(e)}), 400
        )

app.run()