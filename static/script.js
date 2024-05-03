const speakButtons = document.querySelectorAll('.speakButton');
const synth = window.speechSynthesis;

speakButtons.forEach((button) => {
    button.onclick = (event) => {
        const questionText = button.getAttribute('data-question');
        const optionsText = button.getAttribute('data-options');

        const utteranceQuestion = new SpeechSynthesisUtterance(questionText);
        const utteranceOptions = new SpeechSynthesisUtterance(optionsText);

        synth.speak(utteranceQuestion);
        synth.speak(utteranceOptions);

        event.preventDefault();
    };
});

document.getElementById('quizForm').addEventListener('submit', function(event) {
    const duration = parseInt(document.getElementById('duration').value);
    const numQuestions = document.querySelectorAll('.speakButton').length;

    if (numQuestions > duration * 2) {
        alert('Number of questions exceeds the allowed limit based on the duration.');
        event.preventDefault(); // Prevent form submission
    }
});
