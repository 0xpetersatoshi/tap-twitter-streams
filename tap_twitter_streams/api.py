import datetime
import json
import os

import requests
import singer


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    return response.json()


def delete_all_rules(headers, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )


def set_rules(headers, rules):
    # You can adjust the rules if needed

    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )


def get_stream(headers, singer_stream, singer_schema):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # return None
    singer.write_schema(singer_stream, singer_schema, "tweet_id")
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)

            record = {
                "tweet_id": json_response["data"]["id"],
                "timestamp": datetime.datetime.now().isoformat(),
                "text": json_response["data"]["text"],
                "tag_id": json_response["matching_rules"][0]["id"],
                "tag_value": json_response["matching_rules"][0]["tag"]
            }

            singer.write_record(singer_stream, record)


def stream_tweets(stream_id, schema, rules):
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules_to_delete = get_rules(headers)
    delete_all_rules(headers, rules_to_delete)
    set_rules(headers, rules)
    get_stream(headers, stream_id, schema)
