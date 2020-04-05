import csv
import unittest

from generator import build_model, load_model, generate_text


class MyTestCase(unittest.TestCase):

    def test_build_model(self):
        id_to_char = []

        with open('../shakespeare_map.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            char_to_id = {k: v for v, k in enumerate(id_to_char)}

        model = build_model(len(char_to_id))
        self.assertEqual(True, True)

    def test_load_model(self):
        id_to_char = []

        with open('../shakespeare_map.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            char_to_id = {k: v for v, k in enumerate(id_to_char)}

        model = load_model(len(char_to_id), '../shakespeare_checkpoint')

        self.assertEqual(True, True)

    def test_generate_text(self):
        id_to_char = []
        seed = 'Start Text '

        with open('../shakespeare_map.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            char_to_id = {k: v for v, k in enumerate(id_to_char)}

        new_model = load_model(len(char_to_id), '../shakespeare_checkpoint')

        self.assertRegex(generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=50), "Start Text .*")


if __name__ == '__main__':
    unittest.main()
