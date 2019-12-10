from flask import Flask, jsonify, request
import functions, classes

def create_app() -> Flask:
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/')
def index():
    links = [
        classes.link('self', request.path).value,
        classes.link('company', "/company/<id>").value
    ]
    response = classes.json_response(200, links, dict()).value
    return (jsonify(response), 200)

@app.route('/company/<id>', methods=['GET']) 
def get_company_data(id):
    links = [
        classes.link('self', request.path).value
    ]
    functions.get_company_data(id)
    filename = functions.generate_filename(id)
    (data, status) = functions.open_file_and_return_data(filename)
    response = classes.json_response(data, status, links).value
    return (jsonify(response), 200)

if __name__ == "__main__":
    app.run(debug=True)
