var currentQuestion = 1;
var countdown;

function startTimer(duration) {
    var timerElement = document.getElementById('timer' + currentQuestion);
    countdown = setInterval(function() {
        duration--;
        timerElement.textContent = duration;
        if (duration <= 0) {
            clearInterval(countdown);
            document.querySelector('#question' + currentQuestion + ' form').submit();
        }
    }, 1000);
}

startTimer({{ questions[0].duration }});

document.getElementById('submitButton').addEventListener('click', function() {
    clearInterval(countdown);
});

function showNextQuestion() {
    document.getElementById('question' + currentQuestion).style.display = 'none';
    currentQuestion++;
    if (currentQuestion <= {{ questions|length }}) {
        document.getElementById('question' + currentQuestion).style.display = 'block';
        startTimer({{ questions[currentQuestion - 1].duration }});
    } else {
        document.getElementById('quizForm').submit();
    }
}
