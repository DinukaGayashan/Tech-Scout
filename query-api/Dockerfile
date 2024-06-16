# syntax=docker/dockerfile:1

FROM golang:latest

WORKDIR /query-api

COPY go.mod go.sum ./

COPY config.yaml config.yaml

RUN go mod download

COPY src/*.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /query-api-binary

EXPOSE 8001

ENTRYPOINT ["/query-api-binary"]