from src import create_app
from waitress import serve

application = create_app()

if __name__ == "__main__":
    # app.run( host="0.0.0.0", debug=True, port=8000)
    serve(application, host="0.0.0.0", port=8000)