import json
import unittest

from app import app


class TestModels(unittest.TestCase):
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

    # This test only works if you go to the prediction method in app.py and change all of the dirs to ../<dir>
    # Should return code 200
    # this tests the shakespeare model
    def test_predict_shakespeare(self):
        form = {"seed": "Once upon a time", "author": "shakespeare", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # this tests the doyle model
    def test_predict_doyle(self):
        form = {"seed": "Sherlock Holmes", "author": "doyle", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # this tests the mckittrick model
    def test_predict_mckittrick(self):
        form = {"seed": "I", "author": "mckittrick", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # this tests the doyle model
    def test_predict_poe(self):
        form = {"seed": "Sleep", "author": "poe", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # this tests the doyle model
    def test_predict_simpsons(self):
        form = {"seed": "Homer", "author": "simpsons", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # this tests the doyle model
    def test_predict_twain(self):
        form = {"seed": "Sahara", "author": "twain", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
