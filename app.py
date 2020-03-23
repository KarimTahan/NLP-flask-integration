from flask import Flask, render_template, request, make_response, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug=True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/param_input', methods=['POST'])
def get_params():
    params = {'seed': request.form['seed'], 'model': request.form['model']}
    # prediction = generate_text(params['model'], params['seed'])
    # prediction = generate_text(model, seed)
    print(params)
    return make_response(jsonify(params), 200)


if __name__ == '__main__':
    app.run(debug=True)
