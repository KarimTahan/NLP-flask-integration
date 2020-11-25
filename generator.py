import tensorflow as tf
from gensim.models import Word2Vec


def build_model(vocab_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, 256,
                                  batch_input_shape=[1, None]),
        tf.keras.layers.GRU(1024,
                            return_sequences=True,
                            stateful=True,
                            recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model


def load_model(vocab_size, author_ckpt_path):
    model = build_model(vocab_size)
    model.load_weights(tf.train.latest_checkpoint(author_ckpt_path))
    model.build(tf.TensorShape([1, None]))
    return model


def load_w2v(path):
    return Word2Vec.load(path)


def word2idx(word, word_model):
    return word_model.wv.vocab[word].index


def idx2word(idx, word_model):
    return word_model.wv.index2word[idx]

def sample(preds, temperature=1.0):
    if temperature <= 0:
        return np.argmax(preds)
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_text(model, start_string, num_to_generate, w2v_path):
    # Evaluation step (generating text using the learned model)
    w2v_model = load_w2v(w2v_path)
    # Number of characters to generate
    num_generate = num_to_generate
    
    #split start string into list
    seed = start_string.lower().split(" ")

    # Converting our start string to numbers (vectorizing)
    input_eval = [word2idx(s, w2v_model) for s in seed]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(x=np.array(input_array))
        
        idx = sample(prediction[-1], temperature=0.7)
        text_generated.append(idx)
    return ' '.join(idx2word(idx) for idx in text_generated)
