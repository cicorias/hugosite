---
title: "Forcing TLS (HTTPS) on Azure Web Apps for Linux with nginx"
date: 2017-08-15T12:51:00+0000
lastmod: 2017-08-15T13:16:35+0000
slug: "forcing-tls-https-on-azure-web-apps-for-linux"
feature_image: "https://www.cicoria.com/content/images/2017/08/Untitled.jpg"
aliases:
  - /forcing-tls-https-on-azure-web-apps-for-linux/
---

For many websites today TLS (fka SSL) is preferred. For [Azure Web Apps](https://docs.microsoft.com/en-us/azure/app-service-web/), all sites automatically listen on both port 80 and 443 - for HTTP and HTTPS respectively.

If you want to force the site to be only HTTPS you might think that you can just detect the `$scheme` and if `HTTP` redirect to `HTTPS`. Well, in [Azure WebApps for Linux](https://docs.microsoft.com/en-us/azure/app-service-web/app-service-linux-intro), that won't work.

The reason it does not work is [Azure Web Apps](https://docs.microsoft.com/en-us/azure/app-service-web/) provides a front end proxy, either Application Request Routing (ARR) or [nginx](http://nginx.org/), that terminates TLS and the request from that front-end proxy to your app is always HTTP (non-TLS). I'm not going to go into reasons, nor any of the arguments for or against. That's how it works.

The hint that Azure Web Apps provides is the presence or absence of an additional HTTP header - `x--arr-ssl`. If this is present, the value will be the certificate properties, such as `2048|256|C=US, S=Washington, L=Redmond, O=Microsoft Corporation, OU=Microsoft IT, CN=Microsoft IT SSL SHA2|CN=*.azurewebsites.net`.

For a Wordpress HOWTO take a look here: [HTTP to HTTPS redirect for WordPress on Azure Web App on Linux](https://blogs.msdn.microsoft.com/azureossds/2017/08/04/http-to-https-redirect-for-wordpress-on-azure-web-app-on-linux/)

For [nginx](http://nginx.org/) we just need to understand that nginx will make all dashes in custom headers an underscore `_`. So, the `x-arr-ssl` becomes `$http_x_arr_ssl` for any rules or usage in the nginx configuration.

The basic configuration that can be used is:

```
server {
  listen 80 default_server;
  listen [::]:80 default_server;
  index index.html;
  root /usr/share/nginx/html;
  sendfile  off;
  error_log stderr debug;

  if ($http_x_arr_ssl = "") {
        return 301 https://$host$request_uri;
  }

  location / {
    try_files $uri$args $uri$args/ /index.html;
  }

  location = /index.html {
    if ($http_x_debug) {
      add_header X-debug-request "$request";
      add_header X-debug-host "$host";
      add_header X-debug-args "$args";
      add_header X-debug-uri "$uri";
      add_header X-debug-301 "https://$host$request_uri";
      add_header X-debug-arr-ssl "$http_x_arr_ssl";
      add_header X-debug-port "$remote_port";
      add_header X-debug-scheme "$scheme";      
    }
    # no try_files here
  }
}

```
