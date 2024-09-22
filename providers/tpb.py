from bs4 import BeautifulSoup
import utils
import re


def Provider():
    from providers.providers import ProviderResult

    base = "https://tpirbay.site/search"
    page = 0

    # tbp randomizes attributes like id/class by inserting random spaces before/after the text
    def trim_attribute_text(input_string):
        pattern = r'(\w+)="([^"]*)"'

        return re.sub(
            pattern,
            lambda match: f'{match.group(1)}="{match.group(2).replace(" ", "")}"',
            input_string,
        )

    def build_url(query):
        return f"{base}/{utils.encode_uri_component(query)}/{page}/99/0"

    def increment_page():
        nonlocal page
        page += 1

    def parse_html(html):
        results = []
        soup = BeautifulSoup(trim_attribute_text(html), "html.parser")
        tr_elements = soup.select("#content #main-content #searchResult tr")
        for tr in tr_elements:
            # Parse the HTML content
            soup = BeautifulSoup(str(tr), "html.parser")

            # Find the <tr> element
            tr = soup.find("tr")

            if not tr:
                continue

            if "header" in (tr.attrs.get("class") or {}):
                continue

            main_div = tr.find("div", class_="detName")

            if not main_div:
                continue

            title = main_div.a.text.strip()

            magnet = tr.find_all("a")[3]["href"]

            numbers = [td.text for td in tr.find_all("td", align="right")]

            font_element = soup.find("font", class_="detDesc")
            pattern = r"Size\s+([\d.]+)\s*([KMGT]i?B)"
            size_match = re.search(pattern, font_element.text)
            size_text = "N/A"

            if size_match:
                size_text = size_match.group(1) + " " + size_match.group(2)

            results.append(
                {
                    "title": title,
                    "magnet": magnet,
                    "seeders": numbers[0],
                    "leechers": numbers[1],
                    "size": size_text,
                }
            )

        return results

    return ProviderResult(base, parse_html, build_url, increment_page)


tbp_provider = Provider()
