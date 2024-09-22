import requests
import config


class ProviderResult:
    """
    Providers can be implemented in any way that suits the structure/firewalls of the website.
    They however, should always return the results using this class.

    `parse_html` should always return a list of {seeders, leechers, title, magnet, size}
    """

    def __init__(self, base, parse_html, build_url, increment_page):
        self.base = base
        self.parse_html = parse_html
        self.build_url = build_url
        self.increment_page = increment_page


def get_provider_based_on_config(provider):
    if provider == config.PROVIDERS.get("TPB"):
        from providers.tpb import tbp_provider

        return tbp_provider
    raise NotImplementedError


def build_url_based_on_provider(query):
    provider = config.app_config.get_provider()
    return provider.build_url(query)


def get_results_page_from_query(query):
    r = requests.get(build_url_based_on_provider(query))
    return r.text


def get_list_from_query(query):
    provider = config.app_config.get_provider()
    html = get_results_page_from_query(query)
    return provider.parse_html(html)


def next_page():
    provider = config.app_config.get_provider()
    provider.increment_page()
