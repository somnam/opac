FROM nginxinc/nginx-unprivileged:stable-alpine

# Copy application files
COPY --chown=nginx:nginx ./client /usr/share/nginx/html

# Run app
CMD ["nginx", "-g", "daemon off;"]
