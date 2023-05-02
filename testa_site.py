from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    latency = None
    return render_template('home.html')

@app.route('/', methods=['POST'])
def check_website():
    latency = None
    url = request.form['url']
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start_time), 2)
        print(latency)
        total_time = round(response.elapsed.total_seconds(), 2)
        if response.status_code == 200:
            message = f"{url} is reachable with {latency} s latency. Total loading time: {total_time} s"
        else:
            message = f"{url} returned a {response.status_code} error"
    except requests.exceptions.Timeout:
        message = f"{url} timed out"
    except requests.exceptions.ConnectionError:
        message = f"{url} could not be reached"
    except Exception as e:
        message = str(e)
    return render_template('home.html', message=message, latency=latency, total_time=total_time, status=response.status_code)

@app.route('/api/check_website', methods=['GET', 'POST'])
def api_check_website():
    latency = None
    url = request.json['url']
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start_time), 2)
        total_time = round(response.elapsed.total_seconds(), 2)
        if response.status_code == 200:
            #message = f"{url} is reachable with {latency} s latency. Total loading time: {total_time} s"
            message = f"{url} is reachable"
            status = "success"
        else:
            message = f"{url} returned a {response.status_code} error"
            status = "error"
    except requests.exceptions.Timeout:
        message = f"{url} timed out"
        status = "error"
    except requests.exceptions.ConnectionError:
        message = f"{url} could not be reached"
        status = "error"
    except Exception as e:
        message = str(e)
        status = "error"

    return jsonify({'status': status, 'message': message, 'latency': latency, 'total_time': total_time})

if __name__ == '__main__':
    app.run(debug=True)
