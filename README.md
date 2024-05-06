# Website with Secure Authentication, Databases, and Multiplayer Games

This project creates a website that includes secure user authentication, database support, and two games: a memory game and a Pong game with remote multiplayer capabilities. It also includes monitoring services for system health and container performance.

## Setup Instructions

To set up the website, follow these steps:

1. Run the following command to prepare the environment:
   ```sh
   make prepare
   ```
2. After preparation, build and start all services with:
   ```sh
   make all
   ```
Once the setup is complete, the website will be available at:
[https://localhost:9999](https://localhost:9999)

## Monitoring Services

The project includes monitoring services for tracking the health of containers and the hosting machine:

- **Prometheus**: Collects metrics and provides monitoring data.
- **Grafana**: Visualizes the collected data on customizable dashboards.

Grafana dashboards can be accessed at:
[https://localhost:3000](https://localhost:3000)

## Secrets and Environment Variables

Environment variables and secrets are stored in a `.env` file. This approach is **!only for educational purposes!** and should not be used in production environments.

## Games Included

The project includes two games:

- **Memory Game**: A classic memory card-matching game.
- **Pong**: A simple Pong game with remote multiplayer support.

## Notes and Warnings

- The project is designed for educational purposes, so exercise caution when dealing with sensitive information.
- Ensure you have proper security measures in place when deploying in production.

---

Happy coding!
