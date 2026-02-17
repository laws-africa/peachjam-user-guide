#!/usr/bin/env python3
import os
import shutil
import json
import re

from jinja2 import Environment

def process_file(env, file_path, context):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace placeholders with context values
    template = env.from_string(content)
    processed_content = template.render(context)

    # replace the src with the localised version
    # <img src=".gitbook/assets/comments 1.png">
    prefix = f'{context["APPCODE"]}--'

    def replace_src(match):
        src = os.path.basename(match.group(2))
        if '--' not in src:
            return f'src="{match.group(1)}.gitbook/assets/{prefix}{src}"'
        return match.group(0)

    processed_content = re.sub(r'src="([^"]*)\.gitbook/assets/([^"]+)"', replace_src, processed_content)

    return processed_content

def copy_assets(src, dst, site):
    """Copy localised assets into a site variant.

    Override source: site-images/<appcode>/<lang>/<asset-filename>
    Default fallback: <lang>/.gitbook/assets/<asset-filename>
    """
    assets_dir = os.path.join(src, '.gitbook', 'assets')
    override_dir = os.path.join("site-images", site["APPCODE"], site["LANG"])
    dst_assets_dir = os.path.join(dst, '.gitbook', 'assets')
    prefix = f'{site["APPCODE"]}--'

    os.makedirs(dst_assets_dir, exist_ok=True)

    base_assets = {
        entry.name: entry.path
        for entry in os.scandir(assets_dir)
        if entry.is_file() and '--' not in entry.name
    }

    for fname, base_path in base_assets.items():
        override_unprefixed_path = os.path.join(override_dir, fname)
        override_prefixed_path = os.path.join(override_dir, f"{prefix}{fname}")

        if os.path.exists(override_unprefixed_path):
            src_path = override_unprefixed_path
        elif os.path.exists(override_prefixed_path):
            src_path = override_prefixed_path
        else:
            src_path = base_path

        shutil.copy(src_path, os.path.join(dst_assets_dir, f"{prefix}{fname}"))


def copy_and_process_tree(src, dst, site):
    print(f"Building {src} to {dst}")

    if os.path.exists(dst):
        shutil.rmtree(dst)

    def ignore(dir, content):
        if '.gitbook/assets' in dir:
            return content
        return []

    shutil.copytree(src, dst, ignore=ignore)
    copy_assets(src, dst, site)

    env = Environment(
        block_start_string="(%",
        block_end_string="%)",
        variable_start_string="%%",
        variable_end_string="%%",
    )

    # now post-process the .md files
    for root, _, files in os.walk(dst):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                processed_content = process_file(env, file_path, site)
                with open(file_path, 'w') as file:
                    file.write(processed_content)

def build_sites(peachjam_path, src_base, dst_base):
    with open(peachjam_path, 'r') as file:
        peachjam = json.load(file)

    for site in peachjam['sites']:
        if 'APPCODE' not in site:
            site['APPCODE'] = re.sub(r'[^a-zA-Z0-9-]', '', site['APPNAME'].lower())

        for lang in site['languages']:
            src = os.path.join(src_base, lang)
            dst = os.path.join(dst_base, f"{site['APPCODE']}-{lang}")
            site['LANG'] = lang
            copy_and_process_tree(src, dst, site)


if __name__ == '__main__':
    build_sites("peachjam.json", ".", ".")
