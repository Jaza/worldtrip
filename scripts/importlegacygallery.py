#!/usr/bin/env python
import glob
import re
from collections import namedtuple

from slugify import slugify

from importutils import (
    CURRENT_BLOG_CONTENT_RELATIVE_PATH, get_current_repo_path, get_dir_path_in_repo,
    get_filename_from_path, get_legacy_datestr_from_filename, print_progress_dot)


LEGACY_GALLERY_ITEM_REGEX = (
    r"<div[^>]*>\s*<img(\s+class=\"[^\"]+\")?\s*"
    r"src=\"(?P<src>//static.flickr.com/[^/]+/(?P<filename>[^\"]+))\"\s*\/>\s*"
    r"<\/div>\s*"
    r"<p>\s*<em>\s*(?P<desc>.+?(?=<\/em>))<\/em>\s*(\.\s*)?<\/p>")

HTML_LINK_REGEX = r"<a href=\"(?P<url>[^\"]+)\">(?P<desc>[^>]+)<\/a>"

PAGE_DATESTR_REGEX = (
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-"
    r"(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2})$")

DATESTR_FORMAT_STR = (
    "{year:04d}-{month:02d}-{day:02d}-{hour:02d}-{minute:02d}-{second:02d}")

PARENTHESISED_TEXT_REGEX = r"\([^)]+\)"

MAX_SLUG_LEN = 50


LegacyGalleryItem = namedtuple("LegacyGalleryItem", ["src", "filename", "desc"])


LEGACY_FILENAME_TO_CURRENT_FILENAME_MAP_CACHE = {}


def html_formatting_to_markdown(text):
    new_text = re.sub(HTML_LINK_REGEX, "[\g<desc>](\g<url>)", text)
    return new_text.replace("<strong>", "**").replace("</strong>", "**")


def truncate_slug(current_slug, max_len):
    new_slug = ""
    slug_parts = current_slug.split("-")
    slug_parts_iter = iter(slug_parts)
    slug_part = next(slug_parts_iter, None)

    while slug_part and len(new_slug) <= 50:
        if new_slug:
            new_slug = "{0}-".format(new_slug)

        new_slug = "{0}{1}".format(new_slug, slug_part)
        slug_part = next(slug_parts_iter, None)

    return new_slug


def import_legacy_gallery_item(page_path, gallery_item, current_filename_index):
    filename = gallery_item.filename

    if filename in LEGACY_FILENAME_TO_CURRENT_FILENAME_MAP_CACHE:
        return False

    page_filename = get_filename_from_path(page_path)
    page_datestr = get_legacy_datestr_from_filename(page_filename)
    m = re.match(PAGE_DATESTR_REGEX, page_datestr)

    if not m:
        raise ValueError((
            "Page path {0} does not contain expected date string in "
            "YYYY-MM-DD-HH-MM-SS format").format(page_path))

    date_parts = {k: int(v) for k, v in m.groupdict().items()}

    if current_filename_index:
        date_parts["minute"] += current_filename_index

    current_datestr = DATESTR_FORMAT_STR.format(**date_parts)
    truncated_desc = re.sub(PARENTHESISED_TEXT_REGEX, "", gallery_item.desc)
    current_slug = slugify(truncated_desc)

    if len(current_slug) > MAX_SLUG_LEN:
        current_slug = truncate_slug(current_slug, MAX_SLUG_LEN)

    current_filename = "{0}--{1}".format(current_datestr, current_slug)

    return True


def import_legacy_gallery_items_for_page(page_path):
    num_gallery_items_imported = 0
    content = ""

    with open(page_path, "r") as f:
        line = None

        while (line is None) or line:
            line = f.readline()
            content += line

    current_filename_index = 0

    for m in re.finditer(LEGACY_GALLERY_ITEM_REGEX, content):
        src = m.group("src")
        filename = m.group("filename")
        desc = html_formatting_to_markdown(m.group("desc"))
        is_embed_migrated = import_legacy_gallery_item(
            page_path, LegacyGalleryItem(src, filename, desc), current_filename_index)

        if is_embed_migrated:
            current_filename_index += 1

        num_gallery_items_imported += 1

    return num_gallery_items_imported, current_filename_index


def import_legacy_gallery_items(current_content_path):
    glob_path = "{0}/200*.html".format(current_content_path)
    page_paths = glob.glob(glob_path)
    num_items = len(page_paths)
    num_gallery_items_imported = 0
    num_embeds_migrated = 0

    for i, page_path in enumerate(page_paths):
        _num_gallery_items_imported, _num_embeds_migrated = (
            import_legacy_gallery_items_for_page(page_path))
        num_gallery_items_imported += _num_gallery_items_imported
        num_embeds_migrated += _num_embeds_migrated
        print_progress_dot(i, num_items)

    return num_gallery_items_imported, num_embeds_migrated


def run():
    current_repo_path = get_current_repo_path(__file__)
    current_content_path = get_dir_path_in_repo(
        current_repo_path, CURRENT_BLOG_CONTENT_RELATIVE_PATH)

    glob_path = "{0}/200*.html".format(current_content_path)
    print("Found {0} blog posts".format(len(glob.glob(glob_path))))

    num_gallery_items_imported, num_embeds_migrated = (
        import_legacy_gallery_items(current_content_path))
    print("Imported {0} legacy gallery items (TODO: actually import them!)".format(
        num_gallery_items_imported))
    print("Migrated {0} legacy gallery embeds".format(num_embeds_migrated))


if __name__ == "__main__":
    run()
