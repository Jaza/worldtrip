#!/usr/bin/env python
import glob
import re

from importutils import (
    CURRENT_BLOG_CONTENT_RELATIVE_PATH, get_current_repo_path, get_dir_path_in_repo,
    print_progress_dot)


LEGACY_GALLERY_ITEM_REGEX = (
    r"<div[^>]*>\s*<img(\s+class=\"[^\"]+\")?\s*"
    r"src=\"(?P<src>//static.flickr.com/[^/]+/(?P<filename>[^\"]+))\"\s*\/>\s*"
    r"<\/div>\s*"
    r"<p>\s*<em>\s*(?P<desc>.+?(?=<\/em>))<\/em>\s*(\.\s*)?<\/p>")

HTML_LINK_REGEX = r"<a href=\"(?P<url>[^\"]+)\">(?P<desc>[^>]+)<\/a>"


def html_formatting_to_markdown(text):
    new_text = re.sub(HTML_LINK_REGEX, "[\g<desc>](\g<url>)", text)
    return new_text.replace("<strong>", "**").replace("</strong>", "**")


def import_legacy_gallery_items_for_page(file_path):
    num_gallery_items_imported = 0
    content = ""

    with open(file_path, "r") as f:
        line = None

        while (line is None) or line:
            line = f.readline()
            content += line

    for m in re.finditer(LEGACY_GALLERY_ITEM_REGEX, content):
        src = m.group("src")
        filename = m.group("filename")
        desc = html_formatting_to_markdown(m.group("desc"))
        num_gallery_items_imported += 1

    return num_gallery_items_imported


def import_legacy_gallery_items(current_content_path):
    glob_path = "{0}/200*.html".format(current_content_path)
    page_paths = glob.glob(glob_path)
    num_items = len(page_paths)
    num_gallery_items_imported = 0

    for i, page_path in enumerate(page_paths):
        num_gallery_items_imported += import_legacy_gallery_items_for_page(page_path)
        print_progress_dot(i, num_items)

    return num_gallery_items_imported


def run():
    current_repo_path = get_current_repo_path(__file__)
    current_content_path = get_dir_path_in_repo(
        current_repo_path, CURRENT_BLOG_CONTENT_RELATIVE_PATH)

    glob_path = "{0}/200*.html".format(current_content_path)
    print("Found {0} blog posts".format(len(glob.glob(glob_path))))

    num_gallery_items_imported = import_legacy_gallery_items(current_content_path)
    print("Imported {0} legacy gallery items (TODO: actually import them!)".format(
        num_gallery_items_imported))


if __name__ == "__main__":
    run()
