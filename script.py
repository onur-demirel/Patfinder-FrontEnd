import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
import requests
from sentence_transformers import SentenceTransformer
app = Flask(__name__)
CORS(app)

ENDPOINT = "https://localhost:9200"
USERNAME="elastic"
PASSWORD="lQhRXC8Spgb7S189xFIi"

indexname = "patentsberta"
model = SentenceTransformer('AI-Growth-Lab/PatentSBERTa')

client = Elasticsearch(
    hosts=[ENDPOINT],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

def searchInAbstract(userInput):
    searchField = 'abstract_vector'

    response = client.search(
        index=indexname,
        size=100,
        knn={
            "field": searchField,
            "query_vector": model.encode(userInput),
            "k": 100,
            "num_candidates": 100
        }
    )

    results = pretty_response(response)
    return results

def pretty_response(response):
    my_list = list()
    count = 0
    if len(response['hits']['hits']) == 0:
        print('Your search returned no results.')
    else:
        for hit in response['hits']['hits']:
            id = hit['_source']['Publication Number']
            title = hit['_source']['Title']
            abstract = hit['_source']['Abstract']
            description = hit['_source']['Description']

            #make the every first letter of the title capital
            title = title.title()

            #remove any "_x000D_ " from the text
            abstract = abstract.replace("_x000D_", "")
            description = description.replace("_x000D_", "")

             #remove any number in format "[0001]" or "[0002]" from the text
            abstract = re.sub(r'\[\d+\]', '', abstract)
            description = re.sub(r'\[\d+\]', '', description)

            #remove any number in format "(2)" or "(09)" from the text
            abstract = re.sub(r'\(\s*\d+\s*[a-z,]*\s*\)', '', abstract)
            description = re.sub(r'\(\s*\d+\s*[a-z,]*\s*\)', '', description)
            
            my_list.append({'index':count ,'patent_id': id, 'title': title, 'abstract': abstract, 'description': description})
            count = count+1

    print(len(my_list))
    return my_list

@app.route('/submit-message',methods=['POST'])

def handle_message():
    data = request.json
    message = data['message']
    print(f'Printing from python : {message}')
    resultList = searchInAbstract(message)

    #save the jsonify(resultList) to a file
    # with open('result.json', 'w') as f:
    #     f.write(jsonify(resultList))

    # with open('result.txt', 'w') as f:
    #     f.write(resultList)

    #serialize the result to a file
    #with open('results on anydesk.txt', 'w',encoding="utf-8") as f:
    #    f.write(str(resultList))


    return jsonify(resultList)


@app.route('/search-similiar',methods=['POST'])
def search_similiar():
    data = request.json
    title = data['title']
    print(f'Search similiar : {title}')
    resultList = findSimiliar(title)
    return jsonify(resultList)



def parseSimiliar(response):
    my_list = list()
    count = 0
    if len(response['hits']['hits']) == 0:
        print('Your search returned no results.')
    else:
        for hit in response['hits']['hits']:
            id = hit['_source']['Publication Number']
            title = hit['_source']['Title']
            score = hit['_score']

            #make the every first letter of the title capital
            title = title.title()

            my_list.append({'index':count ,'patent_id': id, 'title': title, 'score': score})
            count = count+1

    return my_list

def findSimiliar(userInput):
    searchField = 'abstract_vector'

    response = client.search(
        index=indexname,
        size=100,
        knn={
            "field": searchField,
            "query_vector": model.encode(userInput),
            # "query_vector" : model.encode(userInput),
            "k": 100,
            "num_candidates": 100
        }
    )

    results = parseSimiliar(response)
    return results

@app.route("/summarize", methods=['POST'])

def summarize():
    content = request.json
    messages = content["messages"]
    response = call_mistral_api(messages)
    return jsonify(response)


def call_mistral_api(messages, temperature=0.7, max_tokens=-1, stream=False):
    #url = "http://localhost:1234/v1/"  # The API endpoint,
    url = "http://localhost:1234/v1/chat/completions"  # The API endpoint

    headers = {"Content-Type": "application/json"}

    # Construct the data payload
    data = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }

    # Make the POST request

    print(data)
    response = requests.post(url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        # Handle errors (you could expand this with more detailed error handling)
        return {"error": "Request failed with status code {}".format(response.status_code)}
    
if __name__ == '__main__':
    app.run(debug=True)


