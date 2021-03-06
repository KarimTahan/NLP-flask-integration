import unittest
from app import app


# All paths have be adjusted, otherwise these tests wont work
class TestApp(unittest.TestCase):
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

    # Tests with an empty form
    def test_predict_empty_form(self):
        try:
            form = {}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # Tests with an invalid author
    def test_predict_not_an_author(self):
        try:
            form = {'seed': "hello", 'author': 'noone', 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except FileNotFoundError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # tests with a letter in the length column
    def test_predict_length_is_alphabet(self):
        try:
            form = {'seed': "Once upon a time", 'author': 'shakespeare', 'length': 'a'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except ValueError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # Tests with a missing field
    def test_predict_missing_fields(self):
        # missing author in field
        try:
            form = {'seed': "Once upon a time", 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        # missing seed in field
        try:
            form = {'author': 'shakespeare', 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        # missing the length in the form field
        try:
            form = {'seed': "Once upon a time", 'author': 'shakespeare'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # tests with an invalid seed since the seeds now need words that exist in the model
    def test_predict_invalid_seed(self):
        try:
            form = {'seed': "hello", 'author': 'shakespeare', 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

##################################################################################
# The tests below are for the char2vec model as sanitize_seed() is not used anymore
##################################################################################
#     def test_sanitize_seed_shakespeare(self):
#         seed = sanitize_seed("shakespeare", "hello")
#         self.assertEqual(seed, "hello")
#
#     def test_sanitize_seed_shakespeare_capital(self):
#         seed = sanitize_seed("shakespeare", "HELLO")
#         self.assertEqual(seed, "HELLO")
#
#     def test_sanitize_seed_shakespeare_mismatch(self):
#         seed = sanitize_seed("shakespeare", "hello")
#         self.assertNotEqual(seed, "HELLO")
#
#         seed = sanitize_seed("shakespeare", "HELLO")
#         self.assertNotEqual(seed, "hello")
#
#     def test_sanitize_seed_poe_uppercase(self):
#         seed = sanitize_seed("poe", "HELLO")
#         self.assertEqual(seed, "hello")
#
#     def test_sanitize_seed_poe_lowercase(self):
#         seed = sanitize_seed("poe", "hello")
#         self.assertEqual(seed, "hello")
#
#     def test_sanitize_seed_poe_seed_uppercase(self):
#         seed = sanitize_seed("poe", "HELLO")
#         self.assertNotEqual(seed, "HELLO")


if __name__ == '__main__':
    unittest.main()
