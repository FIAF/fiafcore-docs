import pathlib
import rdflib
import requests
from flask import Flask
from flask import render_template


r = requests.get('https://raw.githubusercontent.com/FIAF/fiafcore/refs/heads/develop/fiafcore.ttl')
if r.status_code != 200:
    raise Exception('API call failed.')

g = rdflib.Graph().parse(data=r.text)

# parsing entity to remove all unionOf nodes.

query = ''' 
    select ?subject ?union_domain where {
        ?subject rdfs:domain ?domain .
        ?domain owl:unionOf ?a .
        ?a rdf:rest*/rdf:first ?union_domain .
    } '''

# add direct domain statements

for a, b in g.query(query):
    g.add((a, rdflib.RDFS.domain, b))

# remove blank node statements

for a,b,c in g.triples((None, None, None)):
    if type(a) is type(rdflib.BNode('')) or type(b) is type(rdflib.BNode('')):
        g.remove(( a, b, c))

g.add((rdflib.URIRef('http://www.w3.org/2002/07/owl#Class'), rdflib.RDFS.label, rdflib.Literal("Class")))





app = Flask(__name__)







def entity_label(graph, entity):
    ''' Return an entity URI and label. '''

    label = [o for s,p,o in graph.triples((entity, rdflib.RDFS.label, None))]
    if not len(label):
        raise Exception('label not found.')

    return {'uri':entity, 'label':label[0]}




@app.route('/<name>')
def entity(name):






    # mimic sparql call here, if no response send to 404, otherwise render payload on the page.

    # graph_path = pathlib.Path.cwd().parent / 'graph.ttl'
    # if not graph_path.exists():
    #     raise Exception('Graph doc not found.')

    test_uri = f'https://ontology.fiafcore.org/{name}'

    # query payload and return result, then make dynamic

    # g = rdflib.Graph().parse(graph_path)
    triples = [(s,p,o) for s,p,o in g.triples((rdflib.URIRef(test_uri), None, None))]
    if not len(triples):
        return render_template('missing.html')
    else:

        # detect a type

        entity_type = [x for x in triples if x[1] == rdflib.RDF.type][0][2]

        description = [x for x in triples if x[1] == rdflib.URIRef('http://purl.org/dc/elements/1.1/description')][0][2]

        source = [x for x in triples if x[1] == rdflib.URIRef('http://purl.org/dc/elements/1.1/source')][0][2]


        # subclasses = [x for x in triples if x[1] == rdflib.RDFS.subClassOf]
        subclasses = [entity_label(g, s) for s,p,o in g.triples((None, rdflib.RDFS.subClassOf, rdflib.URIRef(test_uri)))]





        properties = [entity_label(g, s) for s,p,o in g.triples((None, rdflib.RDFS.domain, rdflib.URIRef(test_uri)))]


        # okay now replicate ontology code!



        if entity_type == rdflib.URIRef('http://www.w3.org/2002/07/owl#Class'):
            print('CLASS')

            data = {
                'entity': entity_label(g, rdflib.URIRef(test_uri)),
                'type': entity_label(g, entity_type),
                'description': description,
                'source': source,
                'subclasses': subclasses,
                'properties': properties




                
                }

#     dc:description
#         "A moving image Work comprises both the intellectual or artistic content and the process of realisation in a cinematographic medium."@en ;
#     dc:source 
#         <https://www.fiafnet.org/images/tinyUpload/E-Resources/Commission-And-PIP-Resources/CDC-resources/20160920_Fiaf_Manual-WEB.pdf#20160915%20Fiaf%20Manual-WEB.indd%3A.35986%3A5030> ;
# .



#     rdfs:subClassOf 
#         <https://ontology.fiafcore.org/Work> ;
# .



#     rdfs:domain 
#         <https://ontology.fiafcore.org/Work> ;
#     rdfs:range 
#         <https://vocabulary.fiafcore.org/Country> ;
# .

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


