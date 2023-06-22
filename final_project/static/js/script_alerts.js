// Function to show the alert-card  
function showLoading() {
    document.getElementById("alert-container").style.display = "flex";
}

const overlay = document.querySelector('.overlay');
const btnClose = document.querySelector('.btn-close');

// Hide alert-card and overlay when close button is clicked
btnClose.addEventListener('click', () => {
    document.getElementById("alert-container").style.display = "none";
    overlay.style.display = 'none';
});

function startCountdown(timeleft=5) {
    // clearInterval(countdown); // clear any existing countdown timer
    timeLeft = timeleft; // reset the timeLeft variable
    countdown = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(countdown);
            // do something when the countdown reaches 0
            document.getElementById("countdown").innerHTML = timeleft;
            document.getElementById("alert-container").style.display = "none";
        } else {
            document.getElementById("countdown").innerHTML = timeLeft;
            timeLeft--;
        }
    }, 1000); // update every 1000ms (1 second)
}


