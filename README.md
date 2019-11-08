# aiohttp-websocket-kafka-mongodb-dockerized
An example of an aiohttp server that will produce and consume kafka streams of data though a kafka cluster, store the messages on mongodb and broadcast through websockets;
The dockerized application will spawn a 3 zookeepers and 3 kafka nodes.
## Running
```
$ docker-compose build 
$ docker-compose up
```
watch the ws messages through http://localhost:8000/get-orders/