import requests
import json


def main():
    url = "http://localhost:8080/v2/models/rep/versions/0.0.1/infer"
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
    response = requests.post(url, json=inference_request)
    print(response.json())


if __name__ == "__main__":
    main()
