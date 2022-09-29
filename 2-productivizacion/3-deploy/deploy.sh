#!/bin/sh

build()
{
  cd ../../2-productivizacion/2-scoring
  docker build --no-cache -t noheroes/mlserver-rep-scoring:latest .
  docker push noheroes/mlserver-rep-scoring:latest
}
echo building...
build
echo deploying...
cd ../3-deploy
kubectl delete -f mlserver-rep-seldon.yaml
kubectl apply -f mlserver-rep-seldon.yaml
echo done...
