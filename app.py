import csv
import os
from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
from generator import load_model, generate_text


app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True
CORS(app)


@app.route('/')
def index():
    return render_template('Index.html')


@app.route('/prediction', methods=['POST'])
def predict():
    """Receive and process the POST request and provide generated text as a response"""
    id_to_char = []
    char_to_id = {}
    params = {}
    checkpoint = ''
    i = 0

    # Allow for both form and json formatted POST requests
    if request.is_json is True:
        params = request.get_json(force=True)
    else:
        params = {'seed': request.form['seed'],
                  'author': request.form['author'],
                  'length': request.form['length']}

    seed = params['seed'] + " "
    author = params['author']
    length = int(params['length'])

    # Retrieve list of available checkpoints
    checkpoints_dir = './checkpoints/'
    checkpoints = [os.path.join(checkpoints_dir, o) for o in os.listdir(checkpoints_dir)
                   if os.path.isdir(os.path.join(checkpoints_dir, o))]

    # Retrieve desired checkpoint
    for c in checkpoints:
        if author in c:
            checkpoint = c

    # Retrieve character mapping of desired author and create reverse mapping
    if author in checkpoint:
        with open('char_mappings/' + author + '_map.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            char_to_id = {k: v for v, k in enumerate(id_to_char)}

    # Load checkpoint into model
    new_model = load_model(len(char_to_id), 'checkpoints/' + author + '_checkpoint')
    print('Generating text...')

    # Generate text and return JSON in POST response
    prediction = generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=length)
    response = make_response(jsonify(author=author, length=length, seed=seed, response=prediction), 200)
    return response


if __name__ == '__main__':
    app.run(debug=True)
