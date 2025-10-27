
# generate test graph.ttl file for doc building.

import pathlib
import rdflib

def append_ttl(path):
    
    ttl_path = pathlib.Path.cwd().parent / f'{path}.ttl'
    if not ttl_path.exists():
        raise Exception('Path not found.')
    
    return rdflib.Graph().parse(ttl_path)

graph = rdflib.Graph()
for p in [
    'fiafcore/fiafcore',
    'fiafcore-bfi/fiafcore_bfi',
    'fiafcore-bundesarchiv/fiafcore_bundesarchiv'
    ]:
    graph += append_ttl(p)


# for now we require some manual labelling.

# graph += 

graph.add((rdflib.URIRef('http://www.w3.org/2002/07/owl#Class'), rdflib.RDFS.label, rdflib.Literal("Class")))


graph.serialize(
    destination=pathlib.Path.cwd() / "graph.ttl",
    format="turtle",
    )

print(len(graph), 'triples.')
