from http import HTTPStatus
# import pickle
from elasticsearch import Elasticsearch
import numpy as np
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pprint
# from .src.data_handler import Query
# from elasticsearch_tweets_query import query_search_scored


# Create Jinja2 template engine to render HTML templates
templates = Jinja2Templates(directory="templates")

# Create Elasticsearch client object
es = Elasticsearch('http://localhost:9200')

def query_search_scored(txt, date_gte, date_lse, coordinates):
    """
    Query Elasticsearch for documents matching the input text and within the specified date range and coordinates.
    Returns the search results.
    """
    return es.search(
    index = 'tweets3',
    body={"query": {
    "bool": {
      "must": [
          {
              "match": {
                  "text": txt
              }
          },
          {
              "range": {
                  "created_at": {
                      "gte": date_gte,
                      "lte": date_lse,
                  }
              }
          },
          {
              "geo_bounding_box": {
                  "coordinates": coordinates
              }
          }
      ]
    }
  }}
    )


# Define application creating FastAPI object
app = FastAPI()

# Serve static files (e.g. HTML, CSS, JavaScript) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define endpoint that renders the HTML template "map.html"
@app.get('/render_template')
def render_template(request: Request):
    """
    Render the HTML template "map.html"
    """
    return templates.TemplateResponse("map.html", {
    "request": request,
    })

# Define health check endpoint
@app.get("/")
def _health_check():
    """
    Check that the server is running and responding to requests.
    """
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }
    return response

# Define endpoint that processes form input and returns search results from Elasticsearch
@app.get("/get_form_input")
def _endpoint(request: Request):  # def _endpoint(request: Query):
    """
    Process form input and return search results from Elasticsearch.

    Parameters:
    - request (FastAPI Request object): an object representing the incoming HTTP request, containing the query parameters
    
    Returns:
    - A dictionary with a single key, 'score_source', whose value is a list of tuples containing coordinates and scores.
    """
    # Extract form input as a dictionary
    params =  request.query_params.items()
    params = dict(params)
    # Extract form values
    input_text = params['text_form']
    start_date = params['start_date']
    end_date = params['end_date']
    coor1 = float(params['coor1'])
    coor2 = float(params['coor2'])
    coor3 = float(params['coor3'])
    coor4 = float(params['coor4'])

    coordinates= {
                    "top_left": [coor1,coor2],
                    "bottom_right": [coor3,coor4]
                    }

    es_query = query_search_scored(input_text, start_date, end_date, coordinates)
    score_source = [
        (
            hit["_source"]['coordinates'][1],
            hit["_source"]['coordinates'][0],
            hit['_score']) for hit in es_query['hits']['hits']
            ]

    return {
        'score_source': score_source,
        }