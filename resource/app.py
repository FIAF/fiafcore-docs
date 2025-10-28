import pathlib
# import rdflib
# import requests
from flask import Flask
from flask import render_template

# TODO, draw out a manifestation using actual import data.


graph_path = pathlib.Path.cwd().parent / 'graph.ttl'
if not graph_path.exists():
    raise Exception('Graph doc not found.')





app = Flask(__name__)



@app.route('/<name>')
def entity(name):

    # so what is name here? it is actually a resource reference we need to hardcode for now.

    data = 'paul'

    return render_template('manifestation.html', data=data)


if __name__ == "__main__":
    app.run(debug=True, port=5002)


