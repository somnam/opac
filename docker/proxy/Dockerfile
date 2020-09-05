FROM nginxinc/nginx-unprivileged:stable-alpine

# Copy websocket proxy configuration.
COPY --chown=nginx:nginx ./docker/proxy/00-client.conf /etc/nginx/conf.d/
COPY --chown=nginx:nginx ./docker/proxy/10-server.conf /etc/nginx/conf.d/

# Run app
CMD ["nginx", "-g", "daemon off;"]
