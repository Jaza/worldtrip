#!/usr/bin/env python
import os
import re
from collections import namedtuple


LEGACY_REPO_PATH_ENVVAR_NAME = "WORLDTRIP_LEGACY_REPO_PATH"
LEGACY_BLOG_PAGES_RELATIVE_PATH = "pages/blog"
LEGACY_BLOG_CONTENT_FULL_RELATIVE_PATH = "content/blog/full"
LEGACY_BLOG_CONTENT_TEASER_RELATIVE_PATH = "content/blog/teaser"
CURRENT_BLOG_CONTENT_RELATIVE_PATH = "content/blog"

LEGACY_BLOG_TITLE_LINE_PREFIX = "$title = '"
LEGACY_BLOG_TITLE_LINE_SUFFIX = "';\n"


PathsInRepos = namedtuple("PathsInRepos", [
    "legacy_pages_path",
    "legacy_content_full_path",
    "legacy_content_teaser_path",
    "current_content_path"])


def get_legacy_repo_path(legacy_repo_path):
    if not legacy_repo_path:
        raise ValueError(
            "Missing required environment variable {0}".format(
                LEGACY_REPO_PATH_ENVVAR_NAME))

    if not os.path.isdir(legacy_repo_path):
        raise ValueError((
            "Environment variable {0} value '{1}' is not a valid "
            "directory").format(
                LEGACY_REPO_PATH_ENVVAR_NAME, legacy_repo_path))

    return os.path.realpath(legacy_repo_path)


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


def get_paths_in_repos(legacy_repo_path, current_repo_path):
    legacy_pages_path = get_dir_path_in_repo(
        legacy_repo_path, LEGACY_BLOG_PAGES_RELATIVE_PATH)
    legacy_content_full_path = get_dir_path_in_repo(
        legacy_repo_path, LEGACY_BLOG_CONTENT_FULL_RELATIVE_PATH)
    legacy_content_teaser_path = get_dir_path_in_repo(
        legacy_repo_path, LEGACY_BLOG_CONTENT_TEASER_RELATIVE_PATH)
    current_content_path = get_dir_path_in_repo(
        current_repo_path, CURRENT_BLOG_CONTENT_RELATIVE_PATH)

    return PathsInRepos(
        legacy_pages_path,
        legacy_content_full_path,
        legacy_content_teaser_path,
        current_content_path)


def get_filename_from_path(page_path):
    return os.path.splitext(os.path.basename(page_path))[0]


def get_slug_from_filename(page_filename):
    return re.sub(
        r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\-[0-9]{2}\-[0-9]{2}\-[0-9]{2}\-\-",
        "",
        page_filename)


def get_title_from_slug(slug):
    return slug.replace("-", " ").capitalize()


def get_title_from_page_file(page_path):
    title = None

    with open(page_path) as f:
        line = None

        while (line is None) or (line and (not title)):
            line = f.readline()

            if line.startswith("$title = '"):
                title = (
                    line.replace(LEGACY_BLOG_TITLE_LINE_PREFIX, "")
                        .replace(LEGACY_BLOG_TITLE_LINE_SUFFIX, "")
                        .replace("\\'", "'"))

    return title


def import_legacy_blog_post(legacy_page_path, paths_in_repos):
    page_filename = get_filename_from_path(legacy_page_path)

    current_content_file_path = os.path.realpath(os.path.join(
        paths_in_repos.current_content_path,
        "{0}.html".format(page_filename)))

    if os.path.isfile(current_content_file_path):
        return False

    title = get_title_from_page_file(legacy_page_path)

    if not title:
        slug = get_slug_from_filename(page_filename)
        title = get_title_from_slug(slug)

    if not title:
        raise ValueError(
            "Unable to determine title for page path {0}".format(
                legacy_page_path))

    # TODO: actually import blog posts here!

    return True


def import_legacy_blog_posts(paths_in_repos):
    legacy_pages_path = paths_in_repos.legacy_pages_path
    num_blog_posts_imported = 0
    num_blog_posts_existing = 0

    for legacy_page_path in os.listdir(legacy_pages_path):
        is_imported = import_legacy_blog_post(
            os.path.realpath(os.path.join(legacy_pages_path, legacy_page_path)),
            paths_in_repos)

        if is_imported:
            num_blog_posts_imported += 1
        else:
            num_blog_posts_existing += 1

    return num_blog_posts_imported, num_blog_posts_existing


def run():
    legacy_repo_path = get_legacy_repo_path(
        os.environ.get(LEGACY_REPO_PATH_ENVVAR_NAME))
    current_repo_path = get_current_repo_path(__file__)

    paths_in_repos = get_paths_in_repos(legacy_repo_path, current_repo_path)

    num_legacy_blog_posts = len(os.listdir(paths_in_repos.legacy_pages_path))
    print("Found {0} legacy blog posts".format(num_legacy_blog_posts))

    num_blog_posts_imported, num_blog_posts_existing = (
        import_legacy_blog_posts(paths_in_repos))
    print("Imported {0} legacy blog posts (TODO: actually import them!)".format(
        num_blog_posts_imported))
    print("Did not import {0} already-imported legacy blog posts".format(
        num_blog_posts_existing))


if __name__ == "__main__":
    run()
