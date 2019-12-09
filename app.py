from flask import Flask, jsonify, request
import functions

def create_app() -> Flask:
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/')
def index():
    links = list()
    links.append({"rel": "self", "href": request.path})
    links.append({"rel": "company", "href": "/company/<id>"})
    status = 200
    data = dict()
    response = functions.make_response(data, status, links)
    return jsonify(response)

@app.route('/company/<id>', methods=['GET']) 
def get_company_data(id):
    links = list()
    links.append({"rel": "self", "href": request.path})
    functions.get_data(id)
    filename = functions.generate_filename(id)
    (data, status) = functions.open_file_and_return_data(filename)
    response = functions.make_response(data, status, links)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

