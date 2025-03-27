from flask import Flask, request, jsonify, render_template
import joblib
from score import score
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
model = joblib.load(open("svc.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/score', methods=['POST'])
def predict():
        text = request.form.get("Text", "")

        pred, prob = score(text, threshold=0.1)
        
        if pred == 1:
            pred = "Spam"
        else:
            pred = "Ham"

        return render_template("score.html", text=text, pred=pred, prob=round(prob,5))

if __name__ == '__main__':
    app.run(debug=True)