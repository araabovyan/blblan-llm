import unittest
from app import app  # Assuming your Flask app is named app.py

class TestChatEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_process_message(self):
        # Define the payload to send to your endpoint
        payload = {
            "userID": "123",
            "conversationID": "456",
            "messageText": "Hello, how are you?"
        }
        # Send a POST request to the endpoint with the payload
        response = self.app.post('/process_message', json=payload)
        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Optionally, check if the response contains expected data
        # self.assertIn('expected response content', response.data.decode())

if __name__ == '__main__':
    unittest.main()
