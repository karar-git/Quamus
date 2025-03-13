#import scrapy
#import json
#from tqdm import tqdm  # Import tqdm for the progress bar
#
#
#class UdemySpider(scrapy.Spider):
#    name = "udemy"
#    allowed_domains = ["udemy.com"]
#
#    def __init__(self):
#        # Load label IDs from JSON file
#        with open("../../../../labels_extraction/labels_with_ids.json", "r") as file:
#            data = json.load(file)
#        self.label_ids = list(data.values())  # Extract label IDs as a list
#        self.label_progress = tqdm(total=len(self.label_ids), desc="Processing Labels", unit="label")
#
#    def start_requests(self):
#        # Generate initial requests for each label ID
#        for label_id in self.label_ids:
#            url = f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?p=1&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&label_id={label_id}&source_page=topic_page&locale=en_US&currency=usd&navigation_locale=en&skip_price=true&sos=pl&fl=lbl"
#            self.label_progress.update(1)  # Update the progress bar for each label
#            yield scrapy.Request(url, callback=self.parse_course_ids, meta={'label_id': label_id, 'page': 1})
#
#    def parse_course_ids(self, response):
#        # Parse course IDs from API response
#        data = response.json()
#        label_id = response.meta['label_id']
#        page = response.meta['page']
#
#        for course in data.get('unit', {}).get('items', []):
#            course_id = course.get('id')
#            # Fetch course details
#            details_url = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components=add_to_cart,curriculum_context,incentives"
#            yield scrapy.Request(details_url, callback=self.parse_course_details, meta={'course_id': course_id})
#
#            # Fetch course reviews
#            reviews_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/reviews/?courseId={course_id}&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials,public_display_name,tracking_id&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since"
#            yield scrapy.Request(reviews_url, callback=self.parse_reviews, meta={'course_id': course_id, 'reviews_fetched': 0})
#
#        # Handle pagination for course IDs
#        total_pages = data.get('pagination', {}).get('total_page', 1)
#        if page < total_pages:
#            next_page = page + 1
#            next_url = f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={next_page}&page_size=60&label_id={label_id}&locale=en_US&currency=usd&skip_price=true"
#            yield scrapy.Request(next_url, callback=self.parse_course_ids, meta={'label_id': label_id, 'page': next_page})
#
#    def parse_course_details(self, response):
#        # Parse course details from API response
#        data = response.json()
#        course_id = response.meta['course_id']
#
#        yield {
#            'course_id': course_id,
#            'add_to_cart': data.get('add_to_cart', {}).get('buyables', []),
#            'curriculum_content': data.get('curriculum_context', {}).get('data', {}),
#            'incentives': data.get('incentives', {}),
#        }
#
#    def parse_reviews(self, response):
#        # Parse reviews for a course
#        data = response.json()
#        course_id = response.meta['course_id']
#        reviews_fetched = response.meta['reviews_fetched']
#
#        # Extract reviews from the current page
#        reviews = data.get('results', [])
#        for review in reviews:
#            yield {
#                'course_id': course_id,
#                'review': review
#            }
#
#        # Stop fetching after collecting 30 reviews
#        reviews_fetched += len(reviews)
#        if reviews_fetched >= 30:
#            return
#
#        # Fetch the next page of reviews if available
#        next_url = data.get('next')
#        if next_url:
#            yield scrapy.Request(next_url, callback=self.parse_reviews, meta={
#                'course_id': course_id,
#                'reviews_fetched': reviews_fetched
#            })
#
#    def close(self, reason):
#        # Close the progress bar when the spider finishes
#        self.label_progress.close()
#






import scrapy
import json
from tqdm import tqdm  # Import tqdm for the progress bar
import time  # For implementing delays


class UdemySpider(scrapy.Spider):
    name = "udemy"
    allowed_domains = ["udemy.com"]

    def __init__(self):
        # Load label IDs from JSON file
        with open("../../../../labels_extraction/labels_with_ids.json", "r") as file:
            data = json.load(file)
        self.label_ids = list(data.values())  # Extract label IDs as a list
        self.label_progress = tqdm(total=len(self.label_ids), desc="Processing Labels", unit="label")

    def start_requests(self):
        # Generate initial requests for each label ID
        for label_id in self.label_ids:
            url = f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?p=1&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&label_id={label_id}&source_page=topic_page&locale=en_US&currency=usd&navigation_locale=en&skip_price=true&sos=pl&fl=lbl"
            self.label_progress.update(1)  # Update the progress bar for each label
            yield scrapy.Request(
                url,
                callback=self.parse_course_ids,
                meta={'label_id': label_id, 'page': 1, 'retry_count': 0},  # Add retry metadata
                dont_filter=True
            )

    def parse_course_ids(self, response):
        if response.status == 429:
            yield from self.handle_too_many_requests(response)
            return

        # Parse course IDs from API response
        data = response.json()
        label_id = response.meta['label_id']
        page = response.meta['page']

        for course in data.get('unit', {}).get('items', []):
            course_id = course.get('id')
            # Fetch course details
            details_url = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components=add_to_cart,curriculum_context,incentives"
            yield scrapy.Request(details_url, callback=self.parse_course_details, meta={'course_id': course_id})

            # Fetch course reviews
            reviews_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/reviews/?courseId={course_id}&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials,public_display_name,tracking_id&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since"
            yield scrapy.Request(reviews_url, callback=self.parse_reviews, meta={'course_id': course_id, 'reviews_fetched': 0})

        # Handle pagination for course IDs
        total_pages = data.get('pagination', {}).get('total_page', 1)
        if page < total_pages:
            next_page = page + 1
            next_url = f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={next_page}&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&label_id={label_id}&source_page=topic_page&locale=en_US&currency=usd&navigation_locale=en&skip_price=true&sos=pl&fl=lbl"
            yield scrapy.Request(next_url, callback=self.parse_course_ids, meta={'label_id': label_id, 'page': next_page})

    def parse_course_details(self, response):
        # Parse course details from API response
        data = response.json()
        course_id = response.meta['course_id']

        yield {
            'course_id': course_id,
            'add_to_cart': data.get('add_to_cart', {}).get('buyables', []),
            'curriculum_content': data.get('curriculum_context', {}).get('data', {}),
            'incentives': data.get('incentives', {}),
        }

    def parse_reviews(self, response):
        if response.status == 429:
            yield from self.handle_too_many_requests(response)
            return

        # Parse reviews for a course
        data = response.json()
        course_id = response.meta['course_id']
        reviews_fetched = response.meta['reviews_fetched']

        # Extract reviews from the current page
        reviews = data.get('results', [])
        for review in reviews:
            yield {
                'course_id': course_id,
                'review': review
            }

        # Stop fetching after collecting 30 reviews
        reviews_fetched += len(reviews)
        if reviews_fetched >= 30:
            return

        # Fetch the next page of reviews if available
        next_url = data.get('next')
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse_reviews, meta={
                'course_id': course_id,
                'reviews_fetched': reviews_fetched
            })

    def handle_too_many_requests(self, response):
        """
        Handle 429 Too Many Requests by waiting and retrying.
        """
        retry_count = response.meta.get('retry_count', 0)
        if retry_count >= 3:  # Stop retrying after 3 attempts
            self.logger.error(f"Gave up on {response.url} after too many retries.")
            return

        # Wait for 10 seconds before retrying
        self.logger.warning(f"Too many requests (429). Retrying {response.url} after waiting 10 seconds...")
        time.sleep(10)

        # Retry the request with an incremented retry count
        retry_count += 1
        yield scrapy.Request(
            response.url,
            callback=response.request.callback,
            meta={**response.meta, 'retry_count': retry_count},  # Pass updated meta
            dont_filter=True  # Ensure request is not filtered
        )

