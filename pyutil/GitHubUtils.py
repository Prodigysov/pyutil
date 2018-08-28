from github import Github, RateLimitExceededException
from pyutil import LoggingUtils
from datetime import datetime
from time import sleep
import traceback

from typing import *


class GitHubUtils:

    logger = LoggingUtils.get_logger("GitHubUtils")

    GITHUB_SEARCH_ITEMS_MAX = 1000
    DEFAULT_ACCESS_TOKEN = "93e7bf061b52c1a8d1511289cc02085878a95b08"  # prodigysov-work:pyutil
    DEFAULT_GITHUB_OBJECT = Github(DEFAULT_ACCESS_TOKEN)

    @classmethod
    def get_github(cls, access_token: str = None) -> Github:
        if access_token is None:
            return cls.DEFAULT_GITHUB_OBJECT
        else:
            return Github(access_token)

    @classmethod
    def search_repos(cls, q: str = "", sort: str = "stars", order: str = "desc",
                     is_allow_fork: bool = False,
                     max_num_repos: int = GITHUB_SEARCH_ITEMS_MAX,
                     github: Github = DEFAULT_GITHUB_OBJECT,
                     is_wait_rate_limit: bool = True,
                     *_, **qualifiers) -> List[str]:
        """
        Searches the repos by querying GitHub API v3.
        :return: a list of full names of the repos match the query.
        """
        num_repos = 0
        repos = list()
        iterator_repos = github.search_repositories(q, sort, order, **qualifiers)
        while True:
            try:
                repo = next(iterator_repos)
            except StopIteration:
                cls.logger.info("Reached the end of iteration.")
                break
            except RateLimitExceededException as e:
                cls.logger.warning("Reached rate limit: {}".format(str(e)))
                if not is_wait_rate_limit:
                    cls.logger.warning("Not waiting for rate limit.")
                    break
                else:
                    rate_limit_reset_time = datetime.fromtimestamp(github.rate_limiting_resettime)
                    rate_limit_wait_seconds = (rate_limit_reset_time - datetime.now()).total_seconds() + 1
                    cls.logger.warning("Rate limit will recover at: {}, will wait for {} seconds.".format(rate_limit_reset_time, rate_limit_wait_seconds))
                    sleep(rate_limit_wait_seconds)
                    cls.logger.warning("Rate limit recovered")
                    continue
                # end if
            except:
                cls.logger.warning("Unknown exception: {}".format(traceback.format_exc()))
                cls.logger.warning("Returning partial results.")
                break
            # end try except
            if not is_allow_fork:
                if repo.fork:
                    continue
            # end if, if
            repos.append(repo.full_name)
            num_repos += 1
            if num_repos >= max_num_repos:
                break
            # end if
        # end for
        return repos

    @classmethod
    def search_users(cls, q: str = "", sort: str = "repositories", order: str = "desc",
                     max_num_users: int = GITHUB_SEARCH_ITEMS_MAX,
                     github: Github = DEFAULT_GITHUB_OBJECT,
                     is_wait_rate_limit: bool = True,
                     *_, **qualifiers) -> List[str]:
        """
        Searches the users by querying GitHub API v3.
        :return: a list of usernames (login) of the users match the query.
        """
        num_users = 0
        users = list()
        iterator_users = github.search_users(q, sort, order, **qualifiers)
        while True:
            try:
                user = next(iterator_users)
            except StopIteration:
                cls.logger.info("Reached the end of iteration.")
                break
            except RateLimitExceededException as e:
                cls.logger.warning("Reached rate limit: {}".format(str(e)))
                if not is_wait_rate_limit:
                    cls.logger.warning("Not waiting for rate limit.")
                    break
                else:
                    rate_limit_reset_time = datetime.fromtimestamp(github.rate_limiting_resettime)
                    rate_limit_wait_seconds = (rate_limit_reset_time - datetime.now()).total_seconds() + 1
                    cls.logger.warning("Rate limit will recover at: {}, will wait for {} seconds.".format(rate_limit_reset_time, rate_limit_wait_seconds))
                    sleep(rate_limit_wait_seconds)
                    cls.logger.warning("Rate limit recovered")
                    continue
                # end if
            except:
                cls.logger.warning("Unknown exception: {}".format(traceback.format_exc()))
                cls.logger.warning("Returning partial results.")
                break
            # end try except
            users.append(user.login)
            num_users += 1
            if num_users >= max_num_users:
                break
            # end if
        # end for
        return users

    @classmethod
    def search_repos_of_language(cls, language: str, max_num_repos: int = float("inf"),
                                 is_allow_fork: bool = False,
                                 is_wait_rate_limit: bool = True,
                                 strategies: List[str] = None) -> List[str]:
        """
        Searches for all the repos of the language.
        :return: a list of full names of matching repos.
        """
        if strategies is None:
            strategies = ["search_repos", "search_users"]
        # end if

        # Check supported strategies
        supported_strategies = ["search_repos", "search_users", "enum_users"]
        for strategy in strategies:
            assert strategy in supported_strategies, strategy
        # end for

        s_repos = set()

        # Strategy 1: search repos (limited to 1000)
        strategy = "search_repos"
        if strategy in strategies:
            cls.logger.info("Using strategy {}".format(strategy))
            l_repos = cls.search_repos("language:{}".format(language), is_allow_fork=is_allow_fork, is_wait_rate_limit=is_wait_rate_limit, max_num_repos=max_num_repos)
            s_repos = s_repos.union(l_repos)
            if len(s_repos) >= max_num_repos:
                return list(s_repos)
            # end if
        # end if

        # Strategy 2: search users (~37000?)
        strategy = "search_users"
        if strategy in strategies:
            cls.logger.info("Using strategy {}".format(strategy))
            s_users = set()
            s_users = s_users.union(cls.search_repos("language:{}".format(language), sort="repositories", is_wait_rate_limit=is_wait_rate_limit))
            s_users = s_users.union(cls.search_repos("language:{}".format(language), sort="followers", is_wait_rate_limit=is_wait_rate_limit))
            s_users = s_users.union(cls.search_repos("language:{}".format(language), sort="joined", is_wait_rate_limit=is_wait_rate_limit))
            for user in s_users:
                l_repos = cls.search_repos("language:{}+user:{}".format(language, user), is_allow_fork=is_allow_fork, is_wait_rate_limit=is_wait_rate_limit)
                s_repos = s_repos.union(l_repos)
                if len(s_repos) >= max_num_repos:
                    return list(s_repos)
                # end if
            # end for
        # end if

        # Strategy 3: enum users (?)
        strategy = "enum_users"
        if strategy in strategies:
            cls.logger.warning("Strategy {} is not implemented yet.".format(strategy))
            cls.logger.warning("Nothing happens.")
        # end if

        cls.logger.warning("Got {}/{} repos.".format(len(s_repos), max_num_repos))
        return list(s_repos)
