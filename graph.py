from flask import Flask, render_template
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB connection
uri =   "mongodb+srv://sampleR:sampleR@cluster0.ljwn3ub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["quiz"]
collection = db["answers"]

@app.route('/')
def index():
    # Fetch data from MongoDB
    data = list(collection.find({}))

    # Process data for the bar graph
    chart_data = {}
    for entry in data:
        quiz_id = entry['quiz']
        username = entry['name']
        totalscore = entry['totalscore']
        if quiz_id not in chart_data:
            chart_data[quiz_id] = {}
        chart_data[quiz_id][username] = totalscore

    # Prepare data for the chart
    labels = []
    datasets = []
    for quiz_id, scores in chart_data.items():
        labels.append(quiz_id)
        scores_data = []
        for username, score in scores.items():
            scores_data.append(score)
        datasets.append({
            'label': quiz_id,
            'data': scores_data
        })

    return render_template('index.html', labels=json.dumps(labels), datasets=json.dumps(datasets))

if __name__ == '__main__':
    app.run(debug=True)
