#!/bin/python3
import requests
import json
import os
import sys


def requests_text_in_yagpt(text):
    return json.dumps({
             "modelUri": "gpt://FOLDER_ID/yandexgpt-lite",
             "completionOptions": {
               "stream": False,
               "temperature": 0.1,
               "maxTokens": "1000"
             },
             "messages": [
               {
                 "role": "system",
                 "text": text
               }
             ]
           })


def gpt(auth_headers):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    resp = requests.post(url, headers=auth_headers, data=requests_text_in_yagpt(" ".join(sys.argv[1:])))

    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {resp.status_code}, {resp.text}
            )
        )
    return resp.json()["result"]["alternatives"]


if __name__ == "__main__":
    print(" ".join(sys.argv[1:]))
    print("==========")
    with open(f'iam_token.password', 'r', encoding='utf-8') as f:
        iam_token = f.read().replace('\n', '')
    headers = {'Authorization': f'Bearer {iam_token}'}
    for i in gpt(headers):
        print(i['message']['text'])
