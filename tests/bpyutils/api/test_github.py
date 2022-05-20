from bpyutils.util.environ import getenv
from bpyutils.api.github   import GitHub

def test_github():
    github_access_token = getenv("GITHUB_TOKEN", raise_err = True)
    github_username = getenv("GITHUB_USERNAME", "achillesrasquinha")
    github_reponame = getenv("GITHUB_REPONAME", "bpyutils")

    github = GitHub(github_access_token)
    
    github\
        .repo(
            github_username,
            github_reponame
        )\
        .pr()

import pytest


def test_git_hub():
	raise NotImplementedError

def test_git_hub___init__():
	raise NotImplementedError

def test_git_hub_repo():
	raise NotImplementedError

def test_git_hub_pr():
	raise NotImplementedError

