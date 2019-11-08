# aiohttp-websocket-kafka-mongodb-dockerized
An example of an aiohttp server that will produce and consume kafka streams of data though a kafka cluster, store the messages on mongodb and broadcast through websockets;
The dockerized application will spawn a 3 zookeepers and 3 kafka nodes.

## Running
```
$ docker-compose build 
$ docker-compose up
```
Watch a real time graph with this data at http://localhost:8000/get-orders/
![alt text](https://github.com/jersobh/aiohttp-websocket-kafka-mongodb-dockerized/raw/master/graph.gif "Real Time Graph")
