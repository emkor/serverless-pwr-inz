import json

file_name = "/home/mkorzeni/projects/serverless-pwr-inz/api/results_lambda_32u_128r.json"

with open(file_name) as input_file:
    results_list = json.load(input_file)

print("results for: {}".format(file_name))
for result in results_list:
    print("{};{};{}".format(result.get("call_id"), result.get("url"), result.get("took")))
