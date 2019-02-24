from cloudflare_fuzzy_finder.cf_utils import prepare_searchable_records

example_records = [{
    'type': 'CNAME',
    'name': 'new.domain3.com',
    'content': 'somewhere.abcnew.com',
    'proxied': True,
    'account_id': 'demo',
    'zone_name': 'domain3.com'
}, {
    'type': 'A',
    'name': 'a.domain3.com',
    'content': '1.1.1.1',
    'proxied': True,
    'account_id': 'demo',
    'zone_name': 'domain3.com'
}, {
    'type': 'TXT',
    'name': 'domain3.com',
    'content': 'somewhere.abc.com',
    'proxied': False,
    'account_id': 'demo',
    'zone_name': 'domain3.com'
}]

def test_getting_records_by_types():
    searchable_records = prepare_searchable_records(
        example_records,
        ["CNAME"]
    )
    assert searchable_records == [
        'CNAME - new.domain3.com somewhere.abcnew.com (Proxied) - demo/domain3.com'
    ]
