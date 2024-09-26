from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def root():
    pass


@app.route('/iframe')
def iframe():
    return render_template('iframe.html')

@app.route('', methed = ['POST'])
def receive_message():
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True)

