# GitLocHistory

GitLocHistory is a command-line tool that calculates the history of lines of code of one or multiple Git repositories and their submodules. It uses the `scc` command-line tool (https://github.com/boyter/scc) to do the counting.



## Prerequisites

Before you can use GitLocHistory, you need to have the following tools installed on your system:

- Python 3.7 or later (https://www.python.org/downloads/)
- `git` (https://git-scm.com/downloads)
- `scc` (https://github.com/boyter/scc#installation)



## Usage

1. Clone the GitLocHistory repository to your local machine.
   ```shell
   git clone git:github.com/lennartmoeller/GitLocHistory.git
   ```

2. Install the required Python packages.
   ```shell
   pip3 install -r GitLocHistory/requirements.txt
   ```

3. Modify the file named `config.json`. See the Configuration section for more details.

4. Run GitLocHistory.
   ```shell
   python3 GitLocHistory/glh.py
   ```

5. Open the `viewer.html` file in your browser to view the result diagram.

6. The output is saved in the output JSON file in the `GitLocHistory` directory.



## Configuration

GitLocHistory uses a configuration file named `config.json` inside the `GitLocHistory` directory.

Here's an example `config.json` file:

```json
{
  "output": "locs.json",
  "repos": [
    {
      "url": "https://github.com/example/repo1.git",
      "dir": "directory/to/analyse",
      "include_submodules": false,
      "scc": {
        "exclude-dir": ["docs"],
        "include-ext": ["java", "php"]
      }
    },
    {
      "url": "https://github.com/example/repo2.git",
      "scc": {
        "exclude-ext": ["json"]
      }
    }
  ],
  "scc": {
    "exclude-dir": ["tests"],
    "exclude-ext": ["md", "py"]
  }
}

```

#### `repos` (required)

The repositories to include. Configure every repository with:

- `url ` (required): The repository URL 
- `dir` (optional): Directory relative to the repository root that should get analyzed (default: root).
- `include_submodules` (optional): Whether submodules and their commits should be included too (default: true).
- `scc` (optional): A repository-specific `scc` configuration that extends the global `scc ` configuration. See below for the supported options.

#### `output` (optional)

The name of the output file. If not specified, `output.json` will be used.

#### `scc` (optional)

The options to pass to the `scc` tool for every repository. Currently supported are:

- `exclude-dir`: List of directories to exclude (default [.git,.hg,.svn]). Does not affect submodules.
- `exclude-ext`: List of file extensions to ignore (overrides include-ext)
- `include-ext`: List of file extensions to limit files (gets overwritten by exclude-ext)



### Overriding

You can override submodules with a repository after the parent repository to have separate configurations.



## Output

The output JSON file consists of a list of datapoint objects:

- `timestamp`: UNIX timestamp
- `lines`: Total number of lines
- `code`: Number of lines of code
- `comment`: Number of lines of comments
- `blank`: Number of blank lines

Here is an example output:

```json
[
  {
    "timestamp": 1519886665,
    "lines": 35,
    "code": 24,
    "comment": 4,
    "blank": 7
  },
  {
    "timestamp": 1519937828,
    "lines": 92,
    "code": 68,
    "comment": 8,
    "blank": 16
  }
]
```



## Performance Limitations

- Although the `scc` command line tool has a good performance, this tool is very slow because of the commands `git clone` (per repository) and `git checkout` (per commit). Surely a different approach could create a more performant solution.
- Currently, when overwriting a submodule with a repository, both repositories are cloned, but only the last one is used.

