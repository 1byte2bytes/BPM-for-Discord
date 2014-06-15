#!/usr/bin/env python3
# -*- coding: utf8 -*-
################################################################################
##
## Copyright (C) 2012 Typhos
##
## This Source Code Form is subject to the terms of the Mozilla Public
## License, v. 2.0. If a copy of the MPL was not distributed with this
## file, You can obtain one at http://mozilla.org/MPL/2.0/.
##
################################################################################

import argparse
import hashlib
import os
import subprocess
import time
import urllib.request

import bplib.objects
import bplib.resolve

AutogenHeader = """
/*
 * This file is AUTOMATICALLY GENERATED. DO NOT EDIT.
 * Generated at %s.
 */

""" % (time.strftime("%c"))

TempFilename = "animote-temp.png"
AnimoteUrlPrefix = "https://ponymotes.net/"

def find_animotes(emotes):
    images = {}
    for (name, emote) in emotes.items():
        if emote.source.variant_matches is None:
            emote.source.match_variants()
        root = emote.source.variant_matches[emote]
        if "+animote" in root.tags:
            images.setdefault(emote.base_variant().image_url, []).append(emote)
    return images

def image_path(url):
    hash = hashlib.sha256(url.encode("ascii")).hexdigest()
    filename = "animotes/%s.gif" % (hash)
    return filename

def update_cache(images):
    for (i, url) in enumerate(images):
        gif_filename = image_path(url)
        if os.path.exists(gif_filename):
            continue

        print("[%s/%s] %s -> %s" % (i + 1, len(images), url, gif_filename))
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as stream:
            data = stream.read()
        open(TempFilename, "wb").write(data)
        subprocess.call(["apng2gif", TempFilename, gif_filename])
        os.remove(TempFilename)

def dump_css(file, images):
    file.write(AutogenHeader)
    for (url, emotes) in images.items():
        selectors = []
        for emote in emotes:
            for variant in emote.variants.values():
                if hasattr(variant, "image_url") and variant.image_url == url:
                    selectors.append(variant.selector())
        selector = ",".join(selectors)
        new_url = AnimoteUrlPrefix + image_path(url)
        s = "%s{background-image:url(%s)!important}\n" % (selector, new_url)
        file.write(s)

def main():
    parser = argparse.ArgumentParser(description="Download and convert APNG animotes to GIF")
    parser.add_argument("-c", "--css", help="Output CSS file", default="build/gif-animotes.css")
    args = parser.parse_args()

    context = bplib.objects.Context()
    context.load_config()
    context.load_sources()

    emotes, all_emotes = bplib.resolve.resolve_emotes(context)
    images = find_animotes(emotes)
    update_cache(images)
    with open(args.css, "w") as file:
        dump_css(file, images)

if __name__ == "__main__":
    main()
