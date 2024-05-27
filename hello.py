from flask import Flask, request, jsonify

app = Flask(__name__)

global_var = 0
def decorar_var_global():
    global global_var
    global_var += 1

@app.route("/")
def hello_world():
    decorar_var_global()
    variableExample_str = str(global_var)
    return f"<p>Tentativas: {variableExample_str}</p>"

@app.route('/measure', methods=['POST'])
def receive_weights():
    # Get JSON data from the request
    data = request.get_json()
    
    # Print the received JSON data
    print(data)
    
    # For debugging purposes, you can also log the data
    app.logger.info(data)
    
    # Respond with a success message
    return jsonify({"message": "Data received successfully"}), 200