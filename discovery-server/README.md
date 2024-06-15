# Discovery Server

Here [Consul](https://www.consul.io/) is configured as the discovery server.

Follow the steps to configure Consul with Docker. Make sure you have [Docker](https://www.docker.com/) installed.

1. Pull the Docker image:
    ```bash
    docker pull consul:1.15.4
    ```

2. Run Consul:
    ```bash
    docker run -d -p 8500:8500 -p 8600:8600/udp --name=badger consul:1.15.4 agent -server -ui -node=server-1 -bootstrap-expec t=1 -client=0.0.0.0
    ```





