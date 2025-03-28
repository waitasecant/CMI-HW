import pytest
from score import score
import requests
import time
import subprocess
import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")


def test_smoke():
    try:
        score("Example", 0.5)
    except Exception as e:
        pytest.fail(f"score function raised an exception: {e} (Smoke test failed)")
    
    assert type(score("Example", 0.5)) == tuple, f"Expected 2 outputs, received 1 (smoke test failed)"
    assert len(score("Example", 0.5)) == 2, f"Expected 2 outputs, received {len(score('Example', 0.5))} (smoke test failed)"

def test_format():
    text = "Example"
    threshold = 0.7
    prediction, probability = score(text, threshold)
    assert type(prediction) == int
    
    try:
        float(probability)
    except Exception as e:
        pytest.fail(f"score function raised an exception: {e} (Format test failed)")

def test_prediction_0_or_1():
    text = "Example"
    threshold = 0.7
    prediction, _ = score(text, threshold)
    assert prediction in (0, 1)

def test_propensity_between_0_and_1():
    text = "Example"
    threshold = 0.7
    _, propensity = score(text, threshold)
    assert 0<=propensity<=1

def test_when_threshold_0_prediction_always_1():
    text_1 = "Be there tonight"
    threshold = 0
    prediction, _ = score(text_1, threshold)
    assert prediction == 1
    
    text_2 = "Get a chance to go on a vacation to Hawaii"
    threshold = 0
    prediction, _ = score(text_2, threshold)
    assert prediction == 1

def test_when_threshold_1_prediction_always_0():
    text_1 = "Be there tonight"
    threshold = 1
    prediction, _ = score(text_1, threshold)
    assert prediction == 0
    
    text_2 = "Get a chance to go on a vacation to Hawaii"
    threshold = 1
    prediction, _ = score(text_2, threshold)
    assert prediction == 0

def test_obvious_spam_gives_prediction_1():
    text = '''Thanks for your ringtone order reference number X number Your mobile will be charged number .
              Should your tone not arrive please call customer services number'''
    threshold = 0.7
    prediction, _ = score(text, threshold)
    assert prediction == 1

def test_obvious_non_spam_gives_prediction_0():
    text = "Don't be late for tomorrow's meeting"
    threshold = 0.4
    prediction, _ = score(text, threshold)
    assert prediction == 0

def test_flask():
    # Start Flask app
    process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE)
    time.sleep(5)

    payload = {"Text": "Hello, congratulations! You have won a prize."}

    response = requests.post("http://127.0.0.1:5000/score", data=payload)

    assert response.status_code == 200
    
    soup = BeautifulSoup(response.text, 'html.parser')

    prediction = soup.find(id="scoreh1").text
    propensity = eval(soup.find(id="scorep").text.split(': ')[1])
    assert "Spam" in prediction or "Ham" in prediction
    assert 0.0 <= propensity and propensity <= 1.0

    process.terminate()


if __name__ == "__main__":
    test_smoke()
    test_format()
    test_prediction_0_or_1()
    test_propensity_between_0_and_1()
    test_when_threshold_0_prediction_always_1()
    test_when_threshold_1_prediction_always_0()
    test_obvious_spam_gives_prediction_1()
    test_obvious_non_spam_gives_prediction_0()
    test_flask()