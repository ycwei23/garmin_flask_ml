from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def process_request():
    data = request.get_json()
    
    response = {'message': '成功', 'data': data}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run()