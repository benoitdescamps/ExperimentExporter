# glues model and view together
from flask import Flask, send_file, render_template, request, jsonify
import model
app = Flask(__name__)

@app.route('/',methods=['GET','POST'] )
def index():
    if request.method == 'POST':
        print('Caught post request...')
        post_data = request.get_json()
        #UPDATE DATABASE -> update model? or on schedule?

        print(post_data)
    return send_file("templates/index_v3.html" )

@app.route('/s/', methods=['GET'])
def search_query():
    """
    View which is called whenever the '/s/' this url is requested
    """

    path_db = 'app_data/current_databases/'
    #database_file = 'email_ICTU_database3.db'
    #data = model.load_database(path_db,database_file)
    print(model.python_data)
    return jsonify(model.python_data)#jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)