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

### Running the Application

1. Clone the repository:
   ```
   git clone git@github.com:jerryleooo/audio-transicribe.git
   cd audio-transicribe
   ```

2. Start the services using Docker Compose:
   ```shell
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Running Tests

```shell
make test
```
