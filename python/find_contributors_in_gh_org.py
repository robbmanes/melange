#!/usr/bin/env python
import httpx
import json
import sys

# walks a github organization for all repositories, then provides a json array of contributors

# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
# profile -> developer settings -> personal access tokens -> fine grained tokens
PERSONAL_ACCESS_TOKEN=''
GITHUB_API_VERSION='2022-11-28'
BASE_URL='https://api.github.com'
ORG='containers'

def main():
    headers = {
        'Authorization': 'Bearer %s' % (PERSONAL_ACCESS_TOKEN),
        'X-GitHub-Api-Version': '%s' % (GITHUB_API_VERSION),
    }
    with httpx.Client(base_url=BASE_URL, headers=headers) as client:
        result = client.get('octocat')
        if result.status_code != 200:
            raise Exception("Could not authenticate to test endpoint: %s", result)
        result = client.get('orgs/containers/repos')
        org_repos = result.json()

        all_contributors = []
        contributors_per_repo = {}
        for repo in org_repos:
            contributors_per_repo[repo['full_name']] = []
            result = client.get('repos/%s/contributors' % repo['full_name'])
            contributors = result.json()
            for contributor in contributors:
                all_contributors.append(contributor['login'])
                user = {
                    contributor['login']: {
                        'contribution_count': contributor['contributions'],
                        'url': contributor['url'],
                    }
                }
                contributors_per_repo[repo['full_name']].append(user)
        report = {
            'contributors': list(set(all_contributors)),
            'repositories': contributors_per_repo,
        }
        print(json.dumps(report))


if __name__ == '__main__':
    sys.exit(main())
