import csv
import unittest

from generator import build_model, load_model, generate_text, load_alt_model


class MyTestCase(unittest.TestCase):

    # Tests the build_model method, should work unless an error happens
    def test_build_model(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')

        model = build_model(len(char_to_id))
        self.assertEqual(True, True)

    # test the build_simpson_poe_model, should work unless an error happens
    def test_build_simpson_poe_model(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')

        model = build_model(len(char_to_id))
        self.assertEqual(True, True)

    # test the load_model method, this should work unless there is an error
    def test_load_model(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')

        model = load_model(len(char_to_id), '../checkpoints/shakespeare_checkpoint')

        self.assertEqual(True, True)

    # This test doesn't work for me which I don't understand since it is the same as the one before this
    def test_load_alt_model(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')

        model = load_alt_model(len(char_to_id), '../checkpoints/simpson')

        self.assertEqual(True, True)

    # Tests the generate_text method, test against a Regex to make sure output is correct
    def test_generate_text(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')
        seed = 'Start Text '

        new_model = load_model(len(char_to_id), '../checkpoints/shakespeare_checkpoint')

        self.assertRegex(generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=50), "Start Text .*")


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
