import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ExploreOWL import load_file_db
from Neo4JConnector.NeoConnector2 import NeoConnector2
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from logs import logger


from flask import Flask, jsonify, request, redirect, Blueprint
import json
from flask_cors import CORS, cross_origin

from flask import Flask, render_template

UPLOAD_FOLDER = 'upload_folder'
ALLOWED_EXTENSIONS = {'ttl'}
# bp = Blueprint('burritos', __name__,
#                         template_folder='templates')
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
connector2 = NeoConnector2()
CORS(app)


app.config['CORS_HEADERS'] = 'Content-Type'

# df = pd.read_csv('data/data2.csv')




@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200


@app.route('/')
def home():
    nodes, links, all_ids = connector2.get_general_graph()
    nodes_dict = [node.to_dict() for node in nodes]
    data = {
        'nodes': nodes_dict,
        'links': links
    }
    return render_template('index.html', data=data, all_ids=all_ids)


@app.route('/search', methods=['GET'])
def search():
    print(request)
    search_str = request.args.get('search')
    print(search_str)
    nodes, links, all_ids = connector2.get_search_graph(search_str)
    nodes_dict = [node.to_dict() for node in nodes]
    data = {
        'nodes': nodes_dict,
        'links': links
    }
    return render_template('index.html', data=data, all_ids=all_ids)


@app.route('/expand_node_2', methods=['POST'])
def expand_node_2():
    data = request.get_json()
    logger.info(f"expand node {data}")
    nodes, links, all_ids = connector2.expand_node(int(data['node_id']), data['current_results'])
    nodes_dict = [node.to_dict() for node in nodes]
    return json.dumps({
        'nodes': nodes_dict,
        'links': links
    }, indent=4)


@app.route('/upload', methods=['POST'])
def upload_file():
    print("Current working directory:", os.getcwd())
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(file_path)
        file.save(file_path)
        load_file_db(file_path)
        return redirect('/')

#app.register_blueprint(bp, url_prefix='/abc')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5005)  # , debug=True)
    app.run(port=5005)  # , debug=True)
