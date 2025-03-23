# Audio Transcription Service

A full-stack application for transcribing audio files using the Whisper speech recognition model.

## Features

- Upload and transcribe audio files (single or batch)
- View all transcriptions
- Search transcriptions by filename
- RESTful API for integration with other services

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.9+
- Node.js 18+
- FFmpeg
- Make

### Running the Application

1. Clone the repository:
   ```
   git clone git@github.com:jerryleooo/audio-transicribe.git
   cd audio-transicribe
   ```

#### Running with Docker

1. Build the Docker images:
   ```shell
   make build
   ```

2. Start the services:
   ```shell
   make up
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

4. View logs:
   ```shell
   make logs
   ```

5. Stop the services:
   ```shell
   make down
   ```

#### Local Development

1. Setup local development environment:
   ```shell
   make local-setup
   ```

2. Run backend locally (For first time running, it might take a while to download the model weights):
   ```shell
   make local-backend
   ```
   > **Note**: The first run will download the Whisper model weights (150MB-3GB depending on the model size) and may take several minutes.

3. Run frontend locally:
   ```shell
   make local-frontend
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

5. Clean up local development environment:
   ```shell
   make local-clean
   ```

#### Running Tests

Run all tests:
```shell
make local-test
```

Run only backend tests:
```shell
make local-test-backend
```

Run only frontend tests:
```shell
make local-test-frontend
```
