"""
Automated Unit Tests for CodeCraftHub REST API.
"""

import os
import unittest
from app import app, DATA_FILE


class CodeCraftHubTestCase(unittest.TestCase):
    """Test suite covering CRUD operations, statistics, and error handling."""

    def setUp(self):
        """Set up test client and isolate test environment."""
        self.app = app.test_client()
        self.app.testing = True

        # Backup existing courses.json if it exists
        if os.path.exists(DATA_FILE):
            if os.path.exists(DATA_FILE + ".bak"):
                os.remove(DATA_FILE + ".bak")
            os.rename(DATA_FILE, DATA_FILE + ".bak")

    def tearDown(self):
        """Restore original storage file after tests complete."""
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if os.path.exists(DATA_FILE + ".bak"):
            os.rename(DATA_FILE + ".bak", DATA_FILE)

    def test_create_and_get_course(self):
        """Test POST /api/courses and GET /api/courses/<id>."""
        payload = {
            "name": "Automated Testing Course",
            "description": "Learning Unittest with Flask",
            "target_date": "2026-12-31",
            "status": "In Progress"
        }
        res_post = self.app.post("/api/courses", json=payload)
        self.assertEqual(res_post.status_code, 201)
        self.assertTrue(res_post.get_json()["success"])

        res_get = self.app.get("/api/courses/1")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.get_json()["data"]["name"], "Automated Testing Course")

    def test_course_stats(self):
        """Test GET /api/courses/stats endpoint."""
        payload = {
            "name": "Stats Test Course",
            "description": "Testing statistics calculation",
            "target_date": "2026-12-31",
            "status": "Completed"
        }
        self.app.post("/api/courses", json=payload)
        
        res = self.app.get("/api/courses/stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()["data"]
        self.assertEqual(data["total_courses"], 1)
        self.assertEqual(data["by_status"]["Completed"], 1)

    def test_invalid_status_validation(self):
        """Test strict validation when providing an invalid status."""
        payload = {
            "name": "Bad Status Course",
            "description": "Testing validation",
            "target_date": "2026-12-31",
            "status": "InvalidStatus"
        }
        res = self.app.post("/api/courses", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.get_json()["success"])

    def test_course_not_found(self):
        """Test GET /api/courses/<id> with non-existent ID."""
        res = self.app.get("/api/courses/999")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()