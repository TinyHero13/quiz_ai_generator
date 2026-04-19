# Quiz App with Artificial Intelligence

The Quiz App is a web application built with **Flask** that uses **Groq** language models to generate personalized multiple-choice quizzes on any topic.

---

## 📋 Project Description

- Create questions on any topic using AI
- Choose from various Groq models
- Set the desired number of questions
- Track your performance during and after the quiz

---

## 🛠️ Tools Used

| Tool | Version |
|------|---------|
| Python | 3.11 |
| Flask | — |
| LiteLLM | — |
| python-dotenv | — |
| Groq API | — |

---

## ⚙️ Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/TinyHero13/quiz_ai_generator.git
cd quiz_ai_generator
```

2. Choose one of the options below to run:

---

### 🐳 Docker

1. Build the Docker image:

```bash
docker build -t quiz_app:latest .
```

2. Run the container:

```bash
docker run -p 5000:5000 -e GROQ_API_KEY=your_api_key_here quiz_app:latest
```

> **Notes:**
> - Replace `your_api_key_here` with your Groq API key
> - The application will be available at `http://localhost:5000`

---

### 💻 Local Installation

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Configure the environment variables:
   - Create a `.env` file in the project root
   - Add your Groq API key

3. Start the Flask server:

```bash
python app.py
```

4. Access the application in your browser:

```
http://localhost:5000
```

---

## 🚀 How to Use

1. Select the desired AI model
2. Choose the number of questions *(default: 5)*
3. Enter the topic for your quiz
4. Click **"Start Quiz"**
5. Answer the questions and receive feedback
6. At the end, view your complete results with explanations

---

## 📁 Project Structure

```
quiz_ai_generator/
├── app.py           # Main file with Flask logic and API interaction
├── templates/       # HTML files for the user interface
└── static/          # Application CSS
```

---

## ⚠️ Errors

> If the model does not generate valid JSON, try again or switch to another model from the list.
