from flask import Flask, render_template, request, Response
import json
# Create the Flask application
app = Flask(__name__)

# Define a route for the root URL


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/sensitivity', methods=['POST'])
def sensitivity_():
    data = request.json
    print(data, "DATA")
    with open("../../settings.json", 'r+') as file:
        curSettings = {}
        s = file.read()
        if s:
            curSettings = json.loads(s)
        curSettings["sensitivity"] = data['value']
        print(curSettings)

    with open("../settings.json", "w") as file:
        json.dump(curSettings, file, indent=4)
    return Response("{}", status=200, mimetype='application/json')


@app.route('/lefteye', methods=['POST'])
def lefteye():
    data = request.json
    print(data, "DATA")
    with open("../settings.json", 'r+') as file:
        curSettings = {}
        s = file.read()
        if s:
            curSettings = json.loads(s)
        curSettings["lefteye"] = float(data['value']) / 1000

    with open("../settings.json", "w") as file:
        json.dump(curSettings, file, indent=4)
    return Response("{}", status=200, mimetype='application/json')


@app.route('/righteye', methods=['POST'])
def righeye():
    data = request.json
    print(data, "DATA")
    with open("../settings.json", 'r+') as file:
        curSettings = {}
        s = file.read()
        if s:
            curSettings = json.loads(s)
        curSettings["righteye"] = float(data['value']) / 1000
        print(curSettings)

    with open("../settings.json", "w") as file:
        json.dump(curSettings, file, indent=4)
    return Response("{}", status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
