FROM nginxinc/nginx-unprivileged:stable-alpine

# Copy websocket proxy configuration.
COPY --chown=nginx:nginx ./docker/proxy/default.conf /etc/nginx/conf.d/

# Run app
CMD ["nginx", "-g", "daemon off;"]
