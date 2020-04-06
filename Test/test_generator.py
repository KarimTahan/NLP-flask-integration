import csv
import unittest

from generator import build_model, load_model, generate_text


class MyTestCase(unittest.TestCase):

    # Tests the build_model method, should work unless an error happens
    def test_build_model(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')

        model = build_model(len(char_to_id), 256)
        self.assertNotEqual(model, None)

    # test the load_model method, this should work unless there is an error
    def test_load_model(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')

        model = load_model(len(char_to_id), '../checkpoints/shakespeare')

        self.assertNotEqual(model, None)

# Tests the generate_text method, test against a Regex to make sure output is correct
    def test_generate_text(self):
        id_to_char, char_to_id = open_file('../char_mappings/shakespeare_map.csv')
        seed = 'Start Text '

        new_model = load_model(len(char_to_id), '../checkpoints/shakespeare')

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
