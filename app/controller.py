# glues model and view together
from flask import Flask, send_file, render_template, request, jsonify
import model
import json
from flask import Response
app = Flask(__name__)

@app.route('/',methods=['GET','POST'] )
def index():
    if request.method == 'POST':
        print('Caught post request...')
        post_data = request.get_json()
        #UPDATE DATABASE -> update model? or on schedule?

        print(post_data)
    return send_file("templates/index_exporter.html" )

@app.route('/experiment/', methods=['GET'])
def search_query():

    experiment = model.load_experiment('exportexperiment.pkl')
    return jsonify({'all_experiments':experiment})

if __name__ == '__main__':
    app.run(debug=True)