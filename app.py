from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    total_time = 0
    latency = 0
    status = 0
    return render_template('home.html')

@app.route('/', methods=['POST'])
def check_website():
    total_time = 0
    latency = 0
    status = 0
    url = request.form['url']
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        status = response.status_code
        latency = round((time.time() - start_time), 2)
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
    return render_template('home.html', message=message, latency=latency, total_time=total_time, status=status, url=url)



@app.route('/api/<path:url>', methods=['GET', 'POST'])
def api_check_website(url):
    total_time = 0
    latency = 0
    status = 0
    if not url.startswith('http'):
        url = 'http://' + url

#    response = None

    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start_time), 2)
        total_time = round(response.elapsed.total_seconds(), 2)
        if response.status_code == 200:
            message = f"{url} esta vivo"
            status = f"sucesso {str(response.status_code)}"
        else:
            message = f"{url} retornou um erro {response.status_code}"
            status = f"erro {str(response.status_code)}"
    except requests.exceptions.Timeout:
        message = f"{url} time out"
        status = f"erro 408"
    except requests.exceptions.ConnectionError:
        message = f"{url} nao pode ser alcancado"
        status = f"erro 500"
    except Exception as e:
        message = str(e)
        status = f"erro 500"

    return jsonify({'status': status, 'message': message, 'latency': latency, 'total_time': total_time})

if __name__ == '__main__':
    app.run(debug=False)
