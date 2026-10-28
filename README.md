# CodeCraftHub - Personalized Developer Learning Platform API

Welcome to **CodeCraftHub**! CodeCraftHub is a simple, lightweight RESTful API built with Python and Flask. It provides developer learners with a clean platform to track software engineering courses they want to master.

This project uses local JSON file storage (`courses.json`) instead of a traditional database, making it an ideal starter project for learning HTTP methods, JSON handling, and RESTful web development.

---

##  Features

- **Full CRUD Operations:** Create, Read, Update, and Delete courses via REST endpoints.
- **Auto-Generating File Persistence:** Data automatically persists to a local `courses.json` file.
- **Strict Data Validation:** Ensures mandatory fields exist and enforces valid status options (`Not Started`, `In Progress`, `Completed`).
- **Standardized Error Handling:** Delivers informative JSON error messages alongside appropriate HTTP status codes (`200`, `201`, `400`, `404`, `500`).
- **Zero Database Overhead:** Runs out of the box with zero external database server setup required.

---

## 🛠️ Prerequisites

Before starting, ensure you have the following installed on your machine:
- **Python 3.8+** or **Anaconda / Miniconda**
- **Git** (optional, for version control)
- **cURL** or **Postman** / **VS Code REST Client** (for API testing)

---

## 🚀 Step-by-Step Installation

### 1. Open VS Code & Open a Terminal
Open VS Code in your project folder (`codecrafthub`). Open the integrated terminal using **`Ctrl + ~`** (Windows/Linux) or **`Cmd + ~`** (macOS).

### 2. Set Up a Python Virtual Environment

**Option A: Using Standard Python**
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate

Option B: Using Anaconda

# Create Conda environment
conda create --name codecrafthub_env python=3.11 -y

# Activate Conda environment
conda activate codecrafthub_env

3. Install Dependencies
pip install -r requirements.txt

🏃 How to Run the Application
Start the Flask development server by running:
python app.py
You should see output similar to:
* Serving Flask app 'app'
 * Debug mode: on
 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
Leave this terminal window running while interacting with the API.

📚 REST API DocumentationBase URLhttp://127.0.0.1:5000Course Object SchemaEach course stored in the platform follows this structure:FieldTypeDescriptionidIntegerAuto-generated unique identifiernameStringTitle of the course (Required)descriptionStringSummary of learning objectives (Required)target_dateStringTarget completion date formatted as YYYY-MM-DD (Required)statusStringMust be: "Not Started", "In Progress", or "Completed" (Required)created_atStringAuto-generated timestamp formatted as YYYY-MM-DD HH:MM:SSEndpoints Overview1. Get All CoursesEndpoint: GET /api/coursesDescription: Returns an array of all courses tracked in the platform.Success Response (200 OK):JSON{
  "count": 1,
  "data": [
    {
      "created_at": "2026-10-28 09:00:00",
      "description": "Learn LLMs, RAG, and Agentic AI frameworks",
      "id": 1,
      "name": "Generative AI Engineering",
      "status": "In Progress",
      "target_date": "2026-12-31"
    }
  ],
  "success": true
}
2. Get Course by IDEndpoint: GET /api/courses/<id>Description: Retrieves details for a specific course by its unique integer ID.Success Response (200 OK):JSON{
  "data": {
    "created_at": "2026-10-28 09:00:00",
    "description": "Learn LLMs, RAG, and Agentic AI frameworks",
    "id": 1,
    "name": "Generative AI Engineering",
    "status": "In Progress",
    "target_date": "2026-12-31"
  },
  "success": true
}
Error Response (404 Not Found):JSON{
  "error": "Course with ID 99 not found",
  "success": false
}
3. Create a New CourseEndpoint: POST /api/coursesHeaders: Content-Type: application/jsonRequest Body Example:JSON{
  "name": "DevOps Security Fundamentals",
  "description": "Master secure CI/CD pipelines and vulnerability scanning",
  "target_date": "2026-11-30",
  "status": "Not Started"
}
Success Response (201 Created):JSON{
  "data": {
    "created_at": "2026-10-28 09:05:00",
    "description": "Master secure CI/CD pipelines and vulnerability scanning",
    "id": 2,
    "name": "DevOps Security Fundamentals",
    "status": "Not Started",
    "target_date": "2026-11-30"
  },
  "success": true
}
4. Update an Existing CourseEndpoint: PUT /api/courses/<id>Headers: Content-Type: application/jsonRequest Body Example:JSON{
  "status": "In Progress"
}
Success Response (200 OK):JSON{
  "data": {
    "created_at": "2026-10-28 09:05:00",
    "description": "Master secure CI/CD pipelines and vulnerability scanning",
    "id": 2,
    "name": "DevOps Security Fundamentals",
    "status": "In Progress",
    "target_date": "2026-11-30"
  },
  "success": true
}
5. Delete a CourseEndpoint: DELETE /api/courses/<id>Success Response (200 OK):JSON{
  "message": "Course 2 deleted successfully",
  "success": true
}
6. Get Course Statistics (Bonus Endpoint)
- **Endpoint:** `GET /api/courses/stats`
- **Description:** Returns total course counts and breakdown by completion status.
- **Success Response (200 OK):**
  ```json
  {
    "data": {
      "by_status": {
        "Completed": 1,
        "In Progress": 2,
        "Not Started": 1
      },
      "total_courses": 4
    },
    "success": true
  }
📂 Project Structure
Plaintext
codecrafthub/
│
├── app.py              # Main application containing routes and JSON persistence logic
├── courses.json        # Auto-created JSON data storage file
├── requirements.txt    # Project dependencies list (Flask)
└── README.md          # Project documentation and beginner API guide
