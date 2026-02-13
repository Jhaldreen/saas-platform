# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json* ./

# Install dependencies (ci is preferred in Docker for production)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Runtime stage - using lightweight nginx to serve the built app
FROM node:18-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser

# Copy built application from builder
COPY --from=builder --chown=appuser:appuser /app/dist ./dist
COPY --from=builder /app/package.json ./

# Install only production dependencies for preview server
RUN npm ci --omit=dev

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:5173', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})" || exit 1

# Run the preview server
CMD ["npm", "run", "serve"]
