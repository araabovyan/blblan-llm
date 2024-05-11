import unittest
from unittest.mock import patch
from flask import json

from app import app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.process_request')
    def test_process_message_model1_success(self, mock_process_request):
        mock_process_request.return_value = ("Response from model 1", False)

        data = {
            'userID': '123',
            'conversationID': '456',
            'messageText': 'Hello, how are you?'
        }

        response = self.app.post('/process_message1', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Response from model 1', response.data.decode())

    @patch('app.process_request')
    def test_process_message_model2_success(self, mock_process_request):
        mock_process_request.return_value = ("Response from model 2", False)

        data = {
            'userID': '123',
            'conversationID': '789',
            'messageText': 'What is the weather today?'
        }

        response = self.app.post('/process_message2', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Response from model 2', response.data.decode())

    def test_invalid_request(self):
        response = self.app.post('/process_message1', data=json.dumps({}), content_type='application/json')

        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()