from mlserver import MLModel, types
# from mlserver.utils import get_model_uri
from scoring import inicio
import os


class ServingModel(MLModel):
    async def load(self) -> bool:
        # model_uri = await get_model_uri(self._settings)
        # print(f"model_uri:{model_uri}")
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) ->
    types.InferenceResponse:

        # input = self._extract_inputs(payload)
        prediction_path = inicio()
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