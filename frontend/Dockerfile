# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json* ./

# Install all dependencies (including dev deps for build)
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Runtime stage
FROM node:18-alpine

WORKDIR /app

# Create non-root user for security (use different uid to avoid conflicts)
RUN addgroup -g 1001 appuser && adduser -D -u 1001 -G appuser appuser

# Copy built application from builder
COPY --from=builder --chown=appuser:appuser /app/dist ./dist
COPY --from=builder /app/package.json ./

# Install only production dependencies for preview server
RUN npm install --production

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:5173', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})" || exit 1

# Run the preview server
CMD ["npm", "run", "serve"]
