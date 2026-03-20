
import pathlib
import rdflib
from flask import Flask
from flask import render_template


# okay what does this even do - load up triples from examples
# you will need to add a bonus Example.ttl for everything stray
# then you filter on the triples to display or not
# and you display the data as jinja
# keep in mind the idea of json-ld!!


graph = rdflib.Graph()
ttl_path = pathlib.Path.cwd() / 'ttl'
for t in [x for x in ttl_path.iterdir()]:
    graph += rdflib.Graph().parse(t)



valid_uris = list()
for s,p,o in graph.triples((None, None, None)):
    if 'example.fiafcore.org' in str(s):
        valid_uris.append(s)
    if type(o) is type(rdflib.URIRef('')):
        if 'example.fiafcore.org' in str(o):
            valid_uris.append(o)



app = Flask(__name__)


@app.route('/<resource>', methods=['GET'])
def home(resource):

    if resource in [pathlib.Path(x).name for x in valid_uris]:
        # if resource not in valid uris, throw a 404
        # otherwise convert data to json-ld and feed to jinja
        namespace = 'https://example.fiafcore.org/'
        subject_uri = rdflib.URIRef(namespace+resource)

        subject_graph = rdflib.Graph()
        for s,p,o in graph.triples((subject_uri, None, None)):
            subject_graph.add((s,p,o))


        # hmm

        return render_template('hello.html', data=subject_graph.serialize(format='json-ld'))
    else:
        return render_template('error.html')
