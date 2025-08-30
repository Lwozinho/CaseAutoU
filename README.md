🤖 Classificador Inteligente de Emails
Uma aplicação web que utiliza Inteligência Artificial para classificar emails e sugerir respostas automáticas, desenvolvida como solução para um desafio de projeto.

A ferramenta é capaz de receber o conteúdo de um email, processá-lo usando técnicas de NLP e um modelo da Hugging Face para determinar se ele é Produtivo (demanda uma ação) ou Improdutivo, e então gerar uma resposta coerente para o usuário.

✨ Funcionalidades
Upload Flexível: Aceita emails colados como texto ou enviados como arquivos .txt e .pdf.

Classificação com IA: Integração com a API da Hugging Face (facebook/bart-large-mnli) para realizar classificação Zero-Shot.

Respostas Inteligentes: Geração de respostas padrão de forma rápida e confiável.

Interface Limpa: Frontend desenvolvido para ser simples, intuitivo e responsivo.

💻 Tecnologias Utilizadas
Backend: Python 3, Flask

Inteligência Artificial: Hugging Face API (Processamento de Linguagem Natural)

Frontend: HTML, CSS, JavaScript

Servidor de Produção: Waitress

Hospedagem: Render.com
