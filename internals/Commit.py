from __future__ import annotations

import git

from internals.Repo import Repo


class Commit:
    """
    A commit of a repository.
    """

    _repo: Repo
    _git: git.Commit

    def __init__(self, repo: Repo, commit: git.Commit):
        """
        Commit constructor.
        :param repo: The repository this commit belongs to.
        :param commit: The git commit object.
        """
        self._repo = repo
        self._git = commit

    @property
    def timestamp(self) -> int:
        """
        :return: The UNIX timestamp of the commit.
        """
        return self._git.committed_date

    @property
    def repo(self) -> Repo:
        """
        :return: The repository this commit belongs to.
        """
        return self._repo

    def checkout(self):
        """
        Checks out this commit.
        """
        self._repo.checkout(self._git)
