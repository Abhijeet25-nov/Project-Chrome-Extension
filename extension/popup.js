console.log("popup.js is running");
const form=document.getElementById("reminderForm");

const titleInput = document.getElementById("title");
const dateInput = document.getElementById("date");
const timeInput=document.getElementById("time");
const reminderList = document.getElementById("reminderList")

const today = new Date();

const year = today.getFullYear()
const month = String(today.getMonth() + 1).padStart(2, "0"); // getMonth()+1 because Jan-0,feb-1 that is why!
const day = String(today.getDate()).padStart(2, "0");

const currentDate =`${year}-${month}-${day}`;

dateInput.min = currentDate;

form.addEventListener("submit", function(event) {

    event.preventDefault();
    const selectedDate = dateInput.value;
    const selectedTime = timeInput.value;
    const selectedDateTime = new Date(
        `${selectedDate}T${selectedTime}`
    );

    const currentDateTime = new Date();
    if (selectedDateTime <= currentDateTime) {
        alert("Please select a future date and time.");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("title", titleInput.value);
    formData.append("date", dateInput.value);
    formData.append("time", timeInput.value);

    fetch("http://127.0.0.1:8000/api/reminders/", {
        method: "POST",
        body: formData
    })

    .then(response => response.json())
    .then(data => {
        console.log(data);
         
        // Reminder From Chrome will added using this reminderDateTime returns json value as id
        const reminderDateTime = new Date(
            `${dateInput.value}T${timeInput.value}`
        );
        chrome.alarms.create(`reminder-${data.id}-${titleInput.value}`, {
            when: reminderDateTime.getTime()
        });

        alert("Reminder added successfully!");
        form.reset();
        loadReminders();
    })
    .catch(error => {
        console.error(error);
        alert("Something went wrong.");
    });

});

function loadReminders() {
    fetch("http://127.0.0.1:8000/api/reminders/")
        .then(response => response.json())
        .then(data => {
            reminderList.innerHTML = "";
            data.forEach(reminder => {
                const reminderDiv = document.createElement("div");
                reminderDiv.innerHTML = `
                    <h3>${reminder.title}</h3>
                    <p>Date: ${reminder.date}</p>
                    <p>Time: ${reminder.time}</p>
                    <button
                        class="delete-btn"
                        data-id="${reminder.id}"
                        data-title="${reminder.title}">
                        Delete
                    </button>
                `;

                reminderList.appendChild(reminderDiv);

                const deleteButton = reminderDiv.querySelector(".delete-btn");
                deleteButton.addEventListener("click", function() {
                    const reminderId = deleteButton.dataset.id;
                    const reminderTitle = deleteButton.dataset.title;

                    fetch(`http://127.0.0.1:8000/api/reminders/${reminderId}/`, {
                        method: "DELETE"
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);

                        chrome.alarms.clear(
                            `reminder-${reminderId}-${reminderTitle}`
                        );

                        alert("Reminder deleted successfully!");
                        loadReminders();
                    })
                });
            });

        })

}

loadReminders();