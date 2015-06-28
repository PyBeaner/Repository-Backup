# coding=utf-8
import json

__author__ = 'PyBeaner'
import os
import requests
import threading
import subprocess

api_url = "https://api.github.com/"
github_url = "https://github.com/"


def get_user_repos(user):
    suffix = "users/{}/repos".format(user)
    url = api_url + suffix
    print("fetching", url)
    r = requests.get(url)
    repos = r.json()
    save_as = open("%s.repos.json" % user, "wt", errors="replace")
    print(json.dumps(repos), file=save_as)
    for repo in repos:
        repo_fullname = repo["full_name"]
        clone_or_pull_repo(full_name=repo_fullname)


from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
save_to = config.get("path", "save_to")
if not save_to:
    save_to = "repos"

def clone_or_pull_repo(user=None, repo_name=None, full_name=None, save_to=save_to):
    if full_name:
        url = "{}{}".format(github_url, full_name)
        user, repo_name = full_name.split("/")
    else:
        url = "{}{}/{}".format(github_url, user, repo_name)
    save_as = os.path.join(save_to, repo_name)
    if os.path.exists(save_as):
        target = pull_repo
        args = (repo_name,)
    else:
        target = download_repo
        args = (url,)
    t = threading.Thread(target=target, args=args)
    t.start()
    t.join()


def download_repo(repo_url):
    os.chdir(save_to)
    print("cloning repo {} into {}".format(repo_url, save_to))
    subprocess.Popen(["git", "clone", repo_url])


def pull_repo(repo_name):
    dir = os.path.join(save_to, repo_name)
    os.chdir(dir)
    print("pulling repo:", repo_name)

    subprocess.Popen(["git", "pull"])


if __name__ == '__main__':
    get_user_repos("PyBeaner")
