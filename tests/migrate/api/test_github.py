import pytest

from upyog.util.environ import getenv
from upyog.api.github   import GitHub

github_username = getenv("GITHUB_USERNAME", "achillesrasquinha")
github_reponame = getenv("GITHUB_REPONAME", "upyog")

@pytest.fixture
def github():
    github_access_token = getenv("GITHUB_TOKEN", raise_err = True)
    github = GitHub(github_access_token)
    return github

def test_git_hub_repo(github):
    pass

def test_git_hub_pr(github):
    with pytest.raises(ValueError):
        github.pr()

    github\
        .repo(
            github_username,
            github_reponame
        )\
        .pr()