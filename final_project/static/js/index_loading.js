
let counter = 0;
let loadingTexts = [
    "Please wait while we load...",
    "Almost complete...",
    "Process finished."
];
let interval;

// Function to show the loading screen
function showLoading() {
    document.getElementById("loading").style.display = "flex";
    interval = setInterval(changeText, 1000);
}

// Function to change the text on the loading screen
function changeText() {
    if (counter < loadingTexts.length) {
        document.getElementById("loadingText").innerHTML = loadingTexts[counter];
        counter++;
    } else {
        clearInterval(interval);
        document.getElementById("loading").style.opacity = "0";
        setTimeout(() => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("loading").style.opacity = "1";
            counter = 0;
        }, 1000);
    }
}

// Function to Submit manually
function submitForm(event) {
    event.preventDefault(); // prevent default form submission
    let loadingTexts = [
        "Reserving your table... 🍽️",
        "Preparing your spot... 🍴",
        "Almost there... 😋",
        "Bon appétit! 🥂"
    ];
    showLoading();
    setTimeout(() => {
        document.getElementById("myForm").submit(); // manually submit the form
    }, 5000); // manually submit the form
}
