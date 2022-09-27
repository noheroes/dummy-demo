from kubernetes import client, config


def create_predictor(model_name, model_type):
    predictor = {
        "apiVersion": "serving.kserve.io/v1beta1",
        "kind": "InferenceService",
        "metadata": {"name": model_name},
        "spec": {
            "predictor": {
                "containers": {
                    "name": model_type,
                    "image": "noheroes/regression:latest",
                    "env": {
                        "name": "PROTOCOL",
                        "value": "v2"
                    },
                    "ports": {
                        "containerPort": "8080",
                        "protocol": "TCP"
                    }
                }
            }
        },
    }
    return predictor


def create_custom_image():
    return


def deploy(model_name, model_type):
    config.load_kube_config()
    api = client.CustomObjectsApi()

    customObject = api.create_namespaced_custom_object(
        group="networking.istio.io",
        version="v1beta1",
        namespace="kubeflow",
        plural="inferenceservices",
        body=create_predictor(model_name, model_type)
    )
    print(customObject)


def main():
    deploy("", "")


if __name__ == '__main__':
    main()