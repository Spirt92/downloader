# Flask Download Endpoint App

This Flask application provides an endpoint to download a zipped file containing files downloaded from various URLs. The zipping process occurs asynchronously, allowing users to start downloading the file while it's being generated.

## Prerequisites

- Docker

## Usage

Clone the repository:

```git clone https://github.com/your-username/your-flask-app.git && cd your-flask-app```


## Docker Commands
- ```make build```: Build the Docker image for the Flask app.
- ```make up```: Start the Flask app container.
- ```make down```: Stop and remove the Flask app container.
- ```make logs```: Display logs from the Flask app container.
- ```make clean```: Remove the Docker image and stop the container.
- ```make bash```: Run a bash shell in the Flask app container.