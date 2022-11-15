#!/bin/sh

build()
{
  cd ../../2-productivizacion/2-scoring-int
  docker build --no-cache -t noheroes/mlserver-rep-scoring-int:latest .
  docker push noheroes/mlserver-rep-scoring-int:latest
}
echo building...
build
echo deploying...
cd ../3-deploy
kubectl delete -f mlserver-rep-seldon-int.yaml
kubectl apply -f mlserver-rep-seldon-int.yaml
echo done...
