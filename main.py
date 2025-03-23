from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json

    number = data.get('number')
    body = data.get('body')

    if not number or not body:
        return jsonify({'error': 'number and body are mandatory'}), 400

    body = body.replace(' ', '\\ ')

    command = [
        'adb', 'shell', 'service', 'call', 'isms', '5', 'i32', '1',
        's16', 'com.android.mms.service',
        's16', 'null',
        's16', number,
        's16', 'null',
        's16', body,
        's16', 'null',
        's16', 'null',
        'i32', '1',
        'i32', '0'
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        if "Result: Parcel(00000000    '....')" in output:
            return jsonify({'message': 'SMS sent successfully'}), 200
        else:
            return jsonify({'error': output}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr.strip()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
