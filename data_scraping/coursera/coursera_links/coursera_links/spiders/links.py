import scrapy


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["coursera.org"]
    start_urls = ["https://www.coursera.org/directory/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {  # Shared dictionary for storing scraped data
            "courses": [],
            "degrees": [],
            "certificates": [],
            "specializations": [],
            "articles": [],
        }
        self.completed_sections = set()  # To track completed sections

    def parse(self, response):
        # Mapping sections to their URLs
        sections = {
            "courses": "courses",
            "degrees": "degrees",
            "certificates": "certificates",
            "specializations": "specializations",
            "articles?localeCode=en-US": "articles",
        }

        for section, key in sections.items():

            section_url = f"{self.start_urls[0]}{section}?page=1"
            if key =="articles":
                section_url = f"{self.start_urls[0]}{section}&page=1"

            yield scrapy.Request(
                url=section_url,
                meta={"key": key},
                callback=self.parse_section,
            )

    def parse_section(self, response):
        key = response.meta["key"]

        # Extract URLs for the current section
        urls = response.css("li.css-4s48ix a::attr(href)").getall()
        self.data[key].extend([response.urljoin(url) for url in urls])

        # Check for the next page
        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                meta={"key": key},
                callback=self.parse_section,
            )
        else:
            # Mark the section as completed
            self.completed_sections.add(key)

            # If all sections are done, yield the final data
            if len(self.completed_sections) == len(self.data):
                yield self.data[0]


