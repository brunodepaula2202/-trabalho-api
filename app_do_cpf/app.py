from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# pip install flask-cors
app = Flask("Minha API")
CORS(app)  # ativa cors para todas rotas


@app.route("/")
def home_page():
    return "Hello World!"


@app.route("/soma")
def soma():
    s = 0
    for i in range(15):
        s += i
    return f"resultado = {s}"


@app.route("/multi", methods=["GET"])
def mult():
    nome = request.args.get("nome")
    x = request.args.get("varx", type=float)
    y = request.args.get("vary")  # y será string, vou precisar converter
    y = float(y)
    resultado = x * y
    return f"Olá {nome}, o resultado = {resultado}"


@app.route("/consulta", methods=["GET"])
def consulta_cliente():
    documento = request.args.get("doc")  # Obtém o CPF enviado na requisição GET
    registro = dados(documento)  # Procura o CPF nos dados
    return jsonify(registro)  # Retorna os dados do cliente ou uma mensagem de erro



@app.route("/cadastro", methods=["POST"])
def cadastrar():
    # Pegando os dados do corpo da requisição
    valores = request.get_json()  # Aqui você usa o get_json(), não json()
    
    # Verificar se todos os campos necessários estão presentes
    if not valores or 'cpf' not in valores or 'nome' not in valores or 'data_nascimento' not in valores or 'email' not in valores:
        return jsonify({"message": "Dados incompletos. CPF, Nome, Data de Nascimento e Email são obrigatórios!"}), 400

    cpf = valores['cpf']
    salvar_dados(cpf, valores)  # Chama a função que salva os dados
    
    return jsonify({"message": f"Cadastro do CPF {cpf} realizado com sucesso!"}), 201


def carregar_arquivo():
    caminho_arquivo = "json.json"  # Caminho do arquivo JSON
    try:
        with open(caminho_arquivo, "r") as arq:
            return json.load(arq)
    except FileNotFoundError:
        return {}  # Se o arquivo não existir, retorna um dicionário vazio

def gravar_arquivo(dados):
    caminho_arquivo = "json.json"  # Caminho do arquivo JSON
    try:
        with open(caminho_arquivo, "w") as arq:
            json.dump(dados, arq, indent=4)  # Salva os dados no formato JSON com indentação
    except Exception as e:
        print("Erro ao salvar o arquivo:", e)

def salvar_dados(cpf, registro):
    dados_pessoas = carregar_arquivo()  # Carrega os dados existentes
    dados_pessoas[cpf] = registro  # Adiciona ou atualiza o registro pelo CPF
    gravar_arquivo(dados_pessoas)  # Salva os dados atualizados


def dados(cpf):
    dados_pessoas = carregar_arquivo()

    # Verifica se o CPF existe no "banco de dados"
    if cpf in dados_pessoas:
        return dados_pessoas[cpf]  # Retorna os dados do cliente como JSON
    else:
        # Se o CPF não for encontrado, retorna uma mensagem
        return {"message": "Registro não encontrado"}


if __name__ == "__main__":
    app.run(debug=True)

