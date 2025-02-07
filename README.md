# Social Network API

This project is built using Python's FastAPI framework to develop a fast and performant social network API.

## 🚀 Getting Started

You can follow the steps below to run the project.

### 📦 Requirements

- Python 3.7 or later
- pip (Python Package Manager)

### ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/memmre/SocialNetworkAPI.git
cd SocialNetworkAPI
```

2.	Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # For Linux and macOS
venv\Scripts\activate      # For Windows
```

3.	Install dependencies:
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Run

To start the application:

```bash
uvicorn main:app --reload
````

- ```main``` is the file name, ```app``` is the FastAPI instance.
- ```--reload``` option enables live reload for development environment.

## 🔗 API Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 📂 Project Structure
```bash
SocialNetworkAPI/
├── constants/
│   └── strings.py
├── helpers/
│   └── databaseHelper.py
├── routers/
│   └── root.py
├── main.py
├── README.md
├── requirements.txt
└── start.sh
```

## 📝 Sample API Requests
• GET Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/status"
```
• POST Request:
```bash
curl -X POST "http://127.0.0.1:8000/api/signInWithEmailAddressAndPassword/" -H "Content-Type: application/json" -d '{"emailAddress": "johndoe@example.com", "password": "Passw0rd!"}'
```
