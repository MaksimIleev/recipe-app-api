server {
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass            ${APP_HOST}:${APP_PORT};
        include               /etc/nginx/uwsgi_params;
        client_max_body_size  10M;
        add_header            'Access-Control-Allow-Origin' '*' always;
        add_header            'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header            'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization' always;
    }
}