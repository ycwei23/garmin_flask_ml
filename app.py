#!/home/ec2-user/garmin_flask_ml/myenv/bin/python
from flask import Flask, request, jsonify, render_template
import pyhrv.frequency_domain as fd
import numpy as np
import scipy.interpolate as interp
from datetime import datetime
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api', methods=['POST'])
def process_request():
    data = request.get_json()
    

    response = data
    
    return jsonify(response)

@app.route('/api/aaa', methods=['POST'])
def process_request1():
    return request


@app.route('/api/iosapp/bbi_analysis', methods=['POST'])
def api_iosapp_bbi_analysis():
    if request.method=='POST':
        data=request.get_json()
    #這個data就是iosapp傳過來的資料，是json個格式
    #要取data裡的"garmin_data_bbi"

    for item in data['garmin_data_bbi'] :
        timestamp = item['timestamp'] / 1000
        datetime_obj = datetime.fromtimestamp(timestamp)
        #秒數到小數地3位
        formatted_datetime = datetime_obj.strftime("%H:%M:%S.%f")

        item['timestamp'] = formatted_datetime


    timestamps = []
    values = []

    # 解析數據中的時間和數值
    for entry in reversed(data["garmin_data_bbi"]):
        if 'timestamp' in entry:
            timestamp_str = entry['timestamp']
            value = float(entry['bbi'])

            # 解析時間格式
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f')

            timestamps.append(timestamp)
            values.append(value)
    # 轉換時間為秒數
    time_in_seconds = [(t - timestamps[0]).total_seconds() for t in timestamps]

    # 計算心跳間隔（RR間期）
    rr_intervals = np.diff(time_in_seconds)
    print(rr_intervals)

    # 計算平均 RR 間隔和 SDNN（標準差）
    mean_rr_interval = np.mean(rr_intervals)
    SDNN = np.std(rr_intervals)

    # 計算 SDSD（連續兩次 RR 間隔的標準差）
    SDSD = np.std(np.diff(rr_intervals))

    # 使用Welch方法進行頻域分析，提取PSD
    frequency_results = fd.welch_psd(rr_intervals)

    # 計算LF/HF比值
    lf = frequency_results[3][1]  # LF功率（索引1對應LF）
    hf = frequency_results[3][2]  # HF功率（索引2對應HF）
    lf_hf_ratio = lf / hf

    # 繪製Poincaré圖
    x = rr_intervals[:-1]  # RR(n)
    y = rr_intervals[1:]   # RR(n+1)

    # 計算SD1和SD2
    sd1 = round(np.std(y - x) / np.sqrt(2), 3)
    sd2 = round(np.std(y + x) / np.sqrt(2), 3)

    # 計算SD1/SD2
    sd1_sd2_ratio = round(sd1 / sd2, 3)

    #這個key值裡的結構者這樣
    """
    {
        "garmin_data_bbi" : [
            {
                "timestamp" : 1689752533567,
                "bbi" : 668
            },
            {
                "timestamp" : 1689752531903,
                "bbi" : 622
            }
        ]
    }
    """
    #是一個array
    sd1 = sd1
    sd2 = sd2
    sd1_sd2 = sd1_sd2_ratio
    sdnn = SDNN
    sdsd = SDSD
    sd1_content = "這裡是sd1的分析"
    sd2_content = "這裡是sd2的分析"
    sd1_sd2_content = "這裡是sd1_sd2的分析"
    sdnn_content = "這裡是sdnn的分析"
    sdsd_content = "這裡是sdsd的分析"
    return {
        "sd1" : sd1,
        "sd2" : sd2,
        "sd1_sd2" : sd1_sd2,
        "sdnn" : sdnn,
        "sdsd" : sdsd,
        "sd1_content" : sd1_content,
        "sd2_content" : sd2_content,
        "sd1_sd2_content" : sd1_sd2_content,
        "sdnn_content" : sdnn_content,
        "sdsd_content" : sdsd_content
    }

if __name__ == '__main__':
    app.run()
