from __future__ import annotations

from json import loads
from os import path
from subprocess import run
from typing import Iterator

import git

from internals.Config.RepoConfig import RepoConfig
from internals.Constants import TMP_DIR
from internals.Datapoint import Datapoint


class Repo:
    """
    A git repository.
    """

    _config: RepoConfig
    _dir: str
    _git: git.Repo
    _hash: str

    def __init__(self, config: RepoConfig):
        """
        Repo constructor.
        Clones the repository.
        :param config: The repository configuration.
        """
        self._config = config
        self._locs = 0
        self._git = self.clone_and_get_repo()
        self._hash = self._git.git.rev_parse('HEAD', short=True)

    @property
    def config(self) -> RepoConfig:
        """
        :return: The repository configuration.
        """
        return self._config

    @property
    def hash(self) -> str:
        """
        :return: The hash of the current commit. Identifies the repository uniquely.
        """
        return self._hash

    @property
    def subrepos(self) -> list[Repo]:
        """
        :return: The sub repositories (submodules) of this repository.
        """
        subrepos = []
        for subrepo_url in [s.url for s in self._git.submodules]:
            subrepo_config = self._config.get_subrepo_config(subrepo_url)
            subrepos.append(Repo(subrepo_config))
        return subrepos

    @property
    def commits(self) -> Iterator[git.Commit]:
        """
        :return: An iterator over the commits of this repository.
        """
        return self._git.iter_commits()

    @property
    def statistics(self) -> Datapoint:
        """
        :return: The statistics of this repository with the current commit checked out and submodules excluded.
        """
        scc_dir = self._dir + "/" + self._config.dir
        scc_command = ["scc"] + [scc_dir] + self._config.scc.scc_command_flags
        result_str = run(scc_command, capture_output=True, text=True).stdout
        result = loads(result_str)
        datapoint = Datapoint(self._git.head.commit.committed_date)
        for lang_result in result:
            datapoint.add(lang_result)
        return datapoint

    def clone_and_get_repo(self) -> git.Repo:
        """
        Clones the repository.
        :return: The git.Repo object.
        """
        index = 0
        while True:
            self._dir = TMP_DIR + "/" + str(index)
            if not path.exists(self._dir):
                break
            index += 1
        git.Repo.clone_from(self.config.url, self._dir)
        return git.Repo(self._dir)

    def checkout(self, commit: git.Commit):
        """
        Checks out the given commit.
        :param commit: The commit to check out.
        """
        self._git.git.checkout(commit)
