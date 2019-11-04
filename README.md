# Chat App

This is a simple chat applcation with live updates and
persistent storage implemented in flask and mongodb.

[Report for assignment](report/)

## Modules

### Application

The application uses flask for basic web requests serving
and flask-socketio as a live sockets manager.

Sources were adopted from [this article][app-source].
[app-source]: https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d

### MongoDB

MongoDB is represented as three nodes combined together
in a replica set. The first one is the primary one.

Configuration was taken from [this post][mongo-source].
[mongo-source]: https://37yonub.ru/articles/mongo-replica-set-docker-localhost

## Deploy

Deploy process involves building images for application
and database, publishing these images and deploying them
via docker swarm.

### Build

There are three containers of the mongodb service and one
of the flask application in a Compose file. All of them
have to be built from the appropriate Dockerfile.

```bash
# Command for building
docker-compose build
```

### Publish

After the build you'll have two new images:

* `regzon/mongo:4.2`
* `regzon/chat-application:latest`

To publish them you need an access to my DockerHub
repository or you could just change name of the images
in a Compose file.

```bash
# Command for publishing
docker-compose push
```

> Don't forget to authenticate with `docker login`.

Image links:
* [mongo][mongo-image]
* [chat-application][chat-app-image]

[chat-app-image]: https://cloud.docker.com/repository/docker/regzon/chat-application
[mongo-image]: https://cloud.docker.com/u/regzon/repository/docker/regzon/mongo

### Swarm Deploy

For this step you should configure a stack (create a swarm).
[You can read more about it here][swarm-guide].
[swarm-guide]: https://docs.docker.com/engine/swarm/swarm-mode/

Now, containers can be deployed with the following command:

```bash
docker stack deploy -c docker-compose.yml chat
```

Services will start an initialization process and after
some time will be fully functional. Chat application
service will be published and will be accessible via http
from any ip of host configured in your swarm.

To check the status of your services, run:

```bash
docker service ls
```

To remove the services:

```bash
docker stack rm chat
```
