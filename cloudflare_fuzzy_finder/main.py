import subprocess
import click
import shelve
import time
import sys
import webbrowser

from .cf_utils import (
    get_dns_records,
    prepare_searchable_records
)
from .settings import (
    SEPARATOR,
    LIBRARY_PATH,
    RECORD_TYPES,
    CACHE_PATH,
    CACHE_EXPIRY_TIME,
    CACHE_ENABLED
)


@click.command()
@click.option('--record-types', 'record_filter', default='cname,a,aaaa', help="Filter by record type (default: cname,a,aaaa)")
@click.option('--no-cache', flag_value=True, help="Ignore and invalidate cache")
def entrypoint(no_cache, record_filter):

    try:
        cache = None
        cache = shelve.open(CACHE_PATH)
        data = cache.get('fuzzy_finder_data')
        if CACHE_ENABLED and data and data.get('expiry') >= time.time() and not no_cache:
            cloudflare_records = data['cloudflare_records']
        else:
            cloudflare_records = get_dns_records()
            if CACHE_ENABLED:
                cache['fuzzy_finder_data'] = {
                    'cloudflare_records': cloudflare_records,
                    'expiry': time.time() + CACHE_EXPIRY_TIME
                }
        cache.close()
    except Exception as e:
        print('Exception occured while getting cache, getting instances from AWS api: %s' % e)
        if cache:
            cache.close()
        cloudflare_records = get_dns_records()

    record_types = RECORD_TYPES or record_filter
    record_types = [r.upper() for r in record_types.split(",")]

    searchable_records = prepare_searchable_records(
        cloudflare_records,
        record_types
    )

    fuzzysearch_bash_command = 'echo -e "{}" | {}'.format(
        "\n".join(searchable_records),
        LIBRARY_PATH
    )

    chosen_record = choice(fuzzysearch_bash_command)

    url = "https://dash.cloudflare.com/{}/dns".format(chosen_record)
    print("Opening {} ...".format(url))
    webbrowser.open(url)


def choice(fuzzysearch_bash_command):
    try:
        choice = subprocess.check_output(
            fuzzysearch_bash_command,
            shell=True,
            executable='/bin/bash'
        ).decode(encoding='UTF-8')
    except subprocess.CalledProcessError:
        exit(1)

    return choice.split(SEPARATOR)[-1].rstrip()


if __name__ == '__main__':
    entrypoint()
