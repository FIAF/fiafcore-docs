import pathlib
import rdflib
from flask import Flask
from flask import render_template



def entity_label(graph, entity):
    ''' Return an entity URI and label. '''

    label = [o for s,p,o in graph.triples((entity, rdflib.RDFS.label, None))]
    if not len(label):
        raise Exception('label not found.')

    return {'uri':entity, 'label':label[0]}


app = Flask(__name__)

@app.route('/<name>')
def entity(name):

    # mimic sparql call here, if no response send to 404, otherwise render payload on the page.

    graph_path = pathlib.Path.cwd().parent / 'graph.ttl'
    if not graph_path.exists():
        raise Exception('Graph doc not found.')

    test_uri = 'https://ontology.fiafcore.org/Work'

    # query payload and return result, then make dynamic

    g = rdflib.Graph().parse(graph_path)
    triples = [(s,p,o) for s,p,o in g.triples((rdflib.URIRef(test_uri), None, None))]
    if not len(triples):
        return render_template('missing.html')
    else:

        # detect a type

        entity_type = [x for x in triples if x[1] == rdflib.RDF.type][0][2]
        if entity_type == rdflib.URIRef('http://www.w3.org/2002/07/owl#Class'):
            print('CLASS')

            data = {
                'entity': entity_label(g, rdflib.URIRef(test_uri)),
                'type': entity_label(g, entity_type)

                
                }





            # for x in triples:
            #     print(x)
            return render_template('class.html', data=data)

        # IF ENTITY_TYPE IS CLASS< render class.html

        # http://www.w3.org/2002/07/owl#Class

        # do we want to run jinja, or python
        # lets try jinja and see how far we get.

        # data = {
        #     'label':'hello'
        # }


        # http://www.w3.org/2002/07/owl#Class


        print(entity_type)

        print(type(entity_type))




        # and render the page, dependant on type - type should probably resolve to a template

        print(graph_path)
        # g = rdflib.Graph()



        return render_template('entity.html', data=(entity_type, triples))

if __name__ == "__main__":
    app.run(debug=True, port=5001)


