# Peachjam User Guides

This repo contains the user documentation for [Peach Jam](https://github.com/laws-africa/peachjam) Legal Information
websites.

The master documentation is edited on GitBook and then committed to this repo. The various website-specific variants
of the documentation is then built automatically using GitHub actions.

## Master documentation

* [eng](eng/) - Master English user guide
* [fra](fra/) - Master French user guide

## Website variants

The website variants are configured in [peachjam.json](peachjam.json). Multiple language variants may be built for
each website.

## How variants are built

Variants are built using GitHub actions. The build script is [bin/build.py](bin/build.py) and the process is configured
in [.github/workflows/build.yml](.github/workflows/build.yml).

We use the Python Jinja2 package to pre-process the Markdown files, replacing variables and allowing basic control
flow such as `if` statements. The built outputs are committed to the repo and Gitbook builds them into the final
user-facing content.

### Variables

Use the syntax `%%VARIABLE%%` for a variable. Variables are defined in the `peachjam.json` file. Variables can be used
anywhere in the Markdown files, including in headings and links.

For example, `%%APPNAME%%` will be replaced with the application website name.

The `%%` escape is used rather than the Jinja default of `{{` and `}}` so as not to conflict with the variable syntax
used by Gitbook.

### Control statements

Use `(%` and `%)` for control statements, such as `(% if APPNAME == "LawLibrary" %)xx(% else %)yy(% endif %)`.

The `(%` and `%)` escapes are used rather than the Jinja default of `{%` and `%}` so as not to conflict with the
syntax used by Gitbook.

Consult the [Jinja template documentation](https://jinja.palletsprojects.com/en/stable/templates/) for more details.

## Localised image variants

The base images are stored in the `.gitbook/assets` directory. Localised variants of each image are stored in the
`_site-images` directory.

For example, to localise `search 1.png` for TanzLII, put the localised image (with exactly the same filename) at:

`_site-images/tanzlii/eng/search 1.png`

During the build process, that image will be copied to `.gitbook/assets/tanzlii--search 1.png` for TanzLII, and GitBook
will use that image for the TanzLII documentation.

### Override precedence

For each source asset `<name>` during a site build:

1. `_site-images/<appcode>/<lang>/<name>` (preferred)
2. `<lang>/.gitbook/assets/<name>` (default image)
