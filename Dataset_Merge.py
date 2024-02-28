import pandas as pd
from flask import Flask, jsonify

result_df = pd.read_csv('AQI_Weather.csv')
aqi_df = pd.read_csv('aqi.csv')
merged_df = pd.merge(result_df, aqi_df, on=['Date', 'Time'], how='inner')

print(merged_df)
merged_df.to_csv('AQIPredictionUpdated.csv', index=False)


# app = Flask(__name__)
#
# csv_file_path = 'AQIPredictionUpdated.csv'
# data_df = pd.read_csv(csv_file_path)
#
#
# @app.route('/data', methods=['GET'])
# def get_data():
#     data_json = data_df.to_json(orient='records')
#
#     return jsonify({'data': data_json})
#
# @app.route('/value', methods=['SET'])
# def set_data():
#     data_json = data_df.to_json(orient='records')
#
#     return jsonify({'data': data_json})
#
# if __name__ == '__main__':
#     app.run(debug=True)
