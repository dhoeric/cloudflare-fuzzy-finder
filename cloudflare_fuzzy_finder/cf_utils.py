import CloudFlare
import time

def get_domains():
    cf = CloudFlare.CloudFlare(raw=True)
    page_number = 0
    zones = []
    while True:
        page_number += 1
        raw_results = cf.zones.get(params = {'per_page': 200, 'page': page_number})
        zones += raw_results['result']

        total_pages = raw_results['result_info']['total_pages']
        if page_number == total_pages:
            break

    return zones


def get_dns_records():
    cf = CloudFlare.CloudFlare(raw=True)

    zones = get_domains()
    records = []

    for zone in zones:
        zone_id = zone['id']

        page_number = 0
        while True:
            page_number += 1
            raw_results = cf.zones.dns_records.get(zone_id, params={'per_page': 200, 'page': page_number})

            # Add account_id for opening browser
            result = map(lambda item: dict(item, account_id=zone['account']['id']), raw_results['result'])

            # Filter by record type
            records += filter(lambda x: x['type'] in ["CNAME", "A"], result)
            records += result

            total_pages = raw_results['result_info']['total_pages']
            if page_number == total_pages:
                break

    return records


def prepare_searchable_records(records, filter_types=['MX', 'CNAME', 'A']):
    searchable_records = []

    for record in records:
        if record['type'] not in filter_types:
            continue

        proxied_text = "Non-proxied"
        if record['proxied']:
            proxied_text = "Proxied"

        formatted_records = "{} - {} {} ({}) - {}/{}".format(
            record['type'],
            record['name'],
            record['content'],
            proxied_text,
            record['account_id'],
            record['zone_name']
        )
        searchable_records.append(formatted_records)

    return searchable_records
