[![Build Status](https://travis-ci.org/dhoeric/cloudflare-fuzzy-finder.svg?branch=master)](https://travis-ci.org/dhoeric/cloudflare-fuzzy-finder)

# CloudFlare Fuzzy Finder

`cloudflare-fuzzy-finder` aims at checking DNS record more easily. It will connect to CloudFlare's API and get all DNS records from your account, and allow to search on fuzzy finder. Once pressing <kbd>Enter</kbd> on highlighted record, it will popup to the CloudFlare website for you to manage the record on that domain.

[![asciicast](https://asciinema.org/a/FpRVqUplovllYfE2jFikhpwUK.svg)](https://asciinema.org/a/FpRVqUplovllYfE2jFikhpwUK?loop=1&autoplay=1&t=5&rows=32&speed=2)

It is inspired by [pmazurek/aws-fuzzy-finder](https://github.com/pmazurek/aws-fuzzy-finder) and built on top of [fzf](https://github.com/junegunn/fzf-bin/releases) binaries and [python-cloudflare](https://github.com/cloudflare/python-cloudflare).


## Installation

To install use the following command:

`pip install cloudflare-fuzzy-finder`

This package uses `cloudflare-python` to authenticate, so if you haven't used before,
you have to get the api key from [your profile](https://dash.cloudflare.com/profile) and put into following files like:

```
$ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
email = user@example.com
token = 00000000000000000000000000000000
certtoken = v1.0-...
extras =
```

More information on alternative ways of configuring your `CF_API_EMAIL`, `CF_API_KEY` and `CF_API_CERTKEY` variables can be found here: https://github.com/cloudflare/python-cloudflare#providing-cloudflare-username-and-api-key

## Settings

The loading time on records list highly dependent on the API calls to CloudFlare to fetch all the DNS records across the domain belongs to you.

The cache on DNS records is turn on by default and keep for 1 hour.

If you want to fine tune the duration on keeping the record locally, you can update by `CF_FUZZ_CACHE_EXPIRY`.

Or if you want to perform the search without using the cache, cau use `cf-fuzzy --no-cache`.

Or you can append this to your `~/.bashrc` to make the settings permamant:
```sh
export CF_FUZZ_USE_CACHE=true
export CF_FUZZ_CACHE_EXPIRY=3600 # in terms of seconds
export CF_RECORD_TYPES=cname,a
```
Remeber that every change to `~/.bashrc` requires you to re-load it: `source ~/.bashrc` or restart terminal.

## Usage

To run, use the following command:

`cf-fuzzy`

To search any records other than CNAME & A, use the following command:

`cf-fuzzy --record-types mx,txt`

## Cache

If you are managing lots of domains and downloading the data takes too long, you can use the built in cache. To enable it set the following variables in your `.bashrc`:
```
export CF_FUZZ_USE_CACHE=true
export CF_FUZZ_CACHE_EXPIRY=3600 # in terms of seconds
```

To invalidate cache and refresh data, run with `--no-cache` param
Cache will be stored as a file in `~/.cloudflare_fuzzy_finder.cache`.
