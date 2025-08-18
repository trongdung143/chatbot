# AI Chatbot Project

A sophisticated chatbot system built with Python, featuring document analysis, RAG (Retrieval-Augmented Generation), and conversation management capabilities.

## Project Structure

```
├── src/
│   ├── agents/             
│   │   ├── analysis/       # Document analysis components
│   │   ├── chat/          # Chat handling components
│   │   └── manage/        # Management utilities
│   ├── api/                # API endpoints
│   ├── config/             # Configuration files
│   ├── database/           # Database models and connections
│   ├── prompts/            # Prompt templates and handlers
│   ├── tools/              # Utility tools and helpers
│   └── utils/              # General utilities
├── static/                 # Frontend assets
├── tests/                  # Test files
├── docker-compose.yml      # Docker composition file
├── Dockerfile             # Docker container definition
├── nginx.conf            # Nginx configuration
└── requirements.txt      # Python dependencies
```

## Features

- Document Analysis with RAG (Retrieval-Augmented Generation)
- Real-time Chat Interface
- User Session Management
- File Upload/Download Capabilities
- Database Integration with PostgreSQL
- Docker Containerization
- Nginx Reverse Proxy Support

## Prerequisites

- Python 3.12+
- PostgreSQL Database
- Docker (optional)
- Nginx (for production deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/trongdung143/chatbot.git
cd chatbot
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
   - Create a `.env` file in the project root
   - Add your database configuration:
   ```
   DATABASE_URL=postgresql+psycopg://user:password@host:port/database
   ```

5. Initialize the database:
```bash
python -m src.config.setup
```

## Running the Application

### Development Mode

```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080
```

### Using Docker

```bash
docker-compose up --build
```

## API Endpoints

- `/api/chat` - Chat interface endpoints
- `/api/login` - Authentication endpoints
- `/api/download` - File download endpoints
- `/api/home` - Home page and main functionality

## Configuration

### Database Configuration

Database settings can be configured in `src/config/database.py`. The application uses SQLAlchemy with PostgreSQL.

### System Configuration

System-wide settings and configurations are managed in `src/config/setup.py`.

## Development

### Adding New Agents

1. Create a new agent file in `src/agents/`
2. Implement the agent interface
3. Register the agent in `src/agents/workflow.py`

### Creating New API Endpoints

1. Add new route file in `src/api/`
2. Implement the endpoint handlers
3. Register routes in `src/main.py`

## Testing

Run tests using:
```bash
python -m pytest tests/
```

## Deployment

### Using Docker

```bash
docker-compose up -d --build
```

### Manual Deployment

1. Set up Nginx using the provided `nginx.conf`
2. Configure SSL certificates
3. Start the application using a production WSGI server

## System Scripts

The `src/config/system/` directory contains useful scripts for:
- Starting/stopping the server
- System restart
- Ngrok tunneling setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
