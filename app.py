"""Super Hero API - Flask App

This script will deploy the Flask website
to visualize the super hero data hydrated with
the data_pull script. Flask application pulls
data from Postgres DB and not only provides
a REST framework to pull data, but also renders
the html web pages. Data visualized with Plotly.
"""

from db_model import SuperHeros, PowerStats, Biography, Aliases, Appearance, Work, Connections, Image
from db_model import session
import flask
import os

# Envionrment Variables
APP_DEBUG=bool(os.getenv('APP_DEBUG', True))

# Flask app
app = flask.Flask(__name__)
app.config['DEBUG'] = APP_DEBUG

@app.route('/', methods=['GET'])
def home():
    return flask.render_template('layouts/home.html')

@app.route('/api/v1/resources/heros/all', methods=['GET'])
def api_hero_all():
    rs = session.query(SuperHeros)
    heros = []
    
    for r in rs:
        heros.append({'id': r.id, 'name': r.name})
    
    return flask.jsonify(heros)

@app.route('/api/v1/resources/heros/powerstats', methods=['GET'])
def api_hero():
    if 'id' in flask.request.args:
        rs = session.query(PowerStats).filter_by(id=int(flask.request.args['id'])).first()
        
        if not rs is None:
            return flask.jsonify({
                'intelligence': rs.intelligence,
                'strength': rs.strength,
                'speed': rs.speed,
                'durability': rs.durability,
                'power': rs.power,
                'combat': rs.combat
            })
        else:
            return 'Hero ID %d Does Not Exist' % flask.request.args['id']

    return 'No Hero ID Parameter Found'

@app.route('/api/v1/resources/heros/image', methods=['GET'])
def api_image():
    if 'id' in flask.request.args:
        rs = session.query(Image).filter_by(id=flask.request.args['id']).first()
        
        if not rs is None:
            return flask.jsonify({'url': rs.url})
        else:
            return 'Hero ID %d Does Not Exist' % flask.request.args['id']

    return 'No Hero ID Parameter Found'

@app.route('/api/v1/resources/heros/occupation', methods=['GET'])
def api_occupation():
    if 'id' in flask.request.args:
        rs = session.query(Work).filter_by(id=flask.request.args['id']).first()
        
        if not rs is None:
            return flask.jsonify({'occupation': rs.occupation})
        else:
            return 'Hero ID %d Does Not Exist' % flask.request.args['id']

    return 'No Hero ID Parameter Found'

if __name__ == '__main__':
    app.run()
