echo "################################## Run nginx"
export DOLLAR='$'
envsubst < /tmp/nginx.conf.template > /etc/nginx/nginx.conf
nginx -g "daemon off;"
