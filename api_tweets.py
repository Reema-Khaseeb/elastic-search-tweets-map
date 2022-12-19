from http import HTTPStatus
# import pickle
from elasticsearch import Elasticsearch
import numpy as np
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pprint
from src.data_handler import Query
# from .elasticsearch_tweets_query import query_search_scored


templates = Jinja2Templates(directory="templates")

es = Elasticsearch('http://localhost:9200')

def query_search_scored(txt, date_gte, date_lse, coordinates):
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


# Define application
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/render_template')
def render_template(request: Request):
    return templates.TemplateResponse("map.html", {
    "request": request,
    })


# Check the connection is OK by initial path
@app.get("/")
def _health_check():
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response


@app.get("/get_form_input")
def _endpoint(request: Request):
    params =  request.query_params.items()
    params = dict(params)

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

    # query_search_scored(txt, date_gte, date_lse, coordinates)
    es_query = query_search_scored(input_text, start_date, end_date, coordinates)
    score_source = [
        (
            hit["_source"]['coordinates'][0],
            hit["_source"]['coordinates'][1],
            hit['_score']) for hit in es_query['hits']['hits']
            ]

    return {
        'score_source': score_source
        }