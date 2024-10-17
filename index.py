from flask import Flask, request, make_response
from chroma_db import ChromaDbManager

db_client = ChromaDbManager()

app = Flask(__name__)


def create_response(message: str, status: int):
    response = make_response(message, status)
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        request_body = request.get_json()
        data = request_body.get('data')

        db_client.insert_data(data)

        return create_response("¡Los datos fueron cargados exitosamente!", 201)
    except Exception as e:
        return create_response(f"Error: {e}", 500)


@app.route('/similarity_calculation', methods=['POST'])
def search_data():
    try:

        request_body = request.get_json()
        document_name = request_body.get("document_name")
        document_section = request_body.get("document_section")
        full_message = request_body.get("full_message")

        best_results = db_client.search_documents(
            document_name, document_section, full_message)
        return create_response(best_results, 200)
    except Exception as e:
        return create_response(f"Error: {e}", 500)


if __name__ == '__main__':
    app.run(debug=True)
