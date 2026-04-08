import json
import os
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


# pull example rdf, from web resource. Do this on flask deploy.

example_graph = rdflib.Graph()
example_graph.add((rdflib.DC.description, rdflib.RDFS.label, rdflib.Literal("Description")))
example_graph.add((rdflib.DC.source, rdflib.RDFS.label, rdflib.Literal("Source")))
example_graph.add((rdflib.RDFS.subClassOf, rdflib.RDFS.label, rdflib.Literal("Subclass Of")))
example_graph.add((rdflib.RDFS.domain, rdflib.RDFS.label, rdflib.Literal("Domain")))
example_graph.add((rdflib.RDFS.range, rdflib.RDFS.label, rdflib.Literal("Range")))
example_graph.add((rdflib.RDFS.label, rdflib.RDFS.label, rdflib.Literal("Label")))

# mint deterministic bnode uris.

bnodes = dict()
for i in range(1,3):
    bnodes[f'blankNode{i}'] = rdflib.BNode()

# build example graph from turtle fragments.

for example_type in [
    'Work',
    'Variant',
    'Manifestation',
    'Item',
    'Carrier',
    'Event',
    'Activity',
    'Agent']:

    example_path = f'https://raw.githubusercontent.com/FIAF/fiafcore/refs/heads/develop/example/{example_type}.ttl'
    r = requests.get(example_path)
    if r.status_code != 200:
        raise Exception(f'API {r.status_code}: {r.text}')

    # convert bnodes to literals.

    rdf = r.text
    for b in bnodes.keys():
        rdf = rdf.replace(f'_:{b}', f'"{b}"')

    example_graph += rdflib.Graph().parse(data=rdf)

# extra entity labelling.

example_graph.add((rdflib.URIRef('https://example.fiafcore.org/f0032f62-d28c-4730-a358-afb8106173e0'), rdflib.RDFS.label, rdflib.Literal('Test Archive')))

# replace bnode literals with deterministic bnodes.

for k,v in bnodes.items():
    for s,p,o in example_graph.triples((None, None, None)):
        if s == rdflib.Literal(k):
            example_graph.add((v, p, o))
            example_graph.remove((s,p,o))
        if o == rdflib.Literal(k):
            example_graph.add((s, p, v))
            example_graph.remove((s,p,o))


# NOTE: all of these additional example labels should be present at source.

r = requests.get('https://raw.githubusercontent.com/FIAF/fiafcore/refs/heads/develop/fiafcore.ttl')
if r.status_code != 200:
    raise Exception('API call failed.')

g = rdflib.Graph().parse(data=r.text) # turn this off in lieu of ontology_graph, once you have re routed.

ontology_graph = rdflib.Graph().parse(data=r.text)

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


def superclass(graph):

    """Predetermine superclasses for core child elements."""

    query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix fiaf: <https://dev.fiafcore.org/>
        select ?parent ?child
        where {
            values ?parent { fiaf:Work fiaf:Variant fiaf:Manifestation fiaf:Item fiaf:Carrier fiaf:Agent }
            ?child rdfs:subClassOf+ ?parent
        }
    """

    return dict([(row.child, row.parent) for row in graph.query(query)])

superclass_lookup = superclass(ontology_graph)
print('**', superclass_lookup)

def subclasses(parent):

    # fiafcore_path = pathlib.Path.cwd() / 'fiafcore.ttl'
    # if not fiafcore_path.exists():
    #     raise Exception('Local ontology file not found.')

    # fiafcore = rdflib.Graph().parse(fiafcore_path)
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?subClass
        WHERE {
            ?subClass rdfs:subClassOf+ <"""+parent+"""> .
        }
    """
    result = [row.subClass for row in g.query(query)]
    result.append(rdflib.URIRef(parent))

    return result

agent_classes = subclasses('https://dev.fiafcore.org/Agent')
work_classes = subclasses('https://dev.fiafcore.org/Work')
manifestation_classes = subclasses('https://dev.fiafcore.org/Manifestation')
item_classes = subclasses('https://dev.fiafcore.org/Item')
carrier_classes = subclasses('https://dev.fiafcore.org/Carrier')

@app.route('/', methods=['GET'])
def home():
    if os.getenv('INSTANCE') != 'dev':
        return render_template('error.html')

    return render_template('index.html')

@app.route('/ontology', methods=['GET'])
def ontology():
    if os.getenv('INSTANCE') != 'dev':
        return render_template('error.html')

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
        example_path = f'https://raw.githubusercontent.com/FIAF/fiafcore/refs/heads/develop/example/{example_type}.ttl'
        r = requests.get(example_path)
        if r.status_code != 200:
            raise Exception(f'API {r.status_code}: {r.text}')

        example = r.text
        example = example.replace('<', '&lt;')
        example = example.replace('>', '&gt;')
        string += f'<pre><code class="language-turtle">{example}</code></pre>'

    return render_template('ontology.html', data=string)

@app.route('/sources', methods=['GET'])
def sources():
    if os.getenv('INSTANCE') != 'dev':
        return render_template('error.html')

    return render_template('sources.html')

@app.route('/access', methods=['GET'])
def access():
    if os.getenv('INSTANCE') != 'dev':
        return render_template('error.html')

    return render_template('access.html')

@app.route('/licence', methods=['GET'])
def licence():
    if os.getenv('INSTANCE') != 'dev':
        return render_template('error.html')

    return render_template('licence.html')

@app.route('/<resource>', methods=['GET'])
def page(resource):

    if os.getenv('INSTANCE') == 'example':

        # determine uuid validaty by attempting to determine the rdf.type.

        uri = rdflib.URIRef(f'https://example.fiafcore.org/{resource}')
        print(uri)
        uri_match = [o for s,p,o in example_graph.triples((uri, rdflib.RDF.type, None))]
        print(uri_match)
        if not len(uri_match):
           return render_template('error.html')

        # pull type and generalise.

        uri_type = uri_match[0]
        print(uri_type)
        print(superclass_lookup.keys())

        if uri_type not in superclass_lookup.keys():
            return render_template('error.html')

        uri_superclass = superclass_lookup[uri_type]

        # route to appropriate shape and insert subject uri.

        shape = pathlib.Path(uri_superclass).stem.lower()
        shape_path = pathlib.Path.cwd() / 'shapes' / f'{shape}.sparql'
        if not shape_path.exists():
            raise Exception('Shape file not found.')

        with open(shape_path) as construct:
            construct = construct.read()
            construct = construct.replace('SUBJECT_URI', f'<{uri}>')

        # apply shape query to example graph and return json-ld.

        result = (example_graph+ontology_graph).query(construct)
        data = result.serialize(format="json-ld").decode()
        data = json.loads(data)

        # TODO: you should be able to route this to the proper template now.

        # return render_template('test.html', data=result.serialize(format='ttl').decode())
        #

        return render_template('entity.html', resource=str(uri), data=data)




    print(resource)

    # these should move to top level so they are not processing for each page.
    # although - longterm they will be sparql queries not local graph queries.

    resource_graph = rdflib.Graph().parse(pathlib.Path.cwd() / 'graph.ttl')
    resources = [pathlib.Path(s).name for s,p,o in resource_graph.triples((None, None, None))]
    ontology = [pathlib.Path(s).name for s,p,o in g.triples((None, None, None))]
    if resource in ontology:

        namespace = 'https://dev.fiafcore.org/'
        subject_uri = f'{namespace}{resource}'

        subject_types = [o for s,p,o in resource_graph.triples((rdflib.URIRef(subject_uri), rdflib.RDF.type, None))]
        if not len(subject_types):
            raise Exception('Type could not be detected.')
        subject_type = subject_types[0]

        if rdflib.URIRef(subject_type) == rdflib.OWL.Class:
            shape = 'class'
        elif rdflib.URIRef(subject_type) == rdflib.OWL.DatatypeProperty:
            shape = 'property'
        elif rdflib.URIRef(subject_type) == rdflib.OWL.ObjectProperty:
            shape = 'property'
        else:
            raise Exception('Shape not determined.')

        shape_path = pathlib.Path.cwd() / 'shapes' / f'{shape}.sparql'
        if not shape_path.exists():
            raise Exception('Shape file not found.')

        with open(shape_path) as construct:
            construct = construct.read()
            construct = construct.replace('SUBJECT_URI', f'<{subject_uri}>')

        resource_graph.add((rdflib.DC.description, rdflib.RDFS.label, rdflib.Literal("Description")))
        resource_graph.add((rdflib.DC.source, rdflib.RDFS.label, rdflib.Literal("Source")))
        resource_graph.add((rdflib.RDFS.subClassOf, rdflib.RDFS.label, rdflib.Literal("Subclass Of")))
        resource_graph.add((rdflib.RDFS.domain, rdflib.RDFS.label, rdflib.Literal("Domain")))
        resource_graph.add((rdflib.RDFS.range, rdflib.RDFS.label, rdflib.Literal("Range")))
        resource_graph.add((rdflib.RDFS.label, rdflib.RDFS.label, rdflib.Literal("Label")))

        result = resource_graph.query(construct)
        data = result.serialize(format="json-ld").decode()
        data = json.loads(data)

        return render_template('entity.html', resource=f'{namespace}{resource}', data=data)

    elif resource in resources:

        namespace = 'https://dev.fiafcore.org/'
        subject_uri = f'{namespace}{resource}'

        subject_types = [o for s,p,o in resource_graph.triples((rdflib.URIRef(subject_uri), rdflib.RDF.type, None))]
        if not len(subject_types):
            raise Exception('Type could not be detected.')
        subject_type = subject_types[0]

        if subject_type in work_classes:
            shape = 'work'
        elif subject_type in manifestation_classes:
            shape = 'manifestation'
        elif subject_type in item_classes:
            shape = 'item'
        elif subject_type in carrier_classes:
            shape = 'carrier'
        elif subject_type in agent_classes:
            shape = 'agent'
        else:
            raise Exception('Shape not determined.')

        shape_path = pathlib.Path.cwd() / 'shapes' / f'{shape}.sparql'
        if not shape_path.exists():
            raise Exception('Shape file not found.')

        with open(shape_path) as construct:
            construct = construct.read()
            construct = construct.replace('SUBJECT_URI', f'<{subject_uri}>')

        resource_graph.add((rdflib.DC.description, rdflib.RDFS.label, rdflib.Literal("Description")))
        resource_graph.add((rdflib.DC.source, rdflib.RDFS.label, rdflib.Literal("Source")))
        resource_graph.add((rdflib.RDFS.subClassOf, rdflib.RDFS.label, rdflib.Literal("Subclass Of")))
        resource_graph.add((rdflib.RDFS.domain, rdflib.RDFS.label, rdflib.Literal("Domain")))
        resource_graph.add((rdflib.RDFS.range, rdflib.RDFS.label, rdflib.Literal("Range")))
        resource_graph.add((rdflib.RDFS.label, rdflib.RDFS.label, rdflib.Literal("Label")))

        result = resource_graph.query(construct)
        data = result.serialize(format="json-ld").decode()
        data = json.loads(data)

        return render_template('entity.html', resource=f'{namespace}{resource}', data=data)
    else:
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True, port=5030)
