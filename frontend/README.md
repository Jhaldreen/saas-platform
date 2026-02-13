# Frontend SaaS Platform

This is the frontend part of the multi-tenant SaaS platform built using React 18 and TypeScript. The application is designed to provide a seamless user experience for managing tenants and users.

## Project Structure

- **src/**: Contains all the source code for the frontend application.
  - **components/**: Reusable components for the application.
    - **Auth/**: Components related to authentication (Login and Registration).
    - **Dashboard/**: Components for the dashboard view.
    - **Common/**: Common components like Navbar.
  - **pages/**: Page components that represent different views in the application.
  - **services/**: API service functions for making requests to the backend.
  - **hooks/**: Custom hooks for managing state and side effects.
  - **types/**: TypeScript type definitions for the application.
  - **context/**: Context API for managing global state (e.g., authentication).
  - **styles/**: Global styles for the application.

## Getting Started

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd saas-platform/frontend
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the application**:
   ```
   npm run dev
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000` to view the application.

## Features

- User authentication (login and registration).
- Dashboard for displaying key performance indicators (KPIs).
- Multi-tenant support for managing different organizations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.