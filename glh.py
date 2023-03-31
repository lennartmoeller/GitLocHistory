from __future__ import annotations

from json import dump
from os import path
from shutil import rmtree
from typing import Literal

from internals.Commit import Commit
from internals.Config.Config import Config
from internals.Constants import TMP_DIR
from internals.Repo import Repo


def create_repos(config: Config) -> dict[str, Repo]:
    """
    Creates all repositories and returns them.
    If a repository is duplicated, the last one will be used (useful for overriding submodule configuration).
    :param config: The global configuration.
    :return: All repositories.
    """
    repos = {}
    for repo_config in config.repos:
        repo = Repo(repo_config)
        repos[repo.hash] = repo
        if not repo.config.include_submodules:
            continue
        for subrepo in repo.subrepos:
            repos[subrepo.hash] = subrepo
    return repos


def create_sorted_commits(repos: dict[str, Repo]) -> list[Commit]:
    """
    :param repos: The repositories to get the commits from.
    :return: All commits sorted by timestamp.
    """
    commits = []
    for repo in repos.values():
        for commit in repo.commits:
            commits.append(Commit(repo, commit))
    return sorted(commits, key=lambda c: c.timestamp)


def calculate_loc_per_commit(commits: list[Commit]) -> list[dict[Literal["x", "y"], int]]:
    """
    Calculates the loc per commit.
    :param commits: The commits to calculate the loc for.
    :return: A list of dicts with UNIX timestamp (x) and loc (y) for each commit.
    """
    loc_per_commit: list[dict[Literal["x", "y"], int]] = []
    loc_per_repo: dict[Repo, int] = {}
    for commit in commits:
        commit.checkout()
        loc_per_repo[commit.repo] = commit.repo.loc
        loc_per_commit.append({"x": commit.timestamp, "y": sum(loc_per_repo.values())})
    return loc_per_commit


def main():
    if path.exists(TMP_DIR):
        print("Removing old tmp dir...")
        rmtree(TMP_DIR)
    print("Parsing config...")
    config = Config()
    print("Cloning repos...")
    repos = create_repos(config)
    print("Collecting commits...")
    commits = create_sorted_commits(repos)
    print("Calculating loc per commit...")
    loc_per_commit = calculate_loc_per_commit(commits)
    print("Removing tmp dir...")
    rmtree(TMP_DIR)
    print("Writing result into output json...")
    with open(config.output_filename, 'w') as f:
        dump(loc_per_commit, f)


if __name__ == '__main__':
    main()
