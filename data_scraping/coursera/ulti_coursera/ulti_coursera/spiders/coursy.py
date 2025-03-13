import scrapy
import re
import json
from scrapy_playwright.page import PageMethod
import pyprind

class SimpleCourseraSpider(scrapy.Spider):
    name = "course"
    
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    def start_requests(self):
        with open("../../../coursera_links.json", "r") as f:
            data = json.load(f)
            courses=data.get("courses", [])
        with open("output.json", "r") as f:
            collected_data= json.load(f)

        def normalize_url(url):
            return re.sub(r"/projects/", "/learn/", url)

        collected_urls = {normalize_url(entry["url"]) for entry in collected_data}

        # Filter courses to include only those not already in collected_data
        filtered_courses = [url for url in courses if url not in collected_urls]
        print(len(filtered_courses))

        pbar = pyprind.ProgBar(len(filtered_courses))
        for url in filtered_courses:
            pbar.update()
            yield scrapy.Request(
                url=url,
                callback=self.parse_course,
                meta={"playwright": True, "playwright_include_page": True}
            )


    async def parse_course(self, response):
        page = response.meta["playwright_page"]
        item = {"url": response.url}

        if "coursera.org/learn" in response.url:
            item["type"] = "course"
        elif "coursera.org/projects" in response.url:
            item["type"] = "project"
        else:
            item["type"] = "unknown"

        try:
            # Click all expand buttons
            #await page.evaluate("window.scrollBy(0, document.body.scrollHeight/5)")
            #await page.wait_for_timeout(1000)

            #await page.wait_for_selector('button[data-track-component="overview_skills_toggle"]', state = "attached")
            button_skill = page.locator('button[data-track-component="overview_skills_toggle"]')
            if await button_skill.count() > 0 :
                await button_skill.click()
            
            buttons = page.locator('button.cds-149.cds-button-disableElevation.cds-button-ghost.css-bkcyb')

            for i in range(await buttons.count()):
                await buttons.nth(i).click()
            
            modules_expand_buttons = page.locator('button.cds-149.cds-ShowMoreContainer-ctaButton.cds-button-disableElevation.cds-button-ghost.css-1mtfnx6')

            for i in range(await buttons.count()):
                await modules_expand_buttons.nth(i).click()

            # Wait for core content
            
            # Get updated HTML
            content = await page.content()

            #with open("my.html", "w") as f:
            #    f.write(content)

            updated_response = scrapy.http.HtmlResponse(url=response.url, body=content, encoding='utf-8')

            # Extract core data
            if item["type"] == "project":
                item["modules"] ={
                        #"Tasks": updated_response.css('h3 ::text').get("NaN").strip(),
                        "Tasks": response.css("li.css-1ifkymy div.css-g2bbpm ::text").getall() or ["NaN"], # NaN will be for the unguided projects
                        "Recommended Experiecne":". ".join(response.css("div.css-6fogz8 div.rc-CML.unified-CML div.css-g2bbpm ::text").getall() or ["NaN"])
                        #"images":
                    } 
                    #note that it is a course modules will be list of dictionaries in spite of projects 



            else:
                item["modules"] =  [
                    {
                        "title": mod.css('h3 ::text').get("NaN").strip(),
                        "description": mod.css('p.css-4s48ix ::text').get("NaN").strip(),
                        "over_view": {f"{content_type}": number for content_type, number in zip([contents.split()[1] for contents in mod.css("p.css-kqm948 ::text").getall()],[contents.split()[0] for contents in mod.css("p.css-kqm948 ::text").getall()])}
                        #details = {f"{content_type}": {f"{title}": length for title, length in zip()} for content_type in modules["over_view"][0] }
                        #the details will be good addition for very personilized coursers or learning material in general, for example the one can take 2 videos from here and 3 from another course or source.
                    } 
                    for mod in updated_response.css('div.css-fndret div[data-testid="accordion-item"]')
                ]


            time = next((elem for elem in response.css('div.css-fk6qfz ::text').getall() if re.search(r'\d+', elem) and ('hour' in elem or 'minute' in elem)),None)

            # If no time is found in the first class, check for "Flexible schedule" in css-fw9ih3
            if not time or "Flexible schedule" in time:
                time = next(
                    (elem for elem in response.css('div.css-fw9ih3 ::text').getall() if re.search(r'\d+', elem) and ('hour' in elem or 'minute' in elem)),
                    "mixed"
                )
            
            # Extract the numeric part of the time
            if time and isinstance(time, str):
                time = re.search(r'\d+', time)
                if time:
                    time = time.group(0)  
            if not time:
                time = "NaN"

            filtered = [elem for elem in response.css("div.css-fk6qfz ::text").getall() if "level" in elem.lower()]

            # If there's at least one element that satisfies the condition
            if filtered:
                # Get the first word of the first element that matches
                level = filtered[0].split()[0]  # Get the first word
            else:
                # If no element matches, assign 'mixed'
                level = "mixed"
            item.update({
                "course_name":updated_response.css("[data-e2e='hero-title']::text").get(default = "NaN"),
                "course_url": response.url,
                "organization": updated_response.css("a.cds-119.cds-113.cds-115.css-5xxql1.cds-142 span.css-6ecy9b::text").getall() or ["NaN"],

                "instructor":updated_response.css("a.cds-119.cds-113.cds-115.css-1famv09.cds-142 span.css-6ecy9b::text").get(default = "NaN"),

                "rating": updated_response.css('div.css-h1jogs::text').get(default = "No rating"),
                "nu_reviews" : updated_response.css("p.css-vac8rf::text").get(default="0").split()[0][1:],
                "description":"".join(updated_response.css('div.content[aria-hidden="true"] ::text').getall()).replace("\n","") or ["NaN"],

                "skills": updated_response.css("ul.css-yk0mzy li.css-0 span[aria-hidden='true'] ::text").getall() or updated_response.css("ul.css-yk0mzy li.css-0 ::text").getall() or ["NaN"],
                "level": level,
                "Duration": time
            })

            # Process reviews
            await page.goto(f"{response.url}/reviews")

            reviews_html = await page.content()
            reviews_response = scrapy.http.HtmlResponse(url=response.url, body=reviews_html, encoding='utf-8')
            
            item["reviews"] = [{
                "comment": rev.css('div.reviewText ::text').get("").strip(),
                "stars": len(rev.css('span._13xsef79 svg[style*="fill:#F2D049"]').getall())
            } for rev in reviews_response.css('div.cds-9.review.review-text.review-page-review.m-b-2.css-0.cds-10')]

        finally:
            await page.close()
            yield item

