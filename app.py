import csv
import os
from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
from generator import load_model, generate_text


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
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
    checkpoint = ''
    seed = ''

    # Allow for both form and json formatted POST requests
    print('Received request...')
    if request.is_json is True:
        params = request.get_json(force=True)
    else:
        params = {'seed': request.form['seed'],
                  'author': request.form['author'],
                  'length': request.form['length']}

    pre_seed = params['seed'] + ' '
    seed_list = pre_seed.splitlines()
    for line in seed_list:
        seed += line

    author = params['author']
    if params['length'] is not '':
        length = int(params['length'])
    else:
        length = 0

    # Retrieve list of available checkpoints
    checkpoints_dir = 'checkpoints'
    checkpoints = [os.path.join(checkpoints_dir, o) for o in os.listdir(checkpoints_dir)
                   if os.path.isdir(os.path.join(checkpoints_dir, o))]

    # Retrieve desired checkpoint
    print('Retrieving checkpoint...')
    for c in checkpoints:
        if author in c:
            checkpoint = c

    # Retrieve character mapping of desired author and create reverse mapping
    print('Retrieving mapping...')
    if author in checkpoint:
        mapping_path = os.path.join('char_mappings', author + '_map.csv')
        with open(mapping_path) as file:
            reader = csv.reader(file)
            for row in reader:
                id_to_char.append(row[1])
            char_to_id = {k: v for v, k in enumerate(id_to_char)}

    # Load checkpoint into model
    print('Loading model...')
    checkpoint_path = os.path.join(checkpoints_dir, author)
    new_model = load_model(len(char_to_id), checkpoint_path)

    # Generate text and return JSON in POST response
    print('Generating text...')
    prediction = generate_text(new_model, seed, char_to_id, id_to_char, num_to_generate=length)
    response = make_response(jsonify(author=author, length=length, seed=seed, response=prediction), 200)
    print('Generation complete.')
    return response


if __name__ == '__main__':
    app.run(debug=True)
