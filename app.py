from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import google.generativeai as gemini

app = Flask(__name__)
CORS(app)

gemini.configure(api_key="AIzaSyDs3p-19ZGt74zCW5rOttypCd4yeMWXLDY")
model = gemini.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/leitura', methods=['POST'])
def make_leitura():
        try:
            dados = request.json
            livros = dados.get('livros')
            prompt = f"""
            Crie um roteiro de estudo bíblico somente com os seguintes livros: {livros}.
            Caso o nome do capítulo informado exista na Bíblia, escreva da seguinte forma:
            Apresente um estudo bíblico no formato html com codificação UTF-8, sem head, sem as tags body, no seguinte formato:
            Linha 1 - Cabeçalho com a div header contendo o nome do livro bíblico e escrita centralizada,
            Linha 2 - Abaixo do Título, esceva os planos de estudo em h2, primeiro escreva "Plano de Estudo para:" e no final coloque o tempo determinado (15 dias , 1 mês ou 6 meses). Ao lado dessa frase, coloque o ícomene de um relógio que seja compatível com computadores e celulares,
            Linha 3 - Após isso, É preciso que você elabore esse estudo para diferentes períodos de leitura sendo eles: um roteiro para 15 dias , um roteiro para um mês e um roteiro para 6 meses.Mantenha essa sepração entre eles, sendo cada período em um parágrafo,
            Linha 5 - Informe a quantidade mínima de capítulos de cada livro que devem ser lidos por dia, de acordo com cada determinado período de tempo, mantenha em forma de lista ordenada os capítulos. Ao lado de cada divisão de capítulo, destaque os temas centrais de cada livros em lista ordenada.
            linha 6 - Ao final do Plano de Estudo, deixe sugestões de perguntas para reflexão de cada livro escolhido.
            NÃO GERE OBSERVAÇÕES AO USUÁRIO!! E não coloque a escrita html acima do livro bíblico.
            Caso o nome do capítulo não exista, escreva a seguinte frase: 'Não existe este capítulo na Biblía'
            NÃO GERE planos de leitura para livros que não pertencem a Bíblia Sagrada, não aceite palavras com escrita errada ou com caracteres especiais.
                    """
            resposta = model.generate_content(prompt)
            print(resposta)

            # Extrai a receita do texto da resposta
            receita = resposta.text.strip().split('\n')

            return jsonify(receita), 200

        except Exception as e:
            return jsonify({"Erro": str(e)}), 300

if __name__ == '__main__':
    app.run(debug=True)