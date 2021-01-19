import os
import re
import sys


CURRENT_BLOG_CONTENT_RELATIVE_PATH = "content/blog"
PRINT_PROGRESS_DOT_EVERY_X_ITEMS = 100


def get_filename_from_path(page_path):
    return os.path.splitext(os.path.basename(page_path))[0]


def get_legacy_datestr_from_filename(page_filename):
    return re.sub(r"\-\-.*$", "", page_filename)


def get_current_repo_path(this_script_path):
    current_repo_path = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.realpath(this_script_path)),
            ".."))

    if not os.path.isdir(current_repo_path):
        raise ValueError(
            "Expected current repo path {0} is not a valid directory".format(
                current_repo_path))

    return current_repo_path


def get_dir_path_in_repo(repo_path, dir_path):
    path_in_repo = os.path.realpath(os.path.join(repo_path, dir_path))

    if not os.path.isdir(path_in_repo):
        raise ValueError((
            "Expected directory {0} to exist in repo path {1} but unable to "
            "find it").format(dir_path, repo_path))

    return path_in_repo


def print_progress_dot(i, num_items):
    if i and ((not i % PRINT_PROGRESS_DOT_EVERY_X_ITEMS) or (i + 1 == num_items)):
        sys.stdout.write(".")

        if i + 1 == num_items:
            sys.stdout.write("\n")

        sys.stdout.flush()
