FROM library/nginx
RUN rm /etc/nginx/conf.d/default.conf 
COPY recordexpunge-nginx.dev.conf /etc/nginx/conf.d/
COPY static/ /usr/share/nginx/html

EXPOSE 3000


