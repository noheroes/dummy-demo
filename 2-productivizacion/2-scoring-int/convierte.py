import pandas as pd

data = pd.read_csv("input_rep.csv")
json = data.to_json(orient="records")
with open("input_rep.json", "w") as f:
    f.write(json)
