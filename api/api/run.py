import json
from random import randint
import multiprocessing

import requests
from typing import Any, Dict, List, Callable

from commons.model import Model, City
from api.places_import import import_from_file

CITIES_FILE = "/home/mkorzeni/projects/serverless-pwr-inz/api/ServerlessPwrInz-Cities.csv"
RESULTS_FILE = "/home/mkorzeni/projects/serverless-pwr-inz/api/results.json"
CALL_COUNT_PER_API = 128
CONCURRENCY = 32
URLs = ["http://localhost:8080/uber",
        "http://localhost:8080/instagram",
        "http://localhost:8080/weather",
        "http://localhost:8080/skyscanner",
        ]

CITIES = import_from_file(csv_file_name=CITIES_FILE)


def random_index(length):
    # type: (int) -> int
    return randint(0, length - 1)


class TestCall(Model):
    def __init__(self, call_id, url, payload):
        # type: (int, str, Dict[str, Any]) -> None
        self.call_id = call_id
        self.url = url
        self.payload = payload

    def __call__(self, *args, **kwargs):
        # type: () -> ExecutedTestCall
        print("Executing {}...".format(self))
        response = requests.post(url=self.url, json=self.payload)
        result = response.elapsed.total_seconds()
        # sleep(0.1)
        # result = 0.1
        print("Executed {}!".format(self))
        return ExecutedTestCall(call_id=self.call_id, url=self.url, payload=self.payload,
                                took=result, status_code=response.status_code)

    def __str__(self):
        return "<Call #{} to {}".format(self.call_id, self.url)


class ExecutedTestCall(TestCall):
    def __init__(self, call_id, url, payload, took, status_code):
        # type: (int, str, Dict[str, Any, float, int]) -> None
        super(ExecutedTestCall, self).__init__(call_id, url, payload)
        self.took = took
        self.status_code = status_code

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Call is already executed!")

    def __str__(self):
        return "<Executed call #{} to {} that took {} ended with {}".format(self.call_id, self.url, self.took,
                                                                            self.status_code)


def build_calls(urls, cities, api_call_count):
    # type: (List[str], List[City], int, int) -> List[TestCall]
    calls = []
    for url in urls:
        api_call = 0
        while api_call < api_call_count:
            city_serialized = cities[api_call % len(cities)].to_serializable()
            if "skyscanner" in url:
                city_b_serialized = cities[(api_call * 2) % len(cities)].to_serializable()
                calls.append(TestCall(call_id=len(calls), url=url,
                                      payload={"city_a": city_serialized, "city_b": city_b_serialized}))
            else:
                calls.append(TestCall(call_id=len(calls), url=url, payload=city_serialized))
            api_call += 1
    return calls


def execute_call(call):
    # type: (Callable[..., ExecutedTestCall]) -> ExecutedTestCall
    return call()


def execute_calls(calls, concurrency):
    # type: (List[TestCall], int) -> List[ExecutedTestCall]
    pool = multiprocessing.Pool(concurrency)
    return pool.map(execute_call, calls)


def main():
    print("Starting script...")
    generated_calls = build_calls(urls=URLs, cities=CITIES, api_call_count=CALL_COUNT_PER_API)
    print("Generated {} calls: {}".format(len(generated_calls), generated_calls))
    results = execute_calls(generated_calls, concurrency=CONCURRENCY)
    print(results)
    with open(RESULTS_FILE, "w") as results_file:
        json.dump([r.to_serializable() for r in results], results_file)
    print("Done storing results in {}!".format(RESULTS_FILE))


if __name__ == "__main__":
    main()
