from flask import Flask, request, jsonify, make_response
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


global data_list
data_list = []


@app.route("/measures", methods=['GET'])
def get_all_measures():
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
        
        # Verifica se o Id já existe, se existe atualiza, caso contrário atualiza
        if(any(item['id'] == data['id'] for item in data_list)):
            for item in data_list:
                if item['id'] == data['id']:
                    item.update(data)
                    break
        else:
            data_list.append(data)
        
        return make_response(
            jsonify( message= "Dados recebidos com sucesso", 
                     data=data), 200
        )
     except Exception as e:
        return make_response(
            jsonify({"error": str(e)}), 400
        )

app.run()