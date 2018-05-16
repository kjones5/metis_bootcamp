import flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

#---------- MODEL IN MEMORY ----------------#

# Read NHSTA data on fatal traffic accident survival by passenger,
# Build a LogisticRegression predictor on it
df = pd.read_csv('flask_subset.csv')

X = df.drop('FATALITY_TARGET', axis=1)
Y = df['FATALITY_TARGET']
PREDICTOR = LogisticRegression().fit(X,Y)


#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, fatality_pred.html
    """
    with open("fatality_pred.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return its score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.matrix(data["example"])
    score = PREDICTOR.predict_proba(x)
    # Put the result in a nice dict so we can send it as json
    results = {"score": score[0,1]}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0')
app.run(debug=True)
