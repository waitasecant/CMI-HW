import requests
import time
import subprocess
import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")


def wait_for_container_ready():
    max_retries = 10
    retry_delay = 5  # seconds

    for _ in range(max_retries):
        try:
            response = requests.post("http://localhost:5000/score", data={"Text": "sample text"}, timeout=2)

            assert response.status_code == 200

            soup = BeautifulSoup(response.text, 'html.parser')
            prediction = soup.find(id="scoreh1").text
            propensity = eval(soup.find(id="scorep").text.split(': ')[1])

            assert "Spam" in prediction or "Ham" in prediction
            assert 0.0 <= propensity and propensity <= 1.0

            return True

        except Exception as e:
            print(f"Error checking container status: {e}")

        print("Container is not ready yet, retrying...")
        time.sleep(retry_delay)

    print("Max retries exceeded, container is not ready")
    return False

def test_docker():

    # Build the Docker image
    subprocess.run(["docker", "build", "-t", "spam-classifier", "."], check=True)

    # Run the Docker container
    subprocess.run(["docker", "run", "-d", "-p", "5000:5000", "--name", "spam-container", "spam-classifier"], check=True)

    # Wait for the container to be ready
    time.sleep(5)  # Initial wait time for the container to start
    if wait_for_container_ready():
        print("Test passed!")
    else:
        print("Test failed!")

    # Close the Docker container
    subprocess.run(["docker", "stop", "spam-container"], check=True)
    subprocess.run(["docker", "rm", "spam-container"], check=True)

if __name__ == "__main__":
    test_docker()