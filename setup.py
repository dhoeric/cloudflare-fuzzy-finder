from setuptools import setup

with open("README.md") as f:
    long_description = "\n".join(f.readlines())

setup(
    name='cloudflare-fuzzy-finder',
    version='0.1.1',
    url='https://github.com/dhoeric/cloudflare-fuzzy-finder',
    download_url='https://github.com/dhoeric/aws-fuzzy-finder/tarball/v0.1.1',
    author='Eric Ho',
    author_email='dho.eric@gmail.com',
    description='Find cloudflare DNS records using fuzzy search.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['cloudflare', 'fuzzy', 'dns'],
    packages=['cloudflare_fuzzy_finder'],
    package_data={'': [
        'libs/fzf-0.17.0-linux_386',
        'libs/fzf-0.17.0-linux_amd64',
        'libs/fzf-0.17.0-darwin_386',
        'libs/fzf-0.17.0-darwin_amd64',
    ]},
    install_requires=[
        'click==6.6',
		'cloudflare==2.1.0'
    ],
    entry_points=dict(
        console_scripts=[
            'cf-fuzzy = cloudflare_fuzzy_finder.main:entrypoint',
        ]
    )
)
