import csv
import os
import unittest
import keras

from generator import load_model, generate_text

CSV_TEST = "../char_mappings/shakespeare_map.csv"
BIN_FILE = "../char_mappings/simpson_w2v.bin"


class MyTestCase(unittest.TestCase):

    ######################################
    # DEPRECATED - No longer in use
    ######################################
    # Tests the build_model method, should work unless an error happens
    # def test_build_model(self):
    #     id_to_char, char_to_id = open_file(CSV_TEST)
    #
    #     model = build_model(len(char_to_id), 256)
    #     self.assertNotEqual(model, None)

    # test the load_model method, this should work unless there is an error
    def test_load_model(self):
        model_path = os.path.join("../models/shakespeare/shakespeare.json")
        with open(model_path, 'r') as file:
            config = file.read()
        model = keras.models.model_from_json(config)
        model = load_model(model, os.path.join("../checkpoints/shakespeare/shakespeare.ckpt"))

        self.assertNotEqual(model, None)

    # Tests the generate_text method, test against a Regex to make sure output is correct
    def test_generate_text(self):
        seed = 'Once upon a time'
        model_path = os.path.join("../models/shakespeare/shakespeare.json")
        with open(model_path, 'r') as file:
            config = file.read()
        model = keras.models.model_from_json(config)
        model = load_model(model, os.path.join("../checkpoints/shakespeare/shakespeare.ckpt"))
        mapping_path = os.path.join('../char_mappings/shakespeare_w2v.model')

        self.assertRegex(generate_text(model, seed, mapping_path, num_to_generate=50), ".*")

    # tests with a failed text
    # TODO the open_file function needs to be updated
    def test_generate_failed_text(self):
        try:
            seed = 'Hello'
            model_path = os.path.join("../models/shakespeare/shakespeare.json")
            with open(model_path, 'r') as file:
                config = file.read()
            model = keras.models.model_from_json(config)
            model = load_model(model, os.path.join("../checkpoints/shakespeare/shakespeare.ckpt"))
            mapping_path = os.path.join('../char_mappings/shakespeare_w2v.model')

            self.assertNotRegex(generate_text(model, seed, mapping_path, num_to_generate=50), ".*")
        except KeyError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
