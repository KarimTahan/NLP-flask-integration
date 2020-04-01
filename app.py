from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
import csv
from generator import load_model, generate_text


app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True
CORS(app)



@app.route('/')
def index():
    return render_template('Index.html')


@app.route('/prediction', methods=['POST'])
def predict():
    id_to_char = []
    char_to_id = {}
    params = {}

    if request.is_json is True:
        params = request.get_json(force=True)
    else:
        params = {'seed': request.form['seed'], 'author': request.form['author'],
                  'length': request.form['length']}
      
    seed = params['seed'] + " "
    author = params['author']
    length = int(params['length'])

    if author in 'shakespeare_map.csv':
        with open('shakespeare_map.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            char_to_id = {k: v for v, k in enumerate(id_to_char)}

    new_model = load_model(len(char_to_id), 'shakespeare_checkpoint')
    print('Generating text...')
    prediction = generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=length)
    response = make_response(jsonify(author=author, length=length, seed=seed, response=prediction), 200)
    return response


if __name__ == '__main__':
    app.run(debug=True)
