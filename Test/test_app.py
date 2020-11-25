import unittest
from app import app, sanitize_seed


# All paths have be adjusted, otherwise these tests wont work
class MyTestCase(unittest.TestCase):
    # builds the api for each test case
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # destroys the api after each test runs
    def tearDown(self):
        pass

    # Tests the Index for the API, returns code 200
    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # This test only works if you go to the prediction method in app.py and change all of the dirs to ../<dir>
    # Should return code 200
    def test_predict(self):
        form = {"seed": "hello", "author": "shakespeare", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_sanitize_seed_shakespeare(self):
        seed = sanitize_seed("shakespeare", "hello")
        self.assertEqual(seed, "hello")

    def test_sanitize_seed_poe(self):
        seed = sanitize_seed("poe", "HELLO")
        self.assertEqual(seed, "hello")


if __name__ == '__main__':
    unittest.main()
