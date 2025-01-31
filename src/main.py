from flask import Flask
from routers.timeline_router import timeline_bp
from config.connectDb import Database
from config.connectRedis import Redis
from config.connectGemini import GeminiConnection
import os

# instantiating the flask application
app = Flask(__name__)

# Initialize connections
db = Database(os.getenv("DATABASE_URL"))
redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT"))
)
gemini = GeminiConnection(os.getenv("GEMINI_API_KEY"))

# Register blueprints
app.register_blueprint(timeline_bp, url_prefix='/api/v1/timeline')

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)