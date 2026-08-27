chrome.alarms.onAlarm.addListener(function(alarm) {

    if (alarm.name.startsWith("reminder-")) {

        const parts = alarm.name.split("-");
        const reminderId = parts[1];
        const reminderTitle = parts.slice(2).join("-");

        chrome.notifications.create({
            type: "basic",
            iconUrl: "pngtree-siren-alarm-icon-png-image_1609902.jpg",
            title: "Reminder",
            message: reminderTitle
        });

        fetch(`http://127.0.0.1:8000/api/reminders/${reminderId}/`, {
            method: "DELETE"
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })


    }

});