// Função para buscar dados de um CPF na API Flask
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário, para usar AJAX

    const cpf = document.getElementById('cpf').value; // Pega o CPF do input

    // Verifica se o CPF não está vazio
    if (!cpf) {
        document.getElementById('message').textContent = 'Digite um CPF válido!';
        document.getElementById('message').style.color = 'red';
        return; // Interrompe a execução se o CPF não for válido
    }

    // Realiza a requisição para a API Flask (rota /consulta)
    fetch(`http://127.0.0.1:5000/consulta?doc=${cpf}`)
        .then(response => {
            // Verifica se a resposta foi bem-sucedida
            if (!response.ok) {
                throw new Error('Erro na requisição');
            }
            return response.json(); // Converte a resposta para JSON
        })
        .then(data => {
            // Verifica se há uma mensagem de erro (registro não encontrado)
            if (data.message) {
                document.getElementById('message').textContent = data.message;
                document.getElementById('message').style.color = 'red';
            } else {
                // Exibe os dados do cliente se encontrados
                document.getElementById('message').textContent = `
                    Nome: ${data.nome}, 
                    Data de Nascimento: ${data.data_nascimento}, 
                    E-mail: ${data.email}
                `;
                document.getElementById('message').style.color = 'green';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            document.getElementById('message').textContent = 'Erro ao buscar CPF.';
            document.getElementById('message').style.color = 'red';
        });
});

