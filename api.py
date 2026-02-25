from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

ARQUIVO_VENDAS = "vendas.json"

# Função para salvar no arquivo
def salvar_venda(dados):
    registro = {
        "data_recebimento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "dados": dados
    }

    # Se arquivo não existir, cria
    if not os.path.exists(ARQUIVO_VENDAS):
        with open(ARQUIVO_VENDAS, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Lê o arquivo existente
    with open(ARQUIVO_VENDAS, "r", encoding="utf-8") as f:
        conteudo = json.load(f)

    conteudo.append(registro)

    # Salva novamente
    with open(ARQUIVO_VENDAS, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)


@app.route("/", methods=["GET", "POST"])
def api_principal():

    # Teste GET (abrir no navegador)
    if request.method == "GET":
        return jsonify({"status": "API Online 🚀"})

    # POST (Owliery envia aqui)
    try:
        dados = request.json

        print("\n===== NOVO POST RECEBIDO =====")
        print(json.dumps(dados, indent=4, ensure_ascii=False))
        print("==============================\n")

        salvar_venda(dados)

        return jsonify({"status": "Recebido e salvo com sucesso!"}), 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"error": "Erro interno"}), 500


if __name__ == "__main__":
    app.run()