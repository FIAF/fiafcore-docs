import json
import pathlib
import requests
import rdflib
from flask import Flask
from flask import render_template

def pull_attribute(e, p, gr):

    x = [c for a,b,c in gr.triples((e, p, None))]
    if len(x) != 1:
        print(c)
        raise Exception(f'Single value expected {x}.')

    return x[0]

app = Flask(__name__)

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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/ontology', methods=['GET'])
def ontology():

    string = ''
    for entity in [
        rdflib.URIRef('https://dev.fiafcore.org/Work'),
        rdflib.URIRef('https://dev.fiafcore.org/Variant'),
        rdflib.URIRef('https://dev.fiafcore.org/Manifestation'),
        rdflib.URIRef('https://dev.fiafcore.org/Item'),
        rdflib.URIRef('https://dev.fiafcore.org/Carrier'),
        rdflib.URIRef('https://dev.fiafcore.org/Event'),
        rdflib.URIRef('https://dev.fiafcore.org/Activity'),
        rdflib.URIRef('https://dev.fiafcore.org/Agent'),
    ]:

        label = pull_attribute(entity, rdflib.RDFS.label, g)
        string += f'<h4>{label}</h4>'

        desc = pull_attribute(entity, rdflib.URIRef('http://purl.org/dc/elements/1.1/description'), g)
        string += f'{desc}<br><br>'

        string += '<i>Properties</i><br><br>'
        string += "<table><tr style='background-color: grey;color: white'><td><b>Property</b></td><td><b>Range</b></td><td><b>Description</b></td></tr>"
        props = [s for s,p,o in g.triples((None, rdflib.RDFS.domain, entity))]
        for p in sorted(props):
            prop = f'fiaf:{pathlib.Path(p).name}'
            rang = pull_attribute(p, rdflib.RDFS.range, g) # TODO, you need to replace xml schema prefix.
            if 'fiafcore' in rang:
                rang = f'fiaf:{pathlib.Path(rang).name}'
            else:
                rang = rang.replace('http://www.w3.org/2001/XMLSchema#', 'xsd:')
            desc = str(pull_attribute(p, rdflib.URIRef('http://purl.org/dc/elements/1.1/description'), g))
            string += f'<tr><td>{prop}</td><td>{rang}</td><td>{desc}</td></tr>'
        string += '</table>'

        string += '<br><i>Example</i><br><br>'

        example_type = pathlib.Path(entity).name
        with open(pathlib.Path.cwd() / 'example' / 'ttl' / f'{example_type}.ttl') as example:
            example = example.read()
            example = example.replace('<', '&lt;')
            example = example.replace('>', '&gt;')

        string += f'<pre><code class="language-turtle">{example}</code></pre>'

    return render_template('ontology.html', data=string)

@app.route('/sources', methods=['GET'])
def sources():
    return render_template('sources.html')

@app.route('/access', methods=['GET'])
def access():
    return render_template('access.html')

@app.route('/licence', methods=['GET'])
def licence():
    return render_template('licence.html')

@app.route('/<resource>', methods=['GET'])
def page(resource):

    print(resource)

    resource_graph = rdflib.Graph().parse(pathlib.Path.cwd() / 'graph.ttl')
    resources = [pathlib.Path(s).name for s,p,o in resource_graph.triples((None, None, None))]
    ontology = [pathlib.Path(s).name for s,p,o in g.triples((None, None, None))]
    if resource in ontology:

        data='ontology'

        return render_template('entity.html', data=data)

    elif resource in resources:

        namespace = 'https://dev.fiafcore.org/'
        subject_uri = f'<{namespace}{resource}>'

        # load by type, so here we have a SPARQL query for work type
        # which means we need to pull type from resource, to begin with
        # and then load up the sparql to issue to the triplestore.

        # if superclass is work:

        with open(pathlib.Path.cwd() / 'shapes' / 'work.sparql') as shape:
            shape = shape.read()
            shape = shape.replace('SUBJECT_URI', subject_uri)

        result = resource_graph.query(shape)
        data = result.serialize(format="json-ld").decode()
        data = json.loads(data)

        return render_template('entity.html', resource=f'{namespace}{resource}', data=data)
    else:
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
