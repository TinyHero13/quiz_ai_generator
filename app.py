from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
import json
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  

LLM_MODELS = [
    {"id": "groq/gemma2-9b-it", "name": "Groq - Gemma 9B"},
    {"id": "groq/llama3-8b-8192", "name": "Groq - Llama 3 8B"},
    {"id": "groq/allam-2-7b", "name": "Groq - Allam 2 7B"},
]

def generate_questions(model, api_key, user_topic, num_questions=5):
    topic_prompt = f"Tema: {user_topic}" 
    
    prompt = f"""Gere {num_questions} perguntas de múltipla escolha sobre {topic_prompt}.
                Formate cada pergunta como um objeto JSON com os seguintes campos:
                "question": O texto da pergunta
                "options": Um array com 4 possíveis respostas rotuladas como A, B, C, D
                "correct_answer": A letra (A, B, C ou D) correspondente à resposta correta
                "explanation": Uma explicação detalhada de por que a resposta está correta
                Retorne APENAS um array JSON de objetos de perguntas, sem nenhum texto adicional.
    """

    system_prompt = "Você é um gerador de quizzes especialista. Gere perguntas de múltipla escolha precisas e educativas sobre o tema solicitado em português. Formate sua resposta como um JSON válido, sem nenhum texto adicional. "
    
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
    )
    
    content = response['choices'][0]['message']['content'].strip()
    
    if "```json" in content:
        json_content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        json_content = content.split("```")[1].strip()
    else:
        json_content = content
    
    try:
        questions = json.loads(json_content)
        return questions
    except json.JSONDecodeError:
        raise ValueError("Por favor tente novamente")

@app.route('/')
def index():
    api_key = session.get('api_key', '')
    return render_template('index.html', models=LLM_MODELS, api_key=api_key)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    model = request.form.get('model')
    api_key = request.form.get('api_key', '')
    num_questions = int(request.form.get('num_questions', 5))
    user_topic = request.form.get('topic', '').strip()
    
    session['api_key'] = api_key
    
    try:
        questions = generate_questions(model, api_key, user_topic, num_questions)
        
        session['questions'] = questions
        session['current_question'] = 0
        session['score'] = 0
        session['answers'] = []
        session['model'] = model
        session['topic'] = user_topic
        
        model_display = next((m['name'] for m in LLM_MODELS if m['id'] == model), model)
        session['model_display'] = model_display
        
        return redirect(url_for('quiz'))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/quiz')
def quiz():
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    questions = session['questions']
    current = session['current_question']
    
    if current >= len(questions):
        return redirect(url_for('results'))
    
    return render_template('quiz.html', 
                           question=questions[current],
                           question_number=current + 1,
                           total_questions=len(questions),
                           model_display=session.get('model_display'))

@app.route('/finish_quiz', methods=['POST'])
def finish_quiz():
    selected_answer = request.form.get('answer')
    
    if selected_answer:
        questions = session['questions']
        current = session['current_question']
        current_question = questions[current]
        
        is_correct = selected_answer == current_question['correct_answer']
        
        if is_correct:
            session['score'] = session.get('score', 0) + 1
        
        answer_data = {
            'question_idx': current,
            'selected': selected_answer,
            'is_correct': is_correct
        }
        session['answers'].append(answer_data)
    
    questions = session['questions']
    answered_indices = [a['question_idx'] for a in session['answers']]
    
    for i in range(len(questions)):
        if i not in answered_indices:
            answer_data = {
                'question_idx': i,
                'selected': None,
                'is_correct': False
            }
            session['answers'].append(answer_data)
    
    return redirect(url_for('results'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_answer = request.form.get('answer')
    
    if not selected_answer:
        return redirect(url_for('quiz'))
    
    questions = session['questions']
    current = session['current_question']
    current_question = questions[current]
    
    is_correct = selected_answer == current_question['correct_answer']
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    answer_data = {
        'question_idx': current,
        'selected': selected_answer,
        'is_correct': is_correct
    }
    session['answers'].append(answer_data)
    
    return render_template('question_result.html',
                          question=current_question,
                          answer=answer_data,
                          question_number=current + 1,
                          total_questions=len(questions),
                          model_display=session.get('model_display'))

@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
    if 'current_question' not in session:
        return redirect(url_for('index'))
        
    current = session['current_question']
    session['current_question'] = current + 1
    
    return redirect(url_for('quiz'))

@app.route('/results')
def results():
    if 'questions' not in session or 'answers' not in session:
        return redirect(url_for('index'))
    
    questions = session['questions']
    answers = session['answers']
    score = session['score']
    
    answers.sort(key=lambda x: x['question_idx'])
    
    return render_template('results.html', 
                           questions=questions,
                           answers=answers,
                           score=score,
                           total=len(questions),
                           model_display=session.get('model_display'))

@app.route('/restart')
def restart():
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('score', None)
    session.pop('answers', None)
    session.pop('model', None)
    session.pop('model_display', None)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)