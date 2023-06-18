# Escape IT - Gamemaster Webapp for Escape Rooms

Escape IT is a Django-based web application designed for gamemasters of escape rooms. It provides the functionality to monitor multiple games simultaneously and send hints to a Unity AR app through a WebSocket. This repository contains the source code and necessary files for running the application using Docker.

## Features

- Monitor multiple escape room games in real-time.
- Send hints to a Unity AR app through a WebSocket connection.
- Easy-to-use web interface for gamemasters.
- Dockerized setup for easy deployment.

## Requirements

- Docker

## Installation and Setup

1. Clone the repository:

    git clone https://github.com/eryk-poradecki/TP_Escape_IT.git


2. Build and run the Docker container:

    build: docker-compose up --build

    run: docker-compose up

4. Open your web browser and access the application at `http://localhost:8000` or `http://127.0.0.1:8000`.

## Unity AR App

The Unity AR app that works in conjunction with Escape IT can be found in the following repository:

- Repository: [TP_Escape_IT_Unity](https://github.com/eryk-poradecki/TP_Escape_IT_Unity)

Please refer to the Unity app repository for instructions on how to set up and use the AR app.

## Project Creators

The following individuals have contributed to the development of Escape IT:

1. Dawid Borkowski
- GitHub: [dawidborkowski](https://github.com/dawidborkowski)
- Role: Backend Developer

2. Mateusz Kubiak
- GitHub: [mat-kubiak](https://github.com/mat-kubiak)
- Role: Unity Developer

3. Eryk Poradecki
- GitHub: [eryk-poradecki](https://github.com/eryk-poradecki)
- Role: Backend Developer

4. Mateusz Pryl
- GitHub: [MateuszPryl](https://github.com/MateuszPryl)
- Role: Frontend Developer

5. Sylwia Sielska
- GitHub: [szylviaaa](https://github.com/szylviaaa)
- Role: Frontend Developer

## License

This project is licensed under the [MIT License](LICENSE).