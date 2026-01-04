// Simple timer logic
document.addEventListener('DOMContentLoaded', () => {
    let timeLeft = 600; // 10 minutes
    const timerDisplay = document.getElementById('timer');

    if (timerDisplay) {
        const interval = setInterval(() => {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;

            seconds = seconds < 10 ? '0' + seconds : seconds;

            timerDisplay.textContent = `${minutes}:${seconds}`;

            if (timeLeft <= 0) {
                clearInterval(interval);
                document.getElementById('quizForm').submit();
            }
            timeLeft--;
        }, 1000);
    }
});
