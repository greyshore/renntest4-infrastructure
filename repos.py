from github import Github
import argparse

def check_repo_exists(org_name, repository_name):
  try:
    repo = g.get_repo(f'{org_name}/{repository_name.lower()}')
    return True
  except:
    print(f'{repository_name.lower()} is not found in {org_name}.')
    return False


def archive_repo(org_name, repository_name):
  repo = g.get_repo(f'{org_name}/{repository_name.lower()}')
  if repo.archived == False:
    repo.edit(archived=True)
    print(f'{repository_name.lower()} is now archived.')
  else:
    print(f'{repository_name.lower()} is already archived.')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("github_token", help="API token for access to Github REST API")
  parser.add_argument("org_name", help="The name of the Github organization")
  parser.add_argument("repository_name", help="The name of the Github repo on which to execute actions")
  args = parser.parse_args()
  g = Github(args.github_token)
  if check_repo_exists(args.org_name, args.repository_name) == True:
    archive_repo(args.org_name, args.repository_name)
  