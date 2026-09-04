# Chrome-Reminder Extension

A full-stack Chrome Extension for creating, managing, scheduling, and receiving reminders directly from the browser.

The project uses **Django** as the backend, **SQLite** for data storage, **JavaScript** for frontend logic, the **Chrome Extensions API** for alarms and notifications, and **Docker** for containerizing the Django backend.

---

##  Project Overview

The Reminder Chrome Extension allows users to create reminders by entering a title, date, and time.
The reminder is stored in the Django backend through an API. The Chrome Extension then schedules an alarm using the Chrome Alarms API.
When the scheduled time arrives, a background service worker displays a Chrome notification containing the reminder title.
After the notification is triggered, the completed reminder is automatically removed from the database.

---

## Features

- Create reminders with title, date, and time
- Prevent selection of past date and time
- Store reminders in a Django backend
- Display saved reminders inside the Chrome Extension
- Delete reminders manually
- Schedule reminders using Chrome Alarms API
- Display desktop notifications at the scheduled time
- Show the actual reminder title in notifications
- Automatically remove completed reminders
- Background processing using Manifest V3 Service Worker
- REST-style communication between frontend and backend
- Dockerized Django backend
- Persistent SQLite data during local Docker development

---

## Tech Stack

### Backend

- Python
- Django
- SQLite

### Frontend / Chrome Extension

- HTML
- CSS
- JavaScript
- Chrome Extension Manifest V3
- Chrome Alarms API
- Chrome Notifications API
- Service Worker - Manifest V3

### API Communication

- Fetch API
- JSON
- HTTP GET
- HTTP POST
- HTTP DELETE

### DevOps

- Docker
- Docker Desktop
- Docker Images
- Docker Containers

---

##  Project Architecture

```text
             Chrome Extension
                    | HTTP Requests
                    v
              Django Backend
                    |
                    v
              SQLite Database


         Reminder Scheduling Flow

User creates reminder
        |
        v
JavaScript validates date/time
        |
        v
POST request to Django
        |
        v
Reminder stored in SQLite
        |
        v
Chrome Alarm scheduled
        |
        v
Popup can be closed
        |
        v
Service Worker waits
        |
        v
Scheduled time arrives
        |
        v
Chrome Notification 
        |
        v
Completed reminder deleted
```

---

##  Project Structure

```text
Project-Chrome-Extension/
│
├── backend/
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── ...
│   │
│   ├── reminder/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── ...
│   │
│   ├── static/
│   ├── templates/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   └── db.sqlite3
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   ├── service_worker.js
│   └── alarm-icon.jpg
│
├── .gitignore
└── README.md
```

---

# API Endpoints

| HTTP Method | Endpoint | Description |
|-------------|----------|-------------|
| GET | `/api/reminders/` | Get all reminders |
| POST | `/api/reminders/` | Create a reminder |
| DELETE | `/api/reminders/<id>/` | Delete a reminder |

---

# ⚙️ How the Application Works

## 1. Creating a Reminder

The user enters:

```text
Title
Date
Time
```

JavaScript first checks whether the selected date and time are in the future.
If the selected time is invalid, the user receives an alert.
If it is valid, the extension sends:

```text
POST /api/reminders/
```

to the Django backend.

---

## 2. Storing the Reminder

Django receives the request and stores the reminder using the `Reminder` model.

```text
Chrome Extension
       |
       | POST
       v
Django API
       |
       v
Reminder Model
       |
       v
SQLite
```

---

## 3. Loading Reminders

Whenever the extension popup opens, JavaScript sends:

```text
GET /api/reminders/
```

Django returns the reminders as JSON.

JavaScript dynamically creates the reminder elements and displays them inside the popup.

---

## 4. Scheduling the Reminder

After successfully creating a reminder, the extension creates a Chrome alarm.

Conceptually:

```javascript
chrome.alarms.create(...)
```

The scheduled alarm continues to exist even after the extension popup is closed.

---

## 5. Background Service Worker

The extension uses a **Manifest V3 Service Worker**.

The service worker listens for Chrome alarm events.

```text
Chrome Alarm
     |
     v
service_worker.js
     |
     v
Notification
```

This allows reminders to work without keeping the extension popup open.

---

## 6. Notification

When the scheduled time arrives, Chrome displays a desktop notification.

Example:

```text
🔔 Reminder

Complete DSA Practice
```

The reminder title is extracted from the scheduled alarm information and displayed in the notification.

---

## 7. Completed Reminder Removal

After the notification is triggered, the service worker sends a DELETE request to Django.

```text
Notification triggered
       |
       v
DELETE /api/reminders/<id>/
       |
       v
Django
       |
       v
SQLite record removed
```

Therefore, completed reminders no longer appear when the popup is opened again.

---
# Preview of Extension

![Reminder Extension Preview](images/Screenshot%202026-09-04%20194559.png)

# Dockerization

The Django backend has been containerized using Docker.

The Dockerfile defines:

1. Python base image
2. Working directory
3. Python dependencies
4. Django application files
5. Application port
6. Django startup command

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## Understanding the Dockerfile

### `FROM`

```dockerfile
FROM python:3.12-slim
```

Uses Python 3.12 Slim as the base image.

### `WORKDIR`

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory inside the container.

### `COPY`

```dockerfile
COPY requirements.txt /app/
```

Copies the Python dependency file into the image.

### `RUN`

```dockerfile
RUN pip install -r requirements.txt
```

Installs the required Python packages.

### Copy Application

```dockerfile
COPY . /app/
```

Copies the Django backend into the Docker image.

### `EXPOSE`

```dockerfile
EXPOSE 8000
```

Documents that the Django application listens on port `8000`.

### `CMD`

```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Starts the Django development server when the container starts.

---

# Local Setup Without Docker

## 1. Clone the Repository

```bash
git clone https://github.com/Abhijeet25-nov/Project-Chrome-Extension.git
```

```bash
cd Project-Chrome-Extension
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
python -m pip install -r backend/requirements.txt
```

---

## 4. Run Migrations

```bash
cd backend
python manage.py migrate
```

---

## 5. Start Django

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

# Running with Docker

Make sure Docker Desktop is running.

Move into the backend directory:

```bash
cd backend
```

## 1. Build the Docker Image

```bash
docker build -t reminder-backend .
```

Where:

```text
docker build        → Build Docker image
-t                  → Assign a tag/name
reminder-backend    → Image name
.                   → Current directory as build context
```

---

## 2. Run the Container

### PowerShell

```powershell
docker run --name reminder-container -p 8000:8000 -v ${PWD}:/app reminder-backend
```

The port mapping means:

```text
Host                       Container

localhost:8000  ────────→  8000
```

The bind mount connects the local backend directory with `/app` inside the container.

---

## 3. Run Django Migrations Inside Container

In another terminal:

```bash
docker exec reminder-container python manage.py migrate
```

---

## 4. Stop Container

If running in the attached terminal:

```text
Ctrl + C
```

---

## 5. Start Existing Container Again

```bash
docker start -a reminder-container
```

---

## 6. View Containers

Running containers:

```bash
docker ps
```

All containers:

```bash
docker ps -a
```

---

## 7. Remove Container

```bash
docker rm -f reminder-container
```

---

## 8. Rebuild After Dockerfile Changes

If the Dockerfile or dependencies change:

```bash
docker build -t reminder-backend .
```

Then recreate the container from the updated image.

---

#  Installing the Chrome Extension

1. Open Google Chrome.
2. Go to `chrome://extensions/`.
3. Enable **Developer Mode**.
4. Click **Load unpacked**.
5. Select the `extension` folder.
6. Pin the extension to the Chrome toolbar.

Make sure the Django backend/container is running before using the extension.

---

# Chrome Permissions

The extension uses:

```json
"permissions": [
    "alarms",
    "notifications"
]
```

### Alarms

Used to schedule an event for the reminder's selected date and time.

### Notifications

Used to display desktop notifications when the scheduled alarm fires.

The extension also requires host permission for the Django backend during local development.

---

# Future Improvements

- Deploy Django backend to a cloud platform
- Replace localhost API URLs with production HTTPS URLs
- Use PostgreSQL for production
- Add user authentication
- Add edit/update reminder functionality
- Add recurring reminders
- Add reminder categories
- Add priority levels
- Add notification customization
- Improve extension UI
- Publish the extension on Chrome Web Store

---

# Concepts Implemented

This project demonstrates practical understanding of:

- Django Models
- Django Views
- Django URL Routing
- SQLite
- CRUD operations
- REST-style APIs
- HTTP methods
- Fetch API
- Asynchronous JavaScript
- DOM manipulation
- Event listeners
- Chrome Extension Manifest V3
- Chrome Alarms API
- Chrome Notifications API
- Dockerfiles
- Docker Images
- Docker Containers
- Containerized Django applications

---

# Author

**Abhijeet**

---
