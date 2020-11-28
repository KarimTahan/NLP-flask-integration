import csv
import unittest

from generator import build_model, load_model, generate_text, load_w2v

CSV_TEST = "../char_mappings/shakespeare_map.csv"
CHECKPOINT = "../checkpoints/shakespeare"
BIN_FILE = "../char_mappings/simpson_w2v.bin"


class MyTestCase(unittest.TestCase):

    # Tests the build_model method, should work unless an error happens
    # TODO Test works but I think it needs an update, seems to build off of the char2vec model
    def test_build_model(self):
        id_to_char, char_to_id = open_file(CSV_TEST)

        model = build_model(len(char_to_id), 256)
        self.assertNotEqual(model, None)am r

    # test the load_model method, this should work unless there is an error
    # TODO Test works but it works with the char2vec model
    def test_load_model(self):
        id_to_char, char_to_id = open_file(CSV_TEST)

        model = load_model(len(char_to_id), CHECKPOINT)

        self.assertNotEqual(model, None)

    # TODO Make test for load_w2v
    def test_load_w2v(self):
        self.assertTrue(False)

    # TODO Make test for word2idx
    def test_word2idx(self):
        self.assertTrue(False)

    # TODO make a test for idx2word
    def test_idx2word(self):
        self.assertTrue(False)

    # TODO make a test for sample
    def test_sample(self):
        self.assertTrue(False)

    # Tests the generate_text method, test against a Regex to make sure output is correct
    # TODO the open_file function needs to be updated to get the correct format now
    def test_generate_text(self):
        id_to_char, char_to_id = open_file(CSV_TEST)
        seed = 'Start Text '

        new_model = load_model(len(char_to_id), CHECKPOINT)

        self.assertRegex(generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=50), "Start Text .*")

    # tests with a failed tesxt
    # TODO the open_file function needs to be updated
    def test_generate_failed_text(self):
        id_to_char, char_to_id = open_file(CSV_TEST)
        seed = ''
        new_model = load_model(len(char_to_id), CHECKPOINT)

        self.assertNotRegex(generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=0), '.+')


# opens the shakespeare_map.csv file, every one of the tests methods in this class uses this
def open_file(path):
    id_to_char = []
    with open(path) as file:
        reader = csv.reader(file)
        for row in reader:
            id_to_char.append(row[1])
        char_to_id = {k: v for v, k in enumerate(id_to_char)}

        return id_to_char, char_to_id


if __name__ == '__main__':
    unittest.main()
