from flask import Flask, request, jsonify
import pandas as pd
from github import Github
import base64

app = Flask(__name__)

# Substitui pelo teu token pessoal
GITHUB_TOKEN = "SEU_TOKEN_AQUI"
REPO_NAME = "rodrigocouras/base-dados-github-excel"
CSV_PATH = "base_dados.csv"

@app.route('/adicionar', methods=['POST'])
def adicionar():
    data = request.json

    # Liga ao GitHub
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Vai buscar o CSV atual
    file = repo.get_contents(CSV_PATH)
    content = base64.b64decode(file.content).decode()
    df = pd.read_csv(pd.compat.StringIO(content))

    # Adiciona nova linha
    df = df.append(data, ignore_index=True)

    # Converte para CSV
    new_content = df.to_csv(index=False)

    # Atualiza ficheiro no GitHub
    repo.update_file(
        path=CSV_PATH,
        message="Adição via frontend",
        content=new_content,
        sha=file.sha
    )

    return jsonify({"status": "ok", "message": "Adicionado com sucesso!"})
