
from flask import Flask, render_template
app = Flask(__name__)


test=  {
        "nodes": [
            {
                "handle": "work",
                "label": "Work/Variant",
                "url": "WorkVariant",
                "x": 100,
                "y": 50
            },
            {
                "handle": "manifestation",
                "label": "Manifestation",
                "url": "Manifestation",
                "x": 100,
                "y": 120
            },
            {
                "handle": "item",
                "label": "Item",
                "url": "Item",
                "x": 100,
                "y": 190
            },
            {
                "handle": "carrier",
                "label": "Carrier",
                "url": "Carrier",
                "x": 100,
                "y": 260
            },
            {
                "handle": "event",
                "label": "Event",
                "url": "Event",
                "x": 250,
                "y": 155
            },
            {
                "handle": "activity",
                "label": "Activity",
                "url": "Activity",
                "x": 350,
                "y": 155
            },
            {
                "handle": "agent",
                "label": "Agent",
                "url": "Agent",
                "x": 450,
                "y": 155
            }
        ],
        "links": [
            {
                "source": "work",
                "target": "manifestation",
                "label": "Has Manfestation"
            },
            {
                "source": "manifestation",
                "target": "item",
                "label": "Has Item"
            },
            {
                "source": "item",
                "target": "carrier",
                "label": "Has Carrier"
            },
            {
                "source": "work",
                "target": "event",
                "label": "Has Event"
            },
            {
                "source": "manifestation",
                "target": "event",
                "label": "Has Event"
            },
            {
                "source": "item",
                "target": "event",
                "label": "Has Event"
            },
            {
                "source": "carrier",
                "target": "event",
                "label": "Has Event"
            },
            {
                "source": "event",
                "target": "activity",
                "label": "Has Activity"
            },
            {
                "source": "activity",
                "target": "agent",
                "label": "Has Agent"
            }
        ]
    }

@app.route('/', methods=['GET', 'POST'])
# @app.route('/ontology/', methods=['GET', 'POST'])
def home_page():

    return render_template('index.html',
    
    
    
    
    
      graph=test
      

    
    )



if __name__ == "__main__":
    app.run(debug=True, port=5000)