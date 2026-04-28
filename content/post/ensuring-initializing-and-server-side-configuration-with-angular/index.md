---
title: "Ensuring Initializing and Server Side Configuration with Angular 4+"
date: 2017-05-31T19:03:59+0000
lastmod: 2017-05-31T19:07:46+0000
slug: "ensuring-initializing-and-server-side-configuration-with-angular"
feature_image: "/images/2017/05/ng.jpg"
aliases:
  - /ensuring-initializing-and-server-side-configuration-with-angular/
---

## Introduction

During the build of the [Blockchain Proof of Concept Framework](https://azure.microsoft.com/en-us/blog/azure-introduces-a-new-blockchain-proof-of-concept-framework-for-developers/) we determined that for greatest configurability and simplistic deployment we needed to have some configuration settings provided by a simple REST service. The website itself for the client is an Angular 4 application and can be served using a static web server such as [nginx](https://nginx.org/) or even an Express site. We ended up creating two approaches and I'm sharing a simple PoC here and on GitHub.

Within Angular there is the `environment` support, which provies basic runtime configuration for the Angular app in static `json` files. But, we didn't want to use this as it complicates build and deployment especially if this is to be used by folks looking for simplicity and not wanting to dive into Angular specific code.

## Angular Startup

For this approach we took advantage of `AppSettings` in Azure WebApps - which show up as environment variables with an `APPSETTING_` prefix. The server has the responsibility to emit a JSON payload that the Angular client can use to prefix any further API calls. Courtesy of this StackOverflow post: [How to call an rest api while bootstrapping angular 2 app](http://stackoverflow.com/questions/41619443/how-to-call-an-rest-api-while-bootstrapping-angular-2-app).

### Angular provider

The key settings in `app.module.ts` is the experimental `APP_INITIALIZER` shown below and the startup service factory.

```
export function startupServiceFactory(startupService: StartupService): Function {
  return () => startupService.load();
}

...

  providers: [
    HttpModule,
    StartupService,
    Title,
    {
      provide: APP_INITIALIZER,
      useFactory: startupServiceFactory,
      deps: [StartupService],
      multi: true
    }

```

### Startup Service

The startup service also uses `load` to ensure that any state is initialized at startup:

```
export class StartupService {

    private _startupData: any;
    // data;

    constructor(private http: Http) { }

    // This is the method you want to call at bootstrap
    // Important: It should return a Promise
    load(): Promise<any> {

        this._startupData = null;

        return this.http
            .get('/config')
            .map((res: Response) => res.json())
            .toPromise()
            .then((data: any) => this._startupData = data)
            .catch((err: any) => Promise.resolve());
    }

    get startupData(): any {
        return this._startupData;
    }

    get gatewayApiHost(): string {
        let rv = this.startupData["APPSETTING_URL"]
            || environment.gatewayApiHost || 'http://localhost:3030';
        console.log('gatewayHost: %s', rv);
        return rv;
    }

    get anotherWay(): string {
        return this.startupData["APPSETTING_URL"];
    }

```

### App Components

Any application component that requires the startup data needs to inject it within the constructor and then within `ngInit` read the properties as follows:

```
export class AppComponent implements OnInit {

    constructor(private startup: StartupService, private router: Router, private titleService: Title) { }

    title = "My site";
    //startupData: string;

    ngOnInit() {

        // If there is no startup data received (maybe an error!)
        // navigate to error route
        if (!this.startup.startupData) {
            console.log('startup data does not exists');
            this.router.navigate(['error'], { replaceUrl: true });
        }
        else {
            console.log('startup data exists.');
        }

        this.setTitle("Your Site..");
        //this.startupData = JSON.stringify(this.startup.startupData);
    
    }

```

## nginx approach

In this example, the server is nginx and a shell script is used to start nginx, but also create a static `config.json` file that is read by the service in the Angular app. Courtesy of [Jurgen Van de Moere](https://www.jvandemo.com/how-to-configure-your-angularjs-application-using-environment-variables/)

### Source Code Example

The source for the example Angular app and a Dockerfile, along with the startup script is [here](https://github.com/cicorias/nginit-nginx).

The startup script is below.

```
#!/usr/bin/env sh

echo "
{
  \"GatewayApiUrl\" : \"${GATEWAY_API_URL}\",
  \"ActiveDirectoryTenant\" : \"${ACTIVE_DIRECTORY_TENANT}\",
  \"ActiveDirectoryClientId\" : \"${ACTIVE_DIRECTORY_CLIENTID}\"
}
" > /usr/share/nginx/html/config.json

nginx -g 'daemon off;'

```

## static "bare node js" approach

This is a non-dependancy static server that offers no caching, etc. it provides several mime types, in addition a single /config endpoint that will run a filter on the environment variables serverside. The intent is that settings prefixed with APPSETTING\_ are bundled into a flat json object. This allows use in Azure WebApps and app settings which are configurage at deployment and at anypoint after deployment. The core of this was taken from this [gist](https://gist.github.com/amejiarosario/53afae82e18db30dadc9bc39035778e5).

### Source Code Example

The source for the example Angular app and the static web server are [here](https://github.com/cicorias/bare-node).

The full source to the pure Node JS static web server is below:

```
'use strict';
/* This is a non-dependancy static server that offers no caching, etc.
 * it provides several mime types, in addition a single /config endpoint
 * that will run a filter on the environment variables serverside.
 * The intent is that settings prefixed with APPSETTING_ are bundled into a flat
 * json object. This allows use in Azure WebApps and app settings which are 
 * configurage at deployment and at anypoint after deployment.
 * The core of this was taken from this gist: //https://gist.github.com/amejiarosario/53afae82e18db30dadc9bc39035778e5
 *
 * 
 * Shawn Cicoria May 23, 2017
 */

const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const util = require('util');

const port = process.env.port || 3000;

http.createServer(function (req, res) {
  console.log(`${req.method} ${req.url}`);

  // parse URL
  const parsedUrl = url.parse(req.url, true);

  // extract URL path
  let pathname = `.${parsedUrl.pathname}`;
  console.log(pathname)

  if (pathname == './') {
    pathname = 'index.html';
  }

  if (req.method === 'GET' && parsedUrl.path === '/config') {
    //run the config API
    configApi(res);
  }
  else {
    // based on the URL path, extract the file extention. e.g. .js, .doc, ...
    const ext = path.parse(pathname).ext;

    // maps file extention to MIME typere
    const map = {
      '.ico': 'image/x-icon',
      '.html': 'text/html',
      '.js': 'text/javascript',
      '.json': 'application/json',
      '.css': 'text/css',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.wav': 'audio/wav',
      '.mp3': 'audio/mpeg',
      '.svg': 'image/svg+xml',
      '.pdf': 'application/pdf',
      '.doc': 'application/msword'
    };

    fs.exists(pathname, function (exist) {
      if (!exist) {
        // if the file is not found, return 404
        res.statusCode = 404;
        res.end(`File ${pathname} not found!`);
        return;
      }

      // if is a directory search for index file matching the extention
      if (fs.statSync(pathname).isDirectory()) pathname += '/index' + ext;

      // read file from file system
      fs.readFile(pathname, function (err, data) {
        if (err) {
          res.statusCode = 500;
          res.end(`Error getting the file: ${err}.`);
        } else {
          // if the file is found, set Content-type and send data
          res.setHeader('Content-type', map[ext] || 'text/plain');
          res.end(data);
        }
      });
    });
  }

}).listen(parseInt(port));

console.log(`Server listening on port ${port}`);

const appSettings = {};
Object.keys(process.env).map(function (key, index, array) {
  if (key.startsWith('APPSETTING_'))
    appSettings[key] = process.env[key];
});

function configApi(res) {
  // if the file is found, set Content-type and send data
  res.setHeader('Content-type', 'application/json');
  return res.end(JSON.stringify(appSettings));
}

```
