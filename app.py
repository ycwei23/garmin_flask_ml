from flask import Flask, request, jsonify
import json

app = Flask(__name__)

#用flask return index.html
@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

 

@app.route('/api', methods=['POST'])
def process_request():
    data = request.get_json()
    
    response = data
    filename = data['username']
    write_json(data, filename)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run()

#寫一個function，讀入json資料，並且建立一個新的json檔案，並且把資料寫入
def write_json(data, filename):
    with open('jsonData/' + filename + '.json','w') as f:
        json.dump(data, f, indent=4)
