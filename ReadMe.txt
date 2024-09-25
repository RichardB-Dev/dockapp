


##Fix environmental variables
python -m venv .venv

#Install Flask on your machine
python -m pip install flask


pip install praw
pip install pandas
pip install TextBlob
pip install matplotlib
pip install seaborn
pip install wordcloud
pip install matplotlib


flask run

############
# Docker Setup + Restart
############

git pull
git reset --hard


# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)

docker build -t app1 .
# docker run app1
docker run -p 5000:5000 app1




##############
# Server setup:
#############
sudo apt install nginx



HTTPS setup
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled


sudo nano /etc/nginx/nginx.conf

#Add the following line inside the http block to include the sites-enabled directory:
include /etc/nginx/sites-enabled/*;


sudo nano /etc/nginx/sites-available/workshop32.ovh
 #PASTE IN BELOW
server {
    listen 80;
    server_name workshop32.ovh www.workshop32.ovh;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name workshop32.ovh www.workshop32.ovh;

    ssl_certificate /etc/letsencrypt/live/workshop32.ovh/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/workshop32.ovh/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;  # Flask app on port 5000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}



sudo ln -s /etc/nginx/sites-available/workshop32.ovh /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx
