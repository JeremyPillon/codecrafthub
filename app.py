"""
CodeCraftHub - Personalized Learning Platform REST API.

Provides full CRUD operations and statistical analytics for managing
developer learning paths using Flask and local JSON flat-file storage.
"""

from datetime import datetime
import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Constants
DATA_FILE = os.path.abspath("courses.json")
VALID_STATUSES = {"Not Started", "In Progress", "Completed"}


# ==========================================
# FILE STORAGE HELPER FUNCTIONS
# ==========================================

def _ensure_file_exists():
    """Ensure that the courses.json data file exists."""
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
        except OSError as err:
            app.logger.error(f"Error creating storage file: {err}")


def load_courses():
    """
    Read and return all courses from the JSON storage file.
    
    Returns:
        list: Collection of course dictionaries.
    """
    _ensure_file_exists()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as err:
        app.logger.error(f"Error reading JSON file: {err}")
        return []


def save_courses(courses):
    """
    Write the full list of courses back to the JSON file safely.
    
    Args:
        courses (list): List of course dictionaries to persist.
    
    Returns:
        bool: True if write succeeded, False otherwise.
    """
    _ensure_file_exists()
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(courses, file, indent=4, ensure_ascii=False)
        return True
    except OSError as err:
        app.logger.error(f"Error writing to JSON file: {err}")
        return False


def get_next_id(courses):
    """
    Determine the next auto-incrementing integer ID.
    
    Args:
        courses (list): Current list of course dictionaries.
        
    Returns:
        int: Unique integer identifier for a new course.
    """
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


# ==========================================
# REST API ENDPOINTS
# ==========================================

@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """Retrieve all tracked courses."""
    courses = load_courses()
    return jsonify({"success": True, "data": courses, "count": len(courses)}), 200


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """
    Retrieve statistics about courses.
    
    Returns:
        JSON: Total count and breakdown by status.
    """
    courses = load_courses()
    total_courses = len(courses)

    # Calculate status counts
    status_counts = {
        "Not Started": 0,
        "In Progress": 0,
        "Completed": 0
    }

    for course in courses:
        status = course.get("status")
        if status in status_counts:
            status_counts[status] += 1

    return jsonify({
        "success": True,
        "data": {
            "total_courses": total_courses,
            "by_status": status_counts
        }
    }), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Retrieve a single course by its auto-generated integer ID."""
    courses = load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)

    if not course:
        return jsonify({"success": False, "error": f"Course with ID {course_id} not found"}), 404

    return jsonify({"success": True, "data": course}), 200


@app.route("/api/courses", methods=["POST"])
def create_course():
    """Create a new course entry in the learning platform."""
    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "error": "Invalid or missing JSON payload"}), 400

    # 1. Required field check
    required_fields = ["name", "description", "target_date", "status"]
    missing = [field for field in required_fields if field not in data or not str(data[field]).strip()]
    if missing:
        return jsonify({
            "success": False,
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400

    # 2. Validate status enum value
    status = data["status"].strip()
    if status not in VALID_STATUSES:
        return jsonify({
            "success": False,
            "error": f"Invalid status '{status}'. Allowed values: {sorted(list(VALID_STATUSES))}"
        }), 400

    courses = load_courses()

    # 3. Construct course dictionary
    new_course = {
        "id": get_next_id(courses),
        "name": str(data["name"]).strip(),
        "description": str(data["description"]).strip(),
        "target_date": str(data["target_date"]).strip(),
        "status": status,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    courses.append(new_course)
    
    if not save_courses(courses):
        return jsonify({"success": False, "error": "Failed to persist data to file"}), 500

    return jsonify({"success": True, "data": new_course}), 201


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Update details or status of an existing course."""
    courses = load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)

    if not course:
        return jsonify({"success": False, "error": f"Course with ID {course_id} not found"}), 404

    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "error": "Invalid or missing JSON payload"}), 400

    # Validate status if included in request
    if "status" in data:
        status = str(data["status"]).strip()
        if status not in VALID_STATUSES:
            return jsonify({
                "success": False,
                "error": f"Invalid status '{status}'. Allowed values: {sorted(list(VALID_STATUSES))}"
            }), 400
        course["status"] = status

    # Update optional fields if provided
    for field in ["name", "description", "target_date"]:
        if field in data and str(data[field]).strip():
            course[field] = str(data[field]).strip()

    if not save_courses(courses):
        return jsonify({"success": False, "error": "Failed to persist data to file"}), 500

    return jsonify({"success": True, "data": course}), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Delete a course by its ID."""
    courses = load_courses()
    updated_courses = [c for c in courses if c["id"] != course_id]

    if len(courses) == len(updated_courses):
        return jsonify({"success": False, "error": f"Course with ID {course_id} not found"}), 404

    if not save_courses(updated_courses):
        return jsonify({"success": False, "error": "Failed to persist data to file"}), 500

    return jsonify({"success": True, "message": f"Course {course_id} deleted successfully"}), 200


if __name__ == "__main__":
    _ensure_file_exists()
    print("CodeCraftHub API is starting...")
    print(f"Data will be stored in: {DATA_FILE}")
    print("API will be available at: http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)