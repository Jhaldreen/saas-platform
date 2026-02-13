FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies for healthcheck
RUN apk add --no-cache wget curl

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Run Vite dev server with host 0.0.0.0 to allow external connections
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]