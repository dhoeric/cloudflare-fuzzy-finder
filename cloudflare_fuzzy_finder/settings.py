import os
import sys

from os.path import expanduser

SEPARATOR = " - "
RECORD_TYPES = os.getenv('CF_RECORD_TYPES')
CACHE_EXPIRY_TIME = int(os.getenv('CF_FUZZ_CACHE_EXPIRY', 3600)) # Keep for 1 hour
CACHE_ENABLED = os.getenv('CF_FUZZ_USE_CACHE', True)
CACHE_PATH = '{}/{}'.format(
    expanduser("~"),
    '.cloudflare_fuzzy_finder.cache'
)

fzf_base = 'fzf-0.17.0'
is_64_bit = sys.maxsize > 2**32

if is_64_bit:
    arch = 'amd64'
else:
    arch = '386'

if sys.platform.startswith('linux'):
    system = 'linux'
elif sys.platform == 'darwin':
    system = 'darwin'
else:
    print('Currently only MAC OS and Linux are supported, exiting.')
    exit(1)

lib = '{}-{}_{}'.format(fzf_base, system, arch)

LIBRARY_PATH = '{}/libs/{}'.format(
    os.path.dirname(os.path.abspath(__file__)),
    lib
)
