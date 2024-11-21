# DTL: An ontology for modeling digital twin’s life cycle

We offer DTL(Digital twin lifecycle ontology) as a possible way to model digital twin’s life cycle in the .owl file. Also, we create a sample API(main.py) and one example(example.py) for testing

It is a very simple API that uses GraphDB to provide CRUD in a rather simple way.

We offer an asynchronous way to run the application.


## The stack

These are the components of our API:

* Application Type:         Python-Web Application
* Web framework:
  - async: https://fastapi.tiangolo.com/[FastAPI] (Micro-Webframework)
* Database:                 GraphDB

## Run locally

python main.py

## Using the example

python example.py

## All Configuration Options

Here are all environment variables that can be used to configure the application.


Environment Variable Name

* GRAPHDB_URL = "http://localhost:7200"

* REPOSITORY_ID = "dt-lifecycle"

* BASE_URI = "http://www.example.org/dtlifecycle#"

## Notice

Remember to create the repository in GraphDB and run it before API.

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Kryst4lskyxx/DTL-An-ontology-for-modeling-digital-twin-s-life-cycle">DTL: An ontology for modeling digital twin’s life cycle</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/Kryst4lskyxx">Ye Yuan</a> is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a></p>

