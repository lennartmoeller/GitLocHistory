from __future__ import annotations

from json import loads

from internals.Config.RepoConfig import RepoConfig
from internals.Config.SccConfig import SccConfig


class Config:
    """
    The main configuration class.
    """

    _output_filename: str
    _repos: list[RepoConfig] = []

    def __init__(self):
        """
        Config constructor.
        Loads the configuration from the config file (config.json).
        """
        # get config from file
        with open('config.json') as config_file:
            file_contents = config_file.read()
        config = loads(file_contents)
        # set output file
        self._output_filename = "output.json" if "output" not in config else config["output"]
        # set repos
        if "repos" not in config:
            raise Exception("No repositories specified")
        global_scc = SccConfig({} if "scc" not in config else config["scc"])
        for repo_config in config["repos"]:
            self._repos.append(RepoConfig(repo_config, global_scc))

    @property
    def output_filename(self) -> str:
        """
        :return: The name of the output json file.
        """
        return self._output_filename

    @property
    def repos(self) -> list[RepoConfig]:
        """
        :return: The repository configurations.
        """
        return self._repos
