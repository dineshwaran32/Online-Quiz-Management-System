from os import abort
from flask import Flask, render_template, request, redirect, url_for, session
from bson import ObjectId

from pymongo import MongoClient
import datetime

from jinja2 import Environment

def get_len(iterable):
    return len(iterable)

app = Flask(__name__)
app.jinja_env.filters['len'] = get_len

app.secret_key = 'din123'
uri = "mongodb+srv://sampleR:sampleR@cluster0.ljwn3ub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["quiz"]
stulogin = db["stulogin"]
tealogin = db["tealogin"]
qui = db["quizzes"]
ans = db["answers"]


@app.route("/")
def admi():
    return render_template("analytics.html")
@app.route("/login", methods=['POST'])
def login():
    user = request.form['username']
    pas = request.form['password']
    for data in stulogin.find():
        if data["username"] == user and data["password"] == pas:
            return redirect('/studentdashboard')
        elif data["username"] == user and data["password"] != pas:
            return render_template("login.html", info="Invalid Password")
        else:
            for data in tealogin.find():
                if data["username"] == user and data["password"] == pas:
                    session['user'] = user
                    return redirect('/teacherdashboard')
                elif data["username"] == user and data["password"] != pas:
                    return render_template("login.html", info="Invalid Password")
            return render_template("login.html", info="Invalid Username")
        



@app.route('/teacherdashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if request.method == 'POST':
        if 'addquiz' in request.form:
            return redirect('/create_quiz')

    return render_template('teacher_dashboard.html')

@app.route('/create_quiz', methods=['POST'])
def create_quiz():
    if request.method == 'POST':
        if 'title' not in request.form:
            return render_template('create_quiz.html', error='Quiz title is required')

        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        num_questions = request.form['num_questions']
        visible_to_students = 'visible_to_students' in request.form
        start_time = request.form['start_time']

        quiz_data = {
            'title': title,
            'description': description,
            'duration': duration,
            'num_questions': num_questions,
            'visible_to_students': visible_to_students,
            'start_time': start_time,
            'questions': []
        }

        for i in range(int(num_questions)):
            question = request.form[f'question_{i+1}']
            option1 = request.form[f'option_{i+1}_1']
            option2 = request.form[f'option_{i+1}_2']
            option3 = request.form[f'option_{i+1}_3']
            option4 = request.form[f'option_{i+1}_4']
            correct_answer = request.form[f'correct_answer_{i+1}']
            score = request.form[f'score_{i+1}']

            quiz_data['questions'].append({
                'question': question,
                'options': [option1, option2, option3, option4],
                'correct_answer': correct_answer,
                'score': score
            })

        db['quizzes'].insert_one(quiz_data)
        return redirect(url_for('teacher_dashboard'))
    return render_template('create_quiz.html')

@app.route('/studentdashboard', methods=['GET', 'POST'])
def student_dashboard():
    quizzes = db['quizzes'].find()
    answered_quiz_ids = ans.distinct('quiz_id', {'username': session.get('user', '')})

    # Filter out quizzes that have been answered by the user
    quizzes = [quiz for quiz in quizzes if str(quiz['_id']) not in answered_quiz_ids]

    if request.method == 'POST':
        quiz_id = request.form['quiz_id']
        return redirect(url_for('quiz', quiz_id=quiz_id))

    return render_template('student_dashboard.html', quizzes=quizzes)


@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    quiz = qui.find_one({"_id": ObjectId(quiz_id)})
    if quiz is None:
        return "Quiz not found", 404
    questions = quiz.get("questions", [])
    return render_template('quiz.html', questions=questions, quiz_id=quiz_id)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    total = 0
    quiz_id = request.form.get('quiz_id')
    quiz = qui.find_one({"_id": ObjectId(quiz_id)})
    if quiz is None:
        return "Quiz not found", 404

    questions = quiz.get("questions", [])
    user_answers = {}
    for question in questions:
        user_answer = request.form.get(question["question"])
        user_answers[question["question"]] = user_answer
        if(question["correct_answer"] == user_answer):
            total += int(question['score'])

    
    

    ans.insert_one({
        "username": session['user'],
        "quiz_id": quiz_id,
        "answers": user_answers,
        "totalscore" : total
    })

    return redirect(url_for('quiz_results', quiz_id=quiz_id))

@app.route('/quiz_results/<quiz_id>', methods=['GET', 'POST'])
def quiz_results(quiz_id):
    username = session.get('user', '')

    answer = ans.find_one({"quiz_id": quiz_id, "username": username})

    if not answer:
        return "Quiz results not found", 404

    total_score = answer.get("answers", {}).get("Total Score", 0)

    if request.method == 'POST':
        if 'Back' in request.form:
            return redirect('/studentdashboard')

    return render_template('quiz_results.html', total_score=total_score)


if __name__ == '__main__':
    app.run(debug=True)
