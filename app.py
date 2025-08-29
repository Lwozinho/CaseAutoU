import os
import requests
import fitz  
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


API_URL_CLASSIFICATION = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
API_URL_GENERATION = "https://api-inference.huggingface.co/models/distilgpt2"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def query_huggingface(payload, api_url):
    """Função de debug máximo para fazer requisições à API da Hugging Face."""
    print(f"\n--- TENTANDO ACESSAR A URL: {api_url} ---")
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=45)
        
        if response.status_code != 200:
            print("--- RESPOSTA DE ERRO RECEBIDA DA API ---")
            print(f"Status Code: {response.status_code}")
            print("Headers da Resposta:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
            print("\nConteúdo Bruto da Resposta de Erro:")
            print(response.text)
            print("--- FIM DO DEBUG DE ERRO ---")
            return {"error": f"A API retornou um status de erro: {response.status_code}. Verifique o console do servidor."}

        return response.json()

    except requests.exceptions.RequestException as e:
        print("--- OCORREU UM ERRO NA BIBLIOTECA REQUESTS ---")
        print(f"Erro: {e}")
        print("Isso geralmente indica um problema de rede, firewall ou DNS para o Python.")
        print("--- FIM DO DEBUG DE ERRO ---")
        return {"error": f"Erro de comunicação fundamental com a API: {e}"}
def classify_text(text):
    """Classifica o texto em Produtivo ou Improdutivo com melhor tratamento de erro."""
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"]},
    }
    result = query_huggingface(payload, API_URL_CLASSIFICATION)
    
    if 'error' in result:
        print(f"DEBUG: Erro da API Hugging Face: {result['error']}") 
        if 'is currently loading' in result.get('error', ''):
            return "Modelo de IA está carregando, por favor tente novamente em 30 segundos."
        return "Erro na API de Classificação"

    if 'scores' in result:
        return result['labels'][0] 
        
    return "Resposta inesperada da API"

def generate_response(category, text):
    """Gera uma resposta baseada na categoria."""
    if category == "Improdutivo":
        return "Obrigado(a) pela mensagem! Arquivarei para referência futura."

    
    prompt = f"""
    Baseado no seguinte email classificado como 'Produtivo', escreva uma resposta curta e profissional que confirme o recebimento e informe que uma ação será tomada.

    Email: "{text}"

    Resposta Sugerida:
    """
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 50, "temperature": 0.7}
    }
    result = query_huggingface(payload, API_URL_GENERATION)
    if isinstance(result, list) and 'generated_text' in result[0]:
        
        return result[0]['generated_text'].replace(prompt, "").strip()
    return "Ação necessária. Analisando para fornecer a melhor resposta."

@app.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    email_text = ""
    if 'email_text' in request.form and request.form['email_text']:
        email_text = request.form['email_text']
    elif 'email_file' in request.files:
        file = request.files['email_file']
        if file.filename.endswith('.pdf'):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for page in doc:
                email_text += page.get_text()
        elif file.filename.endswith('.txt'):
            email_text = file.read().decode('utf-8')

    if not email_text:
        return jsonify({"error": "Nenhum texto de email fornecido."}), 400

    
    category = classify_text(email_text)

    
    suggested_response = generate_response(category, email_text)

    return jsonify({
        'category': category,
        'suggested_response': suggested_response
    })

if __name__ == '__main__':
    app.run(debug=True)