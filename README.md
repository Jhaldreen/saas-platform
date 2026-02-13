# SaaS Platform

This is a multi-tenant Software as a Service (SaaS) platform built with a modern technology stack. The project consists of a backend developed using Python 3.12 with FastAPI and a PostgreSQL database, and a frontend developed using React 18 with TypeScript.

## Features

- **Multi-Tenant Architecture**: Supports multiple tenants with isolated data.
- **User Authentication**: Includes registration, login, and JWT token management.
- **Dashboard**: Provides a dashboard for users to view key performance indicators.
- **Responsive Design**: Built with a mobile-first approach.

## Technology Stack

### Backend
- **Python 3.12**: Programming language for backend development.
- **FastAPI**: Web framework for building APIs quickly and efficiently.
- **PostgreSQL**: Relational database for data storage.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and settings management.

### Frontend
- **React 18**: JavaScript library for building user interfaces.
- **TypeScript**: Superset of JavaScript that adds static types.
- **Vite**: Build tool that provides a fast development environment.

## Project Structure

```
saas-platform
├── backend
│   ├── src
│   ├── tests
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── src
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
└── README.md
```

## Getting Started

### Backend

1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```
   uvicorn src.main:app --reload
   ```

### Frontend

1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run dev
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.