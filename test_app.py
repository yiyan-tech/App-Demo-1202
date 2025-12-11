import unittest
import os
import io
from app import app

class FileManagerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'test_files'
        if not os.path.exists('test_files'):
            os.makedirs('test_files')
        self.app = app.test_client()

    def tearDown(self):
        # Cleanup
        for f in os.listdir('test_files'):
            os.remove(os.path.join('test_files', f))
        os.rmdir('test_files')

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for Hindi title
        self.assertIn('फ़ाइल प्रबंधक'.encode('utf-8'), response.data)
        self.assertIn(b'<!DOCTYPE html>', response.data)
    
    def test_upload_file(self):
        data = {
            'file': (io.BytesIO(b'test content'), 'test.txt')
        }
        response = self.app.post('/upload', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists(os.path.join('test_files', 'test.txt')))
        self.assertIn(b'test.txt', response.data)

    def test_delete_file(self):
        # Create a file first
        with open(os.path.join('test_files', 'todelete.txt'), 'w') as f:
            f.write('content')
        
        response = self.app.get('/delete/todelete.txt', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(os.path.exists(os.path.join('test_files', 'todelete.txt')))

if __name__ == '__main__':
    unittest.main()
