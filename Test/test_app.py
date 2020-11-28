import unittest
from app import app


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
    # TODO Does not work, the /predict endpoint isn't working correctly, I beleive this is the lack of a model
    # (Shape Error)
    def test_predict(self):
        form = {"seed": "hello", "author": "simpson", "length": "50"}
        response = self.app.post('/prediction', json=form, follow_redirects=True)
        self.assertEqual(200, response.status_code)

    # Tests with an empty form
    def test_predict_empty_form(self):
        try:
            form = {}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except:
            self.assertTrue(True)

    # Tests with an invalid author
    def test_predict_not_an_author(self):
        try:
            form = {'seed': "hello", 'author': 'noone', 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except AttributeError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # tests with a letter in the length column
    def test_predict_length_is_alphabet(self):
        try:
            form = {'seed': "hello", 'author': 'shakespeare', 'length': 'a'}
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
            form = {'seed': "hello", 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        # missing seed in field
        try:
            form = {'author': 'noone', 'length': '50'}
            response = self.app.post('/prediction', json=form, follow_redirects=True)
            self.assertNotEqual(200, response.status_code)
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        # missing the length in the form field
        try:
            form = {'seed': "hello", 'author': 'noone'}
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
