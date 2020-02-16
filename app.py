from flask import Flask
import functions

def create_app() -> Flask:
    app = Flask(__name__)
    return app

app = create_app()


api_map = [
    {
        'rule': '/',
        'view_func': functions.index,
        'methods': ['GET']
    },
    {
        'rule': '/company/<id>',
        'view_func': functions.get_company,
        'methods': ['GET']
    }
]

for entry in api_map:
    app.add_url_rule(entry['rule'], 
                    view_func=entry['view_func'],
                    methods=entry['methods'])


if __name__ == "__main__":
    app.run(debug=True)
