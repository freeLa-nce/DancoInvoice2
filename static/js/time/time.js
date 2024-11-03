let timerElement = document.getElementById('timer');
let resendButton = document.getElementById('resend-code-btn');
let timeLeft = 60;

function startTimer() {
    let timerInterval = setInterval(function() {
        timeLeft--;
        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            resendButton.disabled = false;
        }
    }, 1000);
}


resendButton.disabled = true;
startTimer();


resendButton.addEventListener('click', function() {
    timeLeft = 60;
    resendButton.disabled = true;
    
    startTimer();
});
