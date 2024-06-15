# Discovery Server

Here [Consul](https://www.consul.io/) is configured as the discovery server.

Follow the steps to configure Consul with Docker. Make sure you have [Docker](https://www.docker.com/) installed.

1. Run the Docker image:
    ```bash
    docker run -d --name=discovery-server -p 8500:8500 -v .:/ds consul:1.15.4
    ```

2. Run Discovery Server with configs:
    ```bash
    docker exec discovery-server consul services register ds/service-registry.json
    ```
