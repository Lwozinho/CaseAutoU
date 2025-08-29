
document.addEventListener('DOMContentLoaded', () => {
    
    
    const form = document.getElementById('email-form');
    const emailTextInput = document.getElementById('email-text');
    const emailFileInput = document.getElementById('email-file');
    const submitButton = document.getElementById('submit-button');
    
    const resultsArea = document.getElementById('results-area');
    const loadingSpinner = document.getElementById('loading');
    const resultContent = document.getElementById('result-content');
    
    const categoryResultP = document.getElementById('category-result');
    const responseResultP = document.getElementById('response-result');

    
    form.addEventListener('submit', async (event) => {
        
        event.preventDefault();

        
        const emailText = emailTextInput.value;
        const emailFile = emailFileInput.files[0];

        if (!emailText && !emailFile) {
            alert('Por favor, insira um texto ou faça o upload de um arquivo.');
            return;
        }

        
        resultsArea.classList.remove('hidden');
        loadingSpinner.classList.remove('hidden');
        resultContent.classList.add('hidden'); 
        submitButton.disabled = true; 

        
        const formData = new FormData();
        if (emailFile) {
            formData.append('email_file', emailFile);
        } else {
            formData.append('email_text', emailText);
        }

        try {
            
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                
                throw new Error('Ocorreu um erro no servidor. Tente novamente.');
            }

            
            const data = await response.json();

            
            categoryResultP.textContent = data.category;
            responseResultP.textContent = data.suggested_response;

        } catch (error) {
           
            categoryResultP.textContent = 'Erro';
            responseResultP.textContent = error.message;
            console.error('Erro ao processar:', error);
        } finally {
        
            loadingSpinner.classList.add('hidden');
            resultContent.classList.remove('hidden');
            submitButton.disabled = false; 
        }
    });
});