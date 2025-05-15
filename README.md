# 💱 Currency Converter Microservice

A FastAPI-based microservice for currency conversion built with 12-Factor methodology principles.

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker&logoColor=white)

## Features

- Convert between 150+ currencies using real-time exchange rates
- Redis caching for improved performance
- Streamlit web interface for easy use
- Containerized services with Docker and Docker Compose
- CI/CD pipeline with GitHub Actions

## Architecture

This project demonstrates the implementation of the 12-Factor App methodology with:

1. **Codebase**: Single codebase tracked in Git
2. **Dependencies**: Explicitly declared dependencies using Poetry
3. **Config**: Configuration stored in environment variables
4. **Backing Services**: Redis treated as an attached resource
5. **Build, Release, Run**: Separated build and run stages with Docker
6. **Processes**: Stateless processes that share nothing
7. **Port Binding**: Service exported via port binding
8. **Concurrency**: Horizontal scaling possible through the process model
9. **Disposability**: Fast startup and graceful shutdown
10. **Dev/Prod Parity**: Development environment matches production
11. **Logs**: Treated as event streams
12. **Admin Processes**: Admin tasks as one-off processes

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)

### Running with Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/currency-converter.git
   cd currency-converter
   ```

2. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

3. (Optional) If you want to use a specific API key, edit the `.env` file:
   ```bash
   EXCHANGE_API_KEY=your_api_key
   ```

4. Start the services:
   ```bash
   docker-compose up
   ```

5. Access the applications:
   - FastAPI service: http://localhost:8000/docs
   - Streamlit UI: http://localhost:8501

### Local Development

1. Install dependencies:
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install using Poetry
   pip install poetry
   poetry install
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run tests:
   ```bash
   pytest
   ```

4. Start the API service:
   ```bash
   uvicorn app.main:app --reload
   ```

5. In a separate terminal, start the Streamlit app:
   ```bash
   streamlit run streamlit_app/app.py
   ```

## API Documentation

Once the service is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the tests with:

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
