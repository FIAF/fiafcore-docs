from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/ontology', methods=['GET'])
def ontology():
    return render_template('ontology.html')

@app.route('/sources', methods=['GET'])
def sources():
    return render_template('sources.html')

@app.route('/access', methods=['GET'])
def access():
    return render_template('access.html')

@app.route('/licence', methods=['GET'])
def licence():
    return render_template('licence.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
