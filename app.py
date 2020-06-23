"""Super Hero API - Flask App

This script will deploy the Flask website
to visualize the super hero data hydrated with
the data_pull script. Flask application pulls
data from Postgres DB and not only provides
a REST framework to pull data, but also renders
the html web pages. Data visualized with Plotly.

Args:
    APP_DEBUG: Flask debug mode

"""

from db_model import SuperHeros, PowerStats, Work, Image
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
    """Flask Application Home Page

    Returns:
        Home page HTML content
    """
    return flask.render_template('layouts/home.html')

@app.route('/api/v1/resources/heros/all', methods=['GET'])
def api_hero_all():
    """Flask Application All Heros API

    Returns:
        All super heros in JSON response
    """
    rs = session.query(SuperHeros)
    heros = []
    
    for r in rs:
        heros.append({'id': r.id, 'name': r.name})
    
    return flask.jsonify(heros)

@app.route('/api/v1/resources/heros/powerstats', methods=['GET'])
def api_hero():
    """Flask Application Powerstats API

    Returns:
        Super hero powers ratings JSON response
    """
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
        rs = session.query(PowerStats).filter_by(id=id).first()
        
        if not rs is None:
            return flask.jsonify({
                'intelligence': rs.intelligence,
                'strength': rs.strength,
                'speed': rs.speed,
                'durability': rs.durability,
                'power': rs.power,
                'combat': rs.combat,
            })
        else:
            return 'Hero ID %d Does Not Exist' % id

    return 'No Hero ID Parameter Found'

@app.route('/api/v1/resources/heros/image', methods=['GET'])
def api_image():
    """Flask Application Image API

    Returns:
        Super hero image JSON response
    """
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
        rs = session.query(Image).filter_by(id=id).first()
        
        if not rs is None:
            return flask.jsonify({'url': rs.url})
        else:
            return 'Hero ID %d Does Not Exist' % id

    return 'No Hero ID Parameter Found'

@app.route('/api/v1/resources/heros/occupation', methods=['GET'])
def api_occupation():
    """Flask Application Occupation API

    Returns:
        Super hero occupation JSON reponse
    """
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
        rs = session.query(Work).filter_by(id=id).first()
        
        if not rs is None:
            return flask.jsonify({'occupation': rs.occupation})
        else:
            return 'Hero ID %d Does Not Exist' % id

    return 'No Hero ID Parameter Found'

if __name__ == '__main__':
    app.run()
