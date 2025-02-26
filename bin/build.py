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
    """Copy localised versions of assets. Assets are localised by adding a site prefix, such as lawlibrary--foo.png.
    If that file doesn't exist, the original is copied to create it.
    """
    assets_dir = os.path.join(src, '.gitbook', 'assets')
    files = {entry.name: entry for entry in os.scandir(assets_dir) if entry.is_file()}

    prefix = f'{site["APPCODE"]}--'

    for fname, entry in files.items():
        if '--' not in fname:
            local_fname = prefix + fname
            if local_fname not in files:
                # create a localised copy
                shutil.copy(entry.path, os.path.join(assets_dir, local_fname))

    for fname, entry in files.items():
        if fname.startswith(prefix):
            shutil.copy(entry.path, os.path.join(dst, '.gitbook', 'assets', fname))


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
            site['APPCODE'] = site['APPNAME'].lower()

        for lang in site['languages']:
            src = os.path.join(src_base, lang)
            dst = os.path.join(dst_base, f"{site['APPCODE']}-{lang}")
            site['LANG'] = lang
            copy_and_process_tree(src, dst, site)


if __name__ == '__main__':
    build_sites("peachjam.json", ".", ".")
