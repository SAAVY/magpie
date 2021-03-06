[![Build Status](https://travis-ci.org/SAAVY/magpie.svg?branch=master)](https://travis-ci.org/SAAVY/magpie)
[![codecov.io](https://codecov.io/github/SAAVY/magpie/coverage.svg?branch=master)](https://codecov.io/github/SAAVY/magpie?branch=master)

# Project Magpie

Magpie is an API aimed at displaying embedded content without the developer having to parse the website.
Magpie allows the developer to have full customization over how they want to display the metadata, and also choose to cache any metadata via redis.

This is currently an ongoing project and is still at it's early stages of development.
Please subscribe to updates about this project at http://projectmagpie.github.io

### <a name="config"></a>Supported Websites

Magpie supports retrieving metadata from all websites that provide meta tags. Magpie also supports the following websites for retrieving metadata:  

* Youtube
* Wikipedia
* Public Google Drive links (Or documents available to anyone with a share link)
* Public Dropbox links (Or documents available to anyone with a share link)

## <a name="setup"></a>Getting Started

### <a name="setup"></a>Local setup
Since Magpie is a Python based application, please make sure you have `Python 2.7.x` installed before proceeding further.  

  1. Clone the repository  
        ``` git clone https://github.com/SAAVY/magpie.git ```
  2. Ensure you have `redis-server` installed on your local environment see [http://redis.io/topics/quickstart](http://redis.io/topics/quickstart)
  3. Make a Python virtual environment and activate it. For instructions on virtual environments for Python, refer to the
  [virtualenv](http://virtualenv.readthedocs.org/en/latest/installation.html) documentation  
  4. Once the virtual environment has been activated, cd into the magpie directory and run ```make install```  
  This will install all the library requirements for Magpie. A list of all libraries used in this project can be found in requirements.txt    

Magpie is now installed on your computer! Note that Magpie runs on Flask.  

### <a name="run_app"></a>Running the Application
To run the application locally, simply run `make dev` from the root of the project directory. Magpie will then launch on the port set in `config/config.py`
on your localhost.

#<a name="setup"></a>Deployment
To support multiple configuration servers, Magpie recommends using either gunicorn or wsgi.

## <a name="nginx_setup"></a>Database Setup
Currently, magpie supports Redis as the cache for saving metadata as well as rate limiting features.
If you are running your server on aws you can do the following to install `redis-server` on your machine.
See [http://redis.io/topics/quickstart](http://redis.io/topics/quickstart) for more information.

```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```

To run redis on the default host & port `localhost:6379`, just run the command `redis-server`

## <a name="nginx_setup"></a>Nginx Setup
If you are running an nginx webserver, Magpie recommends using [gunicorn](http://gunicorn.org/) to serve the flask server.

Steps to installing gunicorn:

install and start nginx:

``` sudo apt-get install nginx ```

``` sudo /etc/init.d/nginx start ```

``` sudo git clone https://github.com/SAAVY/magpie.git ~/magpie```

``` cd ~/magpie```

rename [`deploy/nginx/magpie_api.ex_nginx.conf`](deploy/nginx/magpie_api.ex_nginx.conf) to `deploy/nginx/magpie_api.conf` and edit the configuration fields. Copy the conf to sites-available

edit the configuration values in the configuration file.

``` sudo cp deploy/nginx/magpie_api.conf /etc/nginx/sites-available/magpie_api.conf```

move config to sites enabled to enable conf

``` sudo cp /etc/nginx/sites-available/magpie_api.conf /etc/nginx/sites-enabled/magpie_api.conf```

``` virtualenv -p /usr/bin/python2.7 venv```

### <a name="nginx_setup"></a>Running server using Gunicorn
``` . venv/bin/activate ```

command to run server using gunicorn:

It is recommended to set the number of threads to be `2*<<number of cores on the server>> -1`

Log directory should be where you would like to place the flask log files in

``` sudo gunicorn -w <<# of threads>> -b 127.0.0.1:8000 'client.api:start("<<log directory>>")'```

Your server should now be accessible!


## <a name="apache_setup"></a>Recommended Apache Setup
If you are running an apache webserver, Magpie recommends using [mod_wsgi](http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/) to serve the flask server.

Steps to installing apache-wsgi & running wsgi application:
``` apt-get install libapache2-mod-wsgi ```

enable wsgi on apache
``` a2enmod wsgi ```

``` git clone https://github.com/SAAVY/magpie.git /var/www/magpie ```

``` cd /var/www/magpie```

``` virtualenv -p /usr/bin/python2.7 venv ```

rename [`deploy/apache/magpie_api.ex_apache.conf`](deploy/apache/magpie_api.ex_apache.conf) to `deploy/apache/magpie_api.conf` and edit the configuration fields. Copy the conf to sites-available

``` sudo cp deploy/apache/magpie_api.conf /etc/apache2/sites-available/magpie_api.conf ```

Enable configuration file:

``` sudo a2ensite magpie_api.conf ```

``` sudo service apache2 reload ```


copy the wsgi file to root directory, edit secret key in file
``` sudo cp /var/www/magpie/deploy/apache/magpie.wsgi /var/www/magpie/magpie.wsgi ```

``` sudo service apache2 reload ```

Your server should be accessible!

#<a name="config"></a>Custom Configuration
In `config/config.py` there are multiple custom configuration variables to configure your api to your liking.

The following variables are currently supported:

| Variable  | Description  |
|---|---|
| `IS_DEV`           | Debug mode, default is `False`
| `DEV_PORT`         | The port for running flask app locally, default is `5000`
| `PROFILE_METHODS`  | Profile methods speed and output to terminal (intended only on dev), default is `False` 
| `CACHE_DATA`       | Whether to cache data to redis machine. Note you will still need to have redis on for rate limiting, default is `False`
| `ImageAttrs.MIN_IMAGE_HEIGHT`   | The filter for checking for minimum image dimensions height attribute, default is `50`
| `ImageAttrs.MIN_IMAGE_WIDTH`    | The filter for checking for minimum image dimensions width attribute, default is `50`
| `ImageAttrs.MAX_RETURN_IMAGES`  | The filter max number of images returned, default is `10`
| `REDIS_HOST`       | Where the redis-server host is, default is `127.0.0.1`
| `REDIS_PORT`       | Where the redis-server port is, default is `6379`
| `GLOBAL_RATE_LIMIT`| Global limit for rate limiter; see http://flask-limiter.readthedocs.org/en/stable/#ratelimit-string, default is `["100/minute", "5/second"]`
| `REQUEST_TIMEOUT` | The max request time for hitting a url in seconds, takes in a tuple (connect timeout, read timeout). The default is `(3.05, 10)`


#<a name="params"></a>Request and Response parameters

## <a name="request"></a>Request Parameters
There are currently two request parameters supported by Magpie  

| Field  | Description  |
|---|---|
| `src`  |The url that needs to be scraped for Metadata. A local request to magpie would be as follows:`http://localhost:5000/website?src=http://www.youtube.com/watch?v=dQw4w9WgXcQ`. Multiple src parameters may also be passed to get multiple responses, such as `http://localhost:5000/website?src=https://www.youtube.com/watch?v=Vhh_GeBPOhs&src=https://en.wikipedia.org/wiki/Toronto`|
| `desc_cap`  | Allows for customization over the length of the `description` field. Default cap is set to 200 characters.   |


## <a name="examples"></a>Response Examples
A sample of the various types of JSON responses are shown below.

### <a name="eg_generic"></a>Generic Request
```json
{
    "status": 200,
    "request_url": "https://medium.com/@gernot/why-tim-cook-is-so-furious-be24163bdfa#.bxs2jw9q8",
    "error_message": null,
    "data": {
        "files": null,
        "provider_url": "https://medium.com/",
        "description": "You might have read the Apple CEO\u2019s open response to the US government earlier today. They are demanding access to an iP\u2026",
        "title": "Why Tim Cook is so furious",
        "url": "https://medium.com/@gernot/why-tim-cook-is-so-furious-be24163bdfa",
        "media": null,
        "favicon": "https://cdn-static-1.medium.com/_/fp/icons/favicon-new.TAS6uQ-Y7kcKgi0xjcYHXw.ico",
        "images": {
            "count": 1,
            "data": [
                {
                    "url": "https://cdn-images-1.medium.com/max/800/1*mWkIN-9FvzyvCqqbpW5Mdw.jpeg"
                }
            ]
        },
        "api_query_url": null
    }
}
```
### <a name="eg_multiple"></a>Multiple Requests

```json
{
    "response_count": 2,
    "responses": [
        {
            "status": 200,
            "request_url": "https://www.youtube.com/watch?v=Vhh_GeBPOhs",
            "error_message": null,
            "data": {
                "files": null,
                "provider_url": "http://www.youtube.com/",
                "description": "Uno de los peces gordos de Microsoft, en lo que parece una presentación de esta compañía, no para de hablar de los \"developers\". VISITA: www.MRWUEB.es.kz www...",
                "title": "Steve Ballmer: Developers",
                "url": "https://www.youtube.com/watch?v=Vhh_GeBPOhs",
                "media": {
                    "count": 1,
                    "data": [
                        {
                            "url": "https://www.youtube.com/embed/Vhh_GeBPOhs?feature=oembed",
                            "type": "video",
                            "iframe": "<iframe width=\"459\" height=\"344\" src=\"https://www.youtube.com/embed/Vhh_GeBPOhs?feature=oembed\" frameborder=\"0\" allowfullscreen></iframe>"
                        }
                    ]
                },
                "favicon": "https://s.ytimg.com/yts/img/favicon-vflz7uhzw.ico",
                "images": {
                    "count": 1,
                    "data": [
                        {
                            "url": "https://i.ytimg.com/vi/Vhh_GeBPOhs/hqdefault.jpg"
                        }
                    ]
                },
                "api_query_url": "http://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=Vhh_GeBPOhs"
            }
        },
        {
            "status": 200,
            "request_url": "https://en.wikipedia.org/wiki/Toronto",
            "error_message": null,
            "data": {
                "files": null,
                "provider_url": "https://en.wikipedia.org/",
                "description": "Toronto (/təˈrɒntoʊ, -tə/, local /təˈrɒnoʊ, ˈtrɒ-/) is the most populous city in Canada, the provincial capital of Ontario, and the centre of the Greater Toronto Area, the most populous metropolitan a...",
                "title": "Toronto - Wikipedia, the free encyclopedia",
                "url": "https://en.wikipedia.org/wiki/Toronto",
                "media": null,
                "favicon": null,
                "images": {
                    "count": 1,
                    "data": [
                        {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Montage_of_Toronto_7.jpg/42px-Montage_of_Toronto_7.jpg",
                            "width": 42,
                            "height": 50
                        }
                    ]
                },
                "api_query_url": null
            }
        }
    ]
}
```

### <a name="eg_youtube"></a>Youtube
```json
{
    "status": 200,
    "request_url": "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "error_message": null,
    "data": {
        "files": null,
        "provider_url": "http://www.youtube.com/",
        "description": "Music video by Rick Astley performing Never Gonna Give You Up. YouTube view counts pre-VEVO: 2,573,462 (C) 1987 PWL",
        "title": "Rick Astley - Never Gonna Give You Up",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "media": {
            "count": 1,
            "data": [
                {
                    "url": "https://www.youtube.com/embed/dQw4w9WgXcQ?feature=oembed",
                    "type": "video",
                    "iframe": "<iframe width=\"459\" height=\"344\" src=\"https://www.youtube.com/embed/dQw4w9WgXcQ?feature=oembed\" frameborder=\"0\" allowfullscreen></iframe>"
                }
            ]
        },
        "favicon": "https://s.ytimg.com/yts/img/favicon-vflz7uhzw.ico",
        "images": {
            "count": 1,
            "data": [
                {
                    "url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
                }
            ]
        },
        "api_query_url": "http://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
}
```

### <a name="eg_dropbox"></a>Dropbox File
```json
{
    "status": 200,
    "request_url": "https://www.dropbox.com/s/7ih2nl5xpkklgv7/Getting%20Started.pdf?dl=0",
    "error_message": null,
    "data": {
        "files": {
            "count": 1,
            "data": [
                {
                    "url": "https://www.dropbox.com/s/7ih2nl5xpkklgv7/Getting%20Started.pdf?dl=1",
                    "type": null
                }
            ]
        },
        "provider_url": "https://www.dropbox.com/",
        "description": "Shared with Dropbox",
        "title": "Getting Started.pdf",
        "url": "https://www.dropbox.com/s/7ih2nl5xpkklgv7/Getting%20Started.pdf?dl=0",
        "media": null,
        "favicon": "https://cf.dropboxstatic.com/static/images/favicon-vflk5FiAC.ico",
        "images": {
            "count": 1,
            "data": [
                {
                    "url": "https://cf.dropboxstatic.com/static/images/icons128/page_white_acrobat.png"
                }
            ]
        },
        "api_query_url": null
    }
}
```

### <a name="eg_wikipedia"></a>Wikipedia
```json
{
    "status": 200,
    "request_url": "https://en.wikipedia.org/wiki/Magpie",
    "error_message": null,
    "data": {
        "files": null,
        "provider_url": "https://en.wikipedia.org/",
        "description": "Magpies are birds of the Corvidae (crow) family, including the black and white Eurasian magpie, which is considered one of the most intelligent animals in the world, and the only non-mammal species able to recognize itself in a mirror test. In addition to other members of the genus Pica, corvids considered as magpies are in the genera Cissa, Cyanopica and Urocissa.",
        "title": "Magpie - Wikipedia, the free encyclopedia",
        "url": "https://en.wikipedia.org/wiki/Magpie",
        "media": null,
        "favicon": "https://en.wikipedia.org/static/favicon/wikipedia.ico",
        "images": {
            "count": 1,
            "data": [
                {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Magpie_arp.jpg/39px-Magpie_arp.jpg",
                    "width": 39,
                    "height": 50
                }
            ]
        },
        "api_query_url": null
    }
}
```

### <a name="eg_drive"></a>Google Drive
```json
{
    "status": 200,
    "request_url": "https://docs.google.com/document/d/1huD2UvKezXfgczQfY10577d6DK_mWLMXmthQtrr7Y24/edit?usp=sharing",
    "error_message": null,
    "data": {
        "files": {
            "count": 1,
            "data": [
                {
                    "url": "https://docs.google.com/document/d/1huD2UvKezXfgczQfY10577d6DK_mWLMXmthQtrr7Y24/export?format=pdf",
                    "type": "pdf"
                }
            ]
        },
        "provider_url": "https://docs.google.com/",
        "description": "Welcome to Magpie! For more information on the Magpie API visit our github page at https://github.com/SAAVY/magpie. For more information about Magpie the bird (one of the most intelligent birds in the world) google on!",
        "title": "Magpie",
        "url": "https://docs.google.com/document/d/1huD2UvKezXfgczQfY10577d6DK_mWLMXmthQtrr7Y24/edit?usp=sharing",
        "media": null,
        "favicon": "https://ssl.gstatic.com/docs/documents/images/kix-favicon6.ico",
        "images": {
            "count": 1,
            "data": [
                {
                    "url": "https://lh5.googleusercontent.com/0W6aLweiroTtNaVb7tlj68CEyjDmRyKLsk5g05EApRq7eutBVQEsKG9sTX7q9SuGuh71sQ=w1200-h630-p"
                }
            ]
        },
        "api_query_url": null
    }
}
```

## <a name="param_table"></a>Response Parameters Explained

| Field  | Description  |
|---|---|
| `status`  | Returns the response code of the request to the website  |
| `request_url`  | The URL provided when making the request to the Magpie API   |
| `error_message`  | Error messages if any when making the request. Eg: if status is `404`, `error_message` might be `404 Not Found` |
|  `provider_url` | The URL of the domain for the `request_url`  |
| `api_query_url`  | The URL of any request made to a 3rd party API to retrieve information   |
| `data`  | A general field name for the contents of the parent. Eg: `data` of an `image` field may consist of 3 fields: `url`, `width`, and `height`  |
| `images`  | Contains the `count` and a list of image properties if the website has any images in its metadata. `null` if none. |
| `files`  | Contains the `count` and a list of file properties if the website has any downloadable files (eg: dropbox). `null` if none.  |
| `title`  | The title of the website or document (taken from the title meta tag if present, or from `<title>`, or from API sources (eg: google drive and dropbox). `null` if none are found.   |
| `description`  | The description of the website or document (taken from the description meta tag if present, or from API sources (eg: google drive and dropbox). `null` if none are found. |
| `media`  | Contains the properties and embedding code for iframe if any are present, such as in the case for YouTube links. `null` if nothing present.|
| `favicon`  | Contains the URL for the favicon of the website. `null` of nothing could be found.  |
| `response_count`  | Number of responses returned for  multiple URL requests.  |
| `responses`  | List of response objects for multiple URL requests.  |

# <a name="contrib"></a>Contributing

To contribute to our project, see [CONTRIBUTING guidelines](CONTRIBUTING.md).

# <a name="contrib"></a>License

Magpie is licensed under the MIT licensing policy. See [LICENSE.md](LICENSE.md) for more information.
