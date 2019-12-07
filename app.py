from flask import Flask, jsonify
import functions
import threading

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/')
def index():
    links = {
        "links" : {
            "self" : "/",
            "company" : "/company/<id>" 
        }
    }
    return jsonify(links)

@app.route('/company/<id>', methods=['GET']) 
def get_company_data(id):
    functions.get_data(id)
    filename = functions.generate_filename(id)
    data, code = functions.open_file_and_return_data(filename)
    return jsonify(data), code

if __name__ == "__main__":
    app.run(debug=True)

