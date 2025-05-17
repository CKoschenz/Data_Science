# Setup

## Build and Export Local Docker Image

Setup the local docker image before setting up the deployment.

```shell
docker build -t the-api .
```

Export

```shell
docker save the-api > ~/tmp/the-api.tar
```

## Register Local Image to k3s

```shell
sudo k3s ctr image import ~/tmp/the-api.tar
```

check

```shell
sudo k3s ctr image ls | grep the-api
```

## Set Secret

```shell
kubectl apply -f my-secret-eval.yml
```

## Apply deployment

```shell
kubectl apply -f my-deployment-eval.yml
```

## Apply Service

```shell
kubectl apply -f my-service-eval.yml
```

## Apply Ingress

```shell
kubectl apply -f my-ingress-eval.yml
```

## Check API

Call `<ingress-IP>:8000/docs` to check API

## Additional tip from DS

Additional tip, _"You should specify the container name directly in your Python file so in your case `mysqlcontainer` for the connection to be established in FastAPI."_
