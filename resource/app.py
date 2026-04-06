import pandas
import pathlib
import rdflib
import requests
from flask import Flask
from flask import render_template


def entity_label(graph, entity):
    ''' Return an entity URI and label. '''

    label = [o for s,p,o in graph.triples((entity, rdflib.RDFS.label, None))]
    if not len(label):
        raise Exception('label not found.')

    return {'uri':str(entity), 'label':str(label[0])}

def entity_properties(entity):
    ''' Determine properties for primary entity types. '''

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

    # for entity in [
    #     rdflib.URIRef('https://ontology.fiafcore.org/Work'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Variant'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Manifestation'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Item'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Carrier'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Event'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Activity'),
    #     rdflib.URIRef('https://ontology.fiafcore.org/Agent'),        
    # ]:

    # label = pull_attribute(entity, rdflib.RDFS.label)
    # string += f'<h4>{label}</h4>'

    # desc = pull_attribute(entity, rdflib.URIRef('http://purl.org/dc/elements/1.1/description'))
    # string += f'{desc}<br><br>'

    # string += '<i>Properties</i><br><br>'
    # string += '<table><tr><td>Property</td><td>Range</td><td>Description</td></tr>'
    return [s for s,p,o in g.triples((None, rdflib.RDFS.domain, entity))]
    
    print(entity)
    print(props)
    print('\n')
    # for p in sorted(props):
    #     prop = f'fiaf:{pathlib.Path(p).name}'
    #     rang = pull_attribute(p, rdflib.RDFS.range) # TODO, you need to replace xml schema prefix.
    #     if 'fiafcore' in rang:
    #         rang = f'fiaf:{pathlib.Path(rang).name}'
    #     else:
    #         rang = rang.replace('http://www.w3.org/2001/XMLSchema#', 'xsd:')                
    #     desc = str(pull_attribute(p, rdflib.URIRef('http://purl.org/dc/elements/1.1/description')))
    #     string += f'<tr><td>{prop}</td><td>{rang}</td><td>{desc}</td></tr>'
    # string += '</table>'

    # string += '<br>EXAMPLE HERE<br>'

# entity_properties()

# TODO, draw out a manifestation using actual import data.

# NOTE graph for front end should always load from triplestore.

graph_path = pathlib.Path.cwd().parent / 'graph.ttl'
if not graph_path.exists():
    raise Exception('Graph doc not found.')

g = rdflib.Graph().parse(graph_path)
print(len(g), 'triples.')

app = Flask(__name__)

@app.route('/<name>')
def entity(name):

    # Manifestation

    test_uri = rdflib.URIRef('https://resource.fiafcore.org/2d057206-ee25-4331-8f32-4744a717b519')

    # Murnau

    # test_uri = rdflib.URIRef('https://resource.fiafcore.org/aafb9593-87b7-43ab-a2f8-8ff0365dcea7')


    # we need to determine class, including where we have a subtype of a class.
    # question is whether this is better as sparql, or we hardcode for now.
    # relevant is how many levels down of class we need to check.

    # for rendering data, we have to assume 0..n, 
    # so what is behaviour for zero? also every response has to be an array for jinja.
    # 
    # Worth thinking about is whether it is possible to dynamically generate templates from the ontology
    # with a caveat that we need to be able to distinguisg between helpful "extension" (lamguage and colour)
    # and unhelpful, eg manifestations showing item info.

    # actually before this we need a label!
    test = {'entity':entity_label(g, test_uri)}

    # first step of this is, what type is test_uri
    # actually these are two question, one is what type it **immediatly** is, for display, second is what the top level.
    # do that first, because then you can just splice the rdf:type on the front.

    r = g.query("""
        select distinct ?class
        where { 
            <"""+str(test_uri)+"""> rdf:type ?c .
            ?c rdfs:subClassOf* ?class .
            filter not exists { ?class rdfs:subClassOf ?b } .
        }""")

    df = pandas.DataFrame(r, columns=['class'])
    entity_type = df.iloc[0]['class']

    print('@@@', entity_type) 
    
    # okay, this has come back as AGENT, what does that mean??
    # now we need to detect all the properties which come off this.
    # if objects are blank nodes, then also pull those 

    entity_prop = sorted(entity_properties(entity_type))
    entity_prop = [rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')]+entity_prop
    # print('@@@', entity_prop)



    # okay now cycle through each prop and return triple statements
    # if o is a blank node, things get interesting!




    for prop in entity_prop:
        print('@@@', prop)


    # sort it and add rdftype on the front!

    # so need to generate a list of all expected properties, per major entity type.


    # so what is name here? it is actually a resource reference we need to hardcode for now.

    # data = 'paul'

    return render_template('manifestation.html', data=test)


if __name__ == "__main__":
    app.run(debug=True, port=5002)


