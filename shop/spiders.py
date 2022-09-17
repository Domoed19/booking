from decimal import Decimal

import scrapy

import requests
from django.conf import settings


class BookingSpider(scrapy.Spider):
    name = "mile.by"
    allowed_domains = ["https://mile.by/"]
    start_urls = ["https://mile.by/catalog/elektricheskiy-obogrev-doma-i-kvartiry/"]

    def parse(self, response, **kwargs):
        for product in response.css(".showcase-sorting-block .anons-wrap"):
            try:
                cost = product.css(".anons-wrap .anons-price-wrap span::text").get().strip()
                cost = Decimal(cost.replace(",", "."))
            except Exception:
                cost = 0

            file_name = None
            image_url = product.css(".anons-wrap .anons-foto::attr(src)").get()
            if image_url:
                r = requests.get(f"https://mile.by/{image_url}", allow_redirects=True)
                if r.status_code == 200:
                    file_name = image_url.split("/")[-1]
                    open(settings.MEDIA_ROOT / file_name, "wb").write(r.content)

            data = {
                "external_id": product.attrib.get(".anons-wrap .anons-sku"),
                "title": product.css(".anons-name a::text").get().strip(),
                "cost": cost,
                "link": f"https://mile.by/{product.css('.anons-wrap::attr(href)').get()}",
                "image": file_name
            }
            yield data

        next_page = response.css(".pagination-wrap .pagin-arrow:last-child::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
