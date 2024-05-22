# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project build output to the container
COPY target/discovery-server-0.0.1-SNAPSHOT.jar /app/discovery-server.jar

# Make port 8761 available to the world outside this container
EXPOSE 8761

# Run the Eureka server application
ENTRYPOINT ["java", "-jar", "discovery-server.jar"]
