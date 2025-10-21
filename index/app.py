import pathlib
import requests
import rdflib
from flask import Flask
from flask import render_template

def pull_attribute(e, p):

    x = [c for a,b,c in g.triples((e, p, None))]
    if len(x) != 1:
        raise Exception('Single value expected.')
    
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
        rdflib.URIRef('https://ontology.fiafcore.org/Work'),
        rdflib.URIRef('https://ontology.fiafcore.org/Variant'),
        rdflib.URIRef('https://ontology.fiafcore.org/Manifestation'),
        rdflib.URIRef('https://ontology.fiafcore.org/Item'),
        rdflib.URIRef('https://ontology.fiafcore.org/Carrier'),
        rdflib.URIRef('https://ontology.fiafcore.org/Event'),
        rdflib.URIRef('https://ontology.fiafcore.org/Activity'),
        rdflib.URIRef('https://ontology.fiafcore.org/Agent'),        
    ]:

        label = pull_attribute(entity, rdflib.RDFS.label)
        string += f'<h4>{label}</h4>'

        desc = pull_attribute(entity, rdflib.URIRef('http://purl.org/dc/elements/1.1/description'))
        string += f'{desc}<br><br>'

        string += '<i>Properties</i><br><br>'
        string += '<table><tr><td>Property</td><td>Range</td><td>Description</td></tr>'
        props = [s for s,p,o in g.triples((None, rdflib.RDFS.domain, entity))]
        for p in sorted(props):
            prop = f'fiaf:{pathlib.Path(p).name}'
            rang = pull_attribute(p, rdflib.RDFS.range) # TODO, you need to replace xml schema prefix.
            if 'fiafcore' in rang:
                rang = f'fiaf:{pathlib.Path(rang).name}'
            else:
                rang = rang.replace('http://www.w3.org/2001/XMLSchema#', 'xsd:')                
            desc = str(pull_attribute(p, rdflib.URIRef('http://purl.org/dc/elements/1.1/description')))
            string += f'<tr><td>{prop}</td><td>{rang}</td><td>{desc}</td></tr>'
        string += '</table>'

        string += '<br>EXAMPLE HERE<br>'

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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
