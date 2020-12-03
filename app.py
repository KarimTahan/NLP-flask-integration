import csv
import os
import keras
from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
from generator import generate_text, load_model


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

    # Allow for both form and json formatted POST requests
    print('Received request...')
    if request.is_json is True:
        params = request.get_json(force=True)
    else:
        params = {'seed': request.form['seed'],
                  'author': request.form['author'],
                  'length': request.form['length']}

    author = params['author']
    seed = params['seed']

    if params['length'] is not '':
        length = int(params['length'])
    else:
        length = 0

    # Retrieve list of available checkpoints
    checkpoints_dir = 'checkpoints'
    checkpoints = [os.path.join(checkpoints_dir, o) for o in os.listdir(checkpoints_dir)
                   if os.path.isdir(os.path.join(checkpoints_dir, o))]
    tensor_model_dir = 'models'
    models = [os.path.join(tensor_model_dir, o) for o in os.listdir(tensor_model_dir)
                   if os.path.isdir(os.path.join(tensor_model_dir, o))]

    print('Building Model...')
    for c in models:
        if author in c:
            tensor_model = c
          
    # Retrieve desired checkpoint
    print('Retrieving checkpoint...')
    for c in checkpoints:
        if author in c:
            checkpoint = c

    # Retrieve character mapping of desired author and create reverse mapping
    print('Retrieving mapping...')
    if author in checkpoint:
        mapping_path = os.path.join('char_mappings', author + '_w2v.bin')
    

    # Load checkpoint into model
    print('Loading model...')
    model_path = os.path.join(tensor_model_dir, author)
    model_path = model_path + "/" + author + ".json"
    model = keras.models.model_from_json(model_path)
    checkpoint_path = os.path.join(checkpoints_dir, author)
    new_model = load_model(model, checkpoint_path)

    # Generate text and return JSON in POST response
    print('Generating text...')
    prediction = generate_text(new_model, seed, mapping_path, num_to_generate=length)
    response = make_response(jsonify(author=author, length=length, seed=seed, response=prediction), 200)
    print('Generation complete.')
    return response

# Deprecated for new model
# def sanitize_seed(author, pre_seed):
#     seed = ''
#     seed_list = pre_seed.splitlines()
#     for line in seed_list:
#         seed += line

#     seed = seed.lower()

#     return seed


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
