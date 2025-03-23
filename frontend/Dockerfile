FROM node:16-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Use npm install instead of npm ci to update package-lock.json
RUN npm install

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build output from build stage to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 