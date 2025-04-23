# Quiz App com inteligência artificial

O Quiz App é uma aplicação web desenvolvida com Flask que utiliza modelos de linguagem da Groq para gerar quizzes de múltipla escolha personalizados sobre qualquer tópico.

## Descrição do projeto

- Crie perguntas sobre qualquer tópico usando IA
- Escolha entre diversos modelos da Groq
- Defina o número de perguntas desejadas
- Acompanhe seu desempenho durante e após o quiz

## Ferramentas utilizadas

- Python 3.11
- Flask
- LiteLLM
- python-dotenv
- API Groq

## Configuração do ambiente

1. Clone o repositório:
   ```
   git clone https://github.com/TinyHero13/quiz_ai_generator.git
   cd quiz_ai_generator
   ```

2. Escolha uma das opções abaixo para executar:

### Docker

1. Construa a imagem Docker:
   ```bash
   docker build -t quiz_app:latest .
   ```

2. Execute o container:
   ```bash
   docker run -p 5000:5000 -e GROQ_API_KEY=sua_chave_api_aqui quiz_app:latest
   ```

   **Observações:**
   - Substitua `sua_chave_api_aqui` pela sua chave da API Groq 
   - A aplicação estará disponível em `http://localhost:5000`
 
### Instalação Local

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da API Groq 

4. Inicie o servidor Flask:
   ```
   python app.py
   ```

5. Acesse a aplicação no navegador:
   ```
   http://localhost:5000
   ```

## Como Usar

1. Selecione o modelo de IA desejado
2. Escolha o número de perguntas (padrão: 5)
3. Digite o tópico para seu quiz
4. Clique em "Iniciar Quiz"
5. Responda às perguntas e receba feedback 
6. Ao final, veja seu resultado completo com explicações


## Estrutura do Projeto

- `app.py`: Arquivo principal com a lógica do Flask e interação com a API
- `templates/`: Contém os arquivos HTML para a interface do usuário
- `static/`: CSS da aplicação

## Erros

- Se o modelo não gerar um JSON válido, tente novamente ou tente outro modelo da lista