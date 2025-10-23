import pathlib
import rdflib
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/<name>')
def entity(name):

    # mimic sparql call here, if no response send to 404, otherwise render payload on the page

    graph_path = pathlib.Path.cwd().parent / 'graph.ttl'
    if not graph_path.exists():
        raise Exception('Graph doc not found.')


    test_uri = 'https://ontology.fiafcore.org/Work'

    # query payload and return result, then make dynamic

    g = rdflib.Graph().parse(graph_path)

    triples = [(s,p,o) for s,p,o in g.triples((rdflib.URIRef(test_uri), None, None))]

    if not len(triples):
        return render_template('missing.html')

        # if triples returned are zero, return a 404 page,


    else:


        # otherwise detect a type

        entity_type = [x for x in triples if x[1] == rdflib.RDF.type][0][2] # returns "class"

        # IF ENTITY_TYPE IS CLASS< render class.html

        # and render the page, dependant on type - type should probably resolve to a template

        print(graph_path)
        # g = rdflib.Graph()



        return render_template('entity.html', data=(entity_type, triples))

if __name__ == "__main__":
    app.run(debug=True, port=5001)


