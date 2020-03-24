from flask import Flask, render_template, request, make_response, jsonify
import csv
import tensorflow as tf
import numpy as np
from author_model import build_model, generate_text

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug=True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/param_input', methods=['POST'])
def get_params():
    params = {'seed': request.form['seed'], 'model': request.form['model']}
    seed = params['seed']
    text = open('training/saved_weights.hdf5', 'rb').read()
    vocab = sorted(set(text))

    char_to_id = {value: key for key, value in enumerate(vocab)}
    id_to_char = np.array(vocab)

    # Manipulate the model
    new_model = build_model(vocab_size=len(char_to_id), embedding_dim=256, rnn_units=1024, batch_size=1)
    new_model.load_weights(tf.train.latest_checkpoint('training', 'saved_weights.hdf5'))
    new_model.build(tf.TensorShape([1, None]))
    new_model.summary()

    prediction = generate_text(new_model, seed, char_to_id, id_to_char)
    return make_response(jsonify(prediction), 200)


if __name__ == '__main__':
    app.run(debug=True)
