
function scrollToPref() {
    // Scroll to Pref
    document.getElementById("pref").scrollIntoView({ behavior: "smooth" });
    $('html, body').animate({
        scrollTop: $('#pref').offset().top
    }, 1000);
}

function scrollToRes() {
    //Scroll to Reservation  
    document.getElementById("reserve").scrollIntoView({ behavior: "smooth" });

    $('html, body').animate({
        scrollTop: $('#reserve').offset().top
    }, 1000);
}

var time_suggested = '{{time_suggested}}';
if (time_suggested) {
    scrollToPref()
} else {
    scrollToRes()
}

$(function () {
    $("#datepicker").datepicker();
});
function updateTimes() {
    var breakfastStart = 8;
    var breakfastEnd = 9;
    var lunchStart = 12;
    var lunchEnd = 13;
    var dinnerStart = 18;
    var dinnerEnd = 19;

    var session = document.getElementById('sessionSelect').value;
    var startTimeSelect = document.getElementById('startTimeSelect');
    var endTimeSelect = document.getElementById('endTimeSelect');
    startTimeSelect.innerHTML = '';
    endTimeSelect.innerHTML = '';
    if (session === 'Breakfast') {
        for (var i = breakfastStart - 1; i <= breakfastEnd; i++) {
            var option1 = document.createElement('option');
            option1.value = i + ':00';
            option1.textContent = i + ':00 AM';
            startTimeSelect.appendChild(option1);
            if (i < breakfastEnd) {
                var option2 = document.createElement('option');
                option2.value = i + ':30';
                option2.textContent = i + ':30 AM';
                startTimeSelect.appendChild(option2);
            }
        }
        for (var i = breakfastStart; i <= breakfastEnd + 1; i++) {
            var option1 = document.createElement('option');
            option1.value = i + ':00';
            option1.textContent = i + ':00 AM';
            endTimeSelect.appendChild(option1);
            if (i < breakfastEnd + 1) {
                var option2 = document.createElement('option');
                option2.value = i + ':30';
                option2.textContent = i + ':30 AM';
                endTimeSelect.appendChild(option2);
            }
        }
    } else if (session === 'Lunch') {
        for (var i = lunchStart - 1; i <= lunchEnd; i++) {
            var option1 = document.createElement('option');
            var option2 = document.createElement('option');
            var hour = i % 12 || 12; // Convert 0 to 12 for proper AM/PM display

            option1.value = i + ':00';
            option1.textContent = hour + ':00 ' + (i < 12 ? 'AM' : 'PM');
            startTimeSelect.appendChild(option1);

            if (i < lunchEnd) {
                option2.value = i + ':30';
                option2.textContent = hour + ':30 ' + (i < 12 ? 'AM' : 'PM');
                startTimeSelect.appendChild(option2);
            }
        }

        for (var i = lunchStart; i <= lunchEnd + 1; i++) {
            var option1 = document.createElement('option');
            var option2 = document.createElement('option');
            var hour = i % 12 || 12; // Convert 0 to 12 for proper AM/PM display

            option1.value = i + ':00';
            option1.textContent = hour + ':00 ' + (i < 12 ? 'AM' : 'PM');
            endTimeSelect.appendChild(option1);

            if (i < lunchEnd + 1) {
                option2.value = i + ':30';
                option2.textContent = hour + ':30 ' + (i < 12 ? 'AM' : 'PM');
                endTimeSelect.appendChild(option2);
            }
        }
    }
    else if (session === 'Dinner') {
        for (var i = dinnerStart - 1; i <= dinnerEnd; i++) {
            var option1 = document.createElement('option');
            option1.value = i + ':00';
            option1.textContent = (i - 12) + ':00 PM';
            startTimeSelect.appendChild(option1);
            if (i < dinnerEnd) {
                var option2 = document.createElement('option');
                option2.value = i + ':30';
                option2.textContent = (i - 12) + ':30 PM';
                startTimeSelect.appendChild(option2);
            }
        }
        for (var i = dinnerStart; i <= dinnerEnd + 1; i++) {
            var option1 = document.createElement('option');
            option1.value = i + ':00';
            option1.textContent = (i - 12) + ':00 PM';
            endTimeSelect.appendChild(option1);
            if (i < dinnerEnd + 1) {
                var option2 = document.createElement('option');
                option2.value = i + ':30';
                option2.textContent = (i - 12) + ':30 PM';
                endTimeSelect.appendChild(option2);
            }
        }
    }
}

document.getElementById('sessionSelect').addEventListener('change', updateTimes);

// Retrieve the session value from the variable and trigger the update
var session = '{{ session|default:"" }}';
if (session) {
    document.getElementById('sessionSelect').value = session;
    updateTimes();
}
