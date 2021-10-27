import http.client
import json
import argparse

CIRCLECI_API_BASE_URL='https://circleci.com/api/v2'

def find_context(api_token, owner_slug, context_name):
  conn = http.client.HTTPSConnection("circleci.com")

  conn.request("GET", f"/api/v2/context?owner-slug={owner_slug}", headers=CIRCLECI_API_BASE_HEADERS)

  res = conn.getresponse()
  json_response = json.loads(res.read())
  context_dict = json_response['items']
  for context in context_dict:
    if context['name'] == context_name:
      print(f"{context_name} already exists")
      return True
      break
  print(f"{context_name} does not exist")
  return False

def get_context_id(api_token, owner_slug, context_name):
  conn = http.client.HTTPSConnection("circleci.com")

  conn.request("GET", f"/api/v2/context?owner-slug={owner_slug}", headers=CIRCLECI_API_BASE_HEADERS)

  res = conn.getresponse()
  json_response = json.loads(res.read())
  context_dict = json_response['items']
  for context in context_dict:
    if context['name'] == context_name:
      context_id = context["id"]
      print(f"{context_name} = {context_id}")
      return context["id"]
      break
  return None

def set_environment_var_to_context(api_token, owner_slug, context_name, variable_name, variable_value):
  conn = http.client.HTTPSConnection("circleci.com")
  payload = f'{{\"value\":\"{variable_value}\"}}'
  context_id = get_context_id(api_token, owner_slug, context_name)
  conn.request("PUT", f'/api/v2/context/{context_id}/environment-variable/{variable_name}', payload, headers=CIRCLECI_API_BASE_HEADERS)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))

def create(api_token, owner_slug, context_name, variable_name, variable_value):
  global CIRCLECI_API_BASE_HEADERS
  CIRCLECI_API_BASE_HEADERS = { 'authorization': f"Basic {api_token}",
    'Content-Type': "application/json",
    'Circle-Token': f"{api_token}"
  }
  if find_context(api_token, owner_slug, context_name) == False:
    print(f"Creating {context_name}")
    payload = f'{{"name":"{context_name}","owner":{{"slug":"{owner_slug}","type":"organization"}}}}'
    conn = http.client.HTTPSConnection("circleci.com")
    conn.request("POST", "/api/v2/context", payload, headers=CIRCLECI_API_BASE_HEADERS)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
  set_environment_var_to_context(api_token, owner_slug, context_name, variable_name, variable_value)

def destroy(api_token, owner_slug, context_name):
  global CIRCLECI_API_BASE_HEADERS
  CIRCLECI_API_BASE_HEADERS = { 'authorization': f"Basic {api_token}",
    'Content-Type': "application/json",
    'Circle-Token': f"{api_token}"
  }
  if find_context(api_token, owner_slug, context_name) == True:
    print(f"Removing {context_name}")
    conn = http.client.HTTPSConnection("circleci.com")
    context_id = get_context_id(api_token, owner_slug, context_name)
    conn.request("DELETE", f'/api/v2/context/{context_id}', headers=CIRCLECI_API_BASE_HEADERS)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("action", choices=['create', 'destroy'], help="The variable determines whether to execute a create or destroy action on the context")
  parser.add_argument("api_token", help="API token for access to CircleCI REST API")
  parser.add_argument("owner_slug", help="A string that represents the Organization URL for the CircleCI Org")
  parser.add_argument("context_name", help="The name of the context to be updated")
  parser.add_argument("variable_name", nargs='?', default=argparse.SUPPRESS, help="The name of the environment variable to be set within the given context")
  parser.add_argument("variable_value", nargs='?', default=argparse.SUPPRESS, help="The value of the environment variable to be set within the given context")
  args = parser.parse_args()
  if args.action == "create":
    create(args.api_token, args.owner_slug, args.context_name, args.variable_name, args.variable_value)
  elif args.action == "destroy":
    destroy(args.api_token, args.owner_slug, args.context_name)
