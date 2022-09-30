from mlserver import MLModel, types
# from mlserver.utils import get_model_uri
from scoring import inicio
import os


class ServingModel(MLModel):
    async def load(self) -> bool:
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input = self._extract_inputs(payload)
        data = input.data[0]
        prediction_path = inicio(data)
        print(f'prediction_path: {prediction_path}')
        prediction_name = os.path.basename(prediction_path)

        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name=prediction_name,
                    shape=[1],
                    datatype="FP32",
                    data=[{"prediction_path": prediction_path}]
                )
            ]
        )

    def _extract_inputs(self, payload: types.InferenceRequest):
        inputs = payload.inputs[0]
        return inputs