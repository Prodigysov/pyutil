import os


class TestSupport:
    """
    Macros, utility functions for tests.
    """
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJECT_DIR = os.path.dirname(THIS_DIR)
    SUBJECTS_DIR = os.path.join(PROJECT_DIR, "test-subjects")
