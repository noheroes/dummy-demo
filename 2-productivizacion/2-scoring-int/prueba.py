import requests
import json

url = "http://dummy-demo-rep-example-classifier.default.svc.cluster.local:9000/v2/models/rep/versions/0.0.1/infer"
# url = "http://localhost:8080/v2/models/rep/versions/0.0.1/infer"

param = json.dumps([{"x": "1"}])
inference_request = {
   "inputs": [
       {
           "name": "rep_data",
           "shape": [len(param)],
           "datatype": "FP32",
           "data": param
        }
    ]
}
print(f'inference_request: {inference_request}')
try:
    response = requests.post(url, json=inference_request)
    print(response)
    print(response.json())
except Exception as e:
    print(e)

# {'model_name': 'rep', 'model_version': '0.0.1', 'id': 'b43999b3-f633-4170-9def-05951530c5f2', 'parameters': {'content_type': None, 'headers': None}, 'outputs': [{'name': 'predict.csv', 'shape': [1], 'datatype': 'FP32', 'parameters': None, 'data': [{'prediction_path': 'http://192.168.100.246/storage/data/predict/raw/rep/predict.csv'}]}]}
