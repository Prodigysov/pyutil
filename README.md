# Project `pyutil`

Current utils:
- BashUtils: for executing bash commands and get return value / stdout / stderr;
- CliUtils: for command line argument parsing, without the need to declare each argument;
- GitHubUtils: for mining GitHub, using `PyGitHub` package;
- IOUtils: for input / output to file, directory, in different formats;
- LoggingUtils: for logging;
- MiscUtils: for whatever functions that may not belong to other classes;
- Stream: similar to java.utils.Stream;
- TimeUtils: for adding time constrain on an operation;

- latex package: for writing macros and tables for latex documents;


## Development Plans

- Version `0.2`:
  
  - Category the utils as "core" and "others", where core utils do not depend on each other (thus can be safely unit-tested).
  - Add unit tests for at least all core utils.
