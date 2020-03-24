from flask import Flask, render_template, request, make_response, jsonify
import csv
from generator import load_model, generate_text

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/param_input', methods=['POST'])
def get_params():
    id_to_char = []
    char_to_id = {}

    params = {'seed': request.form['seed'], 'model': request.form['model']}
    seed = params['seed'] + " "
    if params['model'] in 'shakespeare_map.csv':
        with open('shakespeare_map.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            print(id_to_char)

            char_to_id = {k: v for v, k in enumerate(id_to_char)}
            print(char_to_id)

    new_model = load_model(len(char_to_id), 'shakespeare_checkpoint')

    prediction = generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=1000)
    return make_response(jsonify(prediction), 200)


if __name__ == '__main__':
    app.run(debug=True)
