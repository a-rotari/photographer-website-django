# Photography Website 
##### - Built using Django and SCSS
##### - Running using Docker on AWS (EC2, S3, Cloudfront, SES)
##### - Using MariaDB on host EC2, and served with NGINX



- [Project Overview](#project-overview)
    - [Main Purpose](#main-purpose)
    - [User-Centric Functionality](#user-centric-functionality)
    - [Styling](#styling)
    - [Responsive Images and Lazy Loading](#responsive-images-and-lazy-loading)
    - [Storing Data](#storing-data)
    - [Processing Images with PIL](#processing-images-with-pil)
 - [Deploying the Project](#deploying-the-project)
    - [Setup and Prerequisites](#setup-and-prerequisites)
    - [Configuring NGINX](#configuring-nginx)
    - [Spinning Up the Project's in Docker Container](#spinning-up-the-projects-docker-container)
    - [Important Notice](#important-notice)


## Project overview

###### MAIN PURPOSE
This is a website of a professional photographer that features the photographer's galleries, and allows for the visitors to create appointments using interactive calendar. 

Visitors can register to access their personal page to facilitate booking of appointments, browse their own galleries, and download archives of their hi-res photographs after photography sessions.

###### USER-CENTRIC FUNCTIONALITY
The site uses Django-native password authentication system; it has been improved in a sense that it now sends additional email with a confirmation link to confirm the initial user registration. Users can also reset their passwords, and remove their accounts.

###### STYLING
The site features adaptive styling implemented with the use of SCSS and media queries, adapting the layout for mobile, large mobile, tablet and desktop screens. The design of the site is a pixel-perfect replica of a Figma mockup (I created it myself and I am by no means a designer, so it probably needs improvement).

###### RESPONSIVE IMAGES AND LAZY LOADING
Another feature is the use of HTML's responsive images (picture element), and lazy loading of those responsive images implemented using Intersection Observer API, with the aim to reduce the amount of traffic used during the loading process.

###### STORING DATA
Information about users, images and appointments is stored in a MariaDB relational database that runs on an instance of AWS EC2 machine in the cloud. The images themselves are stored on an AWS S3 bucket, the archived galleries of hi-res user photos are also stored in S3 bucket. The images are distributed through AWS Cloudfront, which allows for great loading speeds and accessibility from various locations. The images are displayed using signed links, which expire after a limited period of time. This will prevent unauthorized distribution of images via sharing the links. Signed links are probably something of an overkill for this use case; they were implemented as an exercise.

###### PROCESSING IMAGES WITH PIL
Before the images are uploaded to the cloud S3 bucket, they are processed and several images optimized to various sizes are generated using Python's PIL library, the app also generates a very lightweight placeholder image for lazy loading using Intersection Observer. When a gallery is displayed, a respective optimized file is loaded depending on the screen size. Original hi-res images can be downloaded by respective authorized user bundled in an archive.


## Deploying the project
###### The following instructions mirror my setup and will work. Needless to say, this project may be deployed using various other approaches too.


###### SETUP AND PREREQUISITES
For this specific setup you will need a Linux VPS (e.g. AWS EC2) host running Docker, NGINX and MariaDB. You will also need to configure AWS keys for Django, S3, Cloudfront, Simple Email Service (SES), and configure MariaDB accordingly, indicating the credentials in .env file in the project folder. Sample .env.example file is included just as a reference. I recommend associating your VPS with a domain name by pointing the domain's DNS records to VPS's IP address (I myself use AWS Route 53 for hosting my domain).

###### CONFIGURING NGINX
You will need to to configure a NGINX server block to correctly serve your project.  This is an example of the server block I use specifically with my setup.

```nginx
server {
    server_name mariarotari.com www.mariarotari.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/mariarotari.com/static/;
    }

    location /media/ {
        alias /var/www/mariarotari.com/media/;
    }

    access_log /var/log/nginx/mariarotari.access.log;
    error_log /var/log/nginx/mariarotari.error.log;

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/mariarotari.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/mariarotari.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.mariarotari.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = mariarotari.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name mariarotari.com www.mariarotari.com;
    return 404; # managed by Certbot
}
```

A good idea would be to use certbot for nginx to setup SSL certificates. The above block shows the configuration after the certification has been performed.

###### SPINNING UP THE PROJECT'S DOCKER CONTAINER
Copy the project directory to your VPS and spin up the app's container using docker-compose.

AFTER THAT, THE PROJECT SHOULD BE UP AND RUNNING. YOU WILL PROBABLY NEED TO CREATE A SUPERUSER.

**!!!** 
###### IMPORTANT NOTICE
**!!!** 
Please note that this is the initial version of the README.md; I will make it more detailed in the future, possibly includign the detailed instructions for setting up various AWS services used by this project, and, generally, optimizing this documentation.

I would greatly appreciate any feedback on my project.
You can reach me at andrei@arotari.com.
