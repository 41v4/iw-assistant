# Intus Windows AI Chatbot

## Brief Summary
A simple LLM-based chatbot assistant web application specialized in window manufacturing, built using FastAPI, DaisyUI, and the OpenAI API.

## Features
- AI-powered responses strictly limited to window manufacturing queries
- Robust system prompt ensuring the chatbot stays on-topic and refuses to engage with unrelated queries or attempts at jailbreaking
- User-friendly web interface for easy interaction
- RESTful API for seamless integration with other systems in the window manufacturing workflow

## Technologies Used
- FastAPI: Modern, fast (high-performance) web framework for building APIs/web applications with Python
- DaisyUI: Tailwind CSS component library
- OpenAI API: For natural language processing and generation
- Docker: For containerization and easy deployment

## System Flowchart
Please check the `iw_assistant_flowchart.html` file (located in this repository) by downloading and opening in your browser. This flowchart provides a visual representation of the system's architecture and data flow.

## Prerequisites
- Docker
- Docker Compose

## Setup and Running with Docker

1. Clone the repository:
   ```
   git clone https://github.com/41v4/iw-assistant
   cd iw-assistant
   ```

2. Set up environment variables:
   - For Unix-based systems:
     ```
     cp .env.example .env
     ```
   - For Windows:
     Manually copy the `.env.example` file, paste it in the same directory, and rename it to `.env`.

   Open the `.env` file and replace the placeholder values with your actual configuration.

3. Build and run the Docker container:
   ```
   docker-compose build
   docker-compose up -d
   ```

The application should now be running and accessible at `http://localhost:8000`.

4. To stop the Docker container:
   ```
   docker-compose stop
   ```

## Environment Variables

The following environment variable is required:

- `OPENAI_API_KEY`: Your OpenAI API key

Ensure this variable is set in your `.env` file.
