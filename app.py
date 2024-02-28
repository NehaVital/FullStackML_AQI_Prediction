import pandas as pd
from flask import Flask, jsonify


app = Flask(__name__)

csv_file_path = 'aqi.csv'
data_df = pd.read_csv(csv_file_path)


@app.route('/data', methods=['GET'])
def get_data():
    data_json = data_df.to_json(orient='records')

    return jsonify({'data': data_json})

@app.route('/value', methods=['SET'])
def set_data():
    data_json = data_df.to_json(orient='records')

    return jsonify({'data': data_json})

if __name__ == '__main__':
    app.run(debug=True)
