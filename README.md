# Tech-Scout

A distributed system for aggregating product details from tech websites, offering a REST API for easy access to availability and pricing information. It saves time for users by eliminating manual comparison and stock checks. It also aids shops in conducting market analysis with comprehensive product data.


## Architecture
The system is designed as a distributed system using the microservice architecture.

![Alt text](https://raw.githubusercontent.com/DinukaGayashan/Tech-Scout/098e090cfad0b93ab23aec4ff3d9748fee0bbf0e/distributed-system-design.svg)

The application is split into different services to ensure modularity, scalability, and maintainability. Each service is responsible for a specific task.

- **Reference Data Scraper**: Collects reference data.
- **Data Scraper**: Collects raw data from various sources.
- **Data Processor**: Matches products and structures data.
- **Query API**: Provides access to the structured data.
- **Authorization**: Manages access control across the system.
- **API Gateway**: Central entry point for external requests.
- **Discovery Server**: Manages service discovery.
- **Logging & Monitoring**: Ensures system health and performance.


## Microservices

The application leverages 

### Core Services

#### Reference Data Scraper
- **Functionality**: Scrapes reference data from predefined sources.
- **API Endpoints**:
  - `POST /scrape-all`: Start scraping.
  - `GET /get-all?category={category}`: Retrieve reference data.
  - `GET /status`: Service status.
  - `DELETE /delete-data/{time}`: Delete reference data.
- **Inter-service Interactions**: Communicates with the Authorization service for access control.

#### Data Scraper
- **Functionality**: Scrapes raw data from various sources.
- **API Endpoints**:
  - `POST /process`: Start website scraping.
  - `GET /data?category={category}`: Initiate a new data scrape.
  - `GET /status`: Service status.
  - `DELETE /delete-data/{time}`: Delete scraped data.
- **Inter-service Interactions**: Interacts with Authorization and Data Processor services.

#### Data Processor
- **Functionality**: Processes scraped data to match products and structure it.
- **API Endpoints**:
  - `POST /process`: Start processing data.
  - `POST /push`: Push processed data.
  - `GET /status`: Service status.
  - `DELETE /delete-data/{time}`: Delete processed data.
- **Inter-service Interactions**: Consumes data from Data Scraper and Reference Data Scraper services.

#### Query API
- **Functionality**: Provides access to structured data.
- **API Endpoints**:
  - `GET /query/{category}`: Query structured data.
  - `GET /query-by-name/{category}`: Query structured data by name.
  - `GET /query-by-spec/{category}`: Query structured data by spec.
  - `GET /query-by-shop/{category}`: Query structured data by shop.
  - `GET /query-by-price/{category}`: Query structured data by price.
  - `GET /status`: Service status.
- **Inter-service Interactions**: Retrieves data from the Data Processor.

### Discovery Server
- **Functionality**: Services register with the Discovery Server upon startup. The server maintains a registry of available services and their instances. It monitors the health of services and removes any that are no longer available.
- **Implementation**: Uses Consul for service discovery and registration.

### API Gateway
- **Functionality**: Acts as a single entry point for external requests, routing them to the appropriate services.
- **Configuration**: Configured using Spring Cloud Gateway. Handles routing, filtering, and load balancing.


## User Interface



## Deployment

### Local Deployment
1. Clone the repository: `git clone https://github.com/DinukaGayashan/Tech-Scout.git`
2. Navigate to the project directory: `cd Tech-Scout`
3. Start each service using terminal commands: `./start_service.sh`
4. Access the UI at `http://localhost:3000`

### Cloud Deployment
1. Set up a VM in a cloud environment (AWS, GCP, Azure)
2. Export necessary ports to public
3. Install Docker
4. Run the system with Docker compose


## Source Code
- **GitHub Repository**: [https://github.com/DinukaGayashan/Tech-Scout](https://github.com/DinukaGayashan/Tech-Scout)
- **Development Challenges**: Faced issues with service discovery and load balancing. Solved by configuring Eureka and Zuul properly. Encountered data consistency issues, resolved through transaction management and data validation.


## References
- [Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway)
- [Consul](https://www.consul.io/)
- [Go Gin Gonic](https://pkg.go.dev/github.com/gin-gonic/gin)
- [Python](https://www.python.org/)
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Docker](https://docs.docker.com/)
- [Postman](https://www.postman.com/)
