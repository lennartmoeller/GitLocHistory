from __future__ import annotations

from json import dump
from os import path
from shutil import rmtree

from internals.Commit import Commit
from internals.Config.Config import Config
from internals.Constants import TMP_DIR
from internals.Datapoint import Datapoint
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


def calculate_commit_statics(commits: list[Commit]) -> list[dict[str, int]]:
    """
    :param commits: The commits to calculate the statistics for.
    :return: The statistics per commit as a list of dictionaries.
    """
    statistics_per_repo: dict[str, Datapoint] = {}
    statistics_per_commit: list[dict[str, int]] = []
    for commit in commits:
        commit.checkout()
        statistics_per_repo[commit.repo.hash] = commit.repo.statistics
        commit_statistics: Datapoint = Datapoint(commit.timestamp)
        for repo_statistics in statistics_per_repo.values():
            commit_statistics.add(repo_statistics)
        statistics_per_commit.append(commit_statistics.__dict__)
    return statistics_per_commit


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
    print("Calculating commit statistics...")
    commit_statistics = calculate_commit_statics(commits)
    print("Removing tmp dir...")
    rmtree(TMP_DIR)
    print("Writing result into output json...")
    with open(config.output_filename, 'w') as f:
        dump(commit_statistics, f)


if __name__ == '__main__':
    main()
