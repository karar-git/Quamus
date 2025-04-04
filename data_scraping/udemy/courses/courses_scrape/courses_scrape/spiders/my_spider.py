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
import os
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
        #if response.status == 429:
        #    yield from self.handle_too_many_requests(response)
        #    return

        # Parse course IDs from API response
        data = response.json()
        label_id = response.meta['label_id']
        page = response.meta['page']

        for course in data.get('unit', {}).get('items', []):
            course_id = course.get('id')
            # Fetch course details
            details_url = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components=add_to_cart,curriculum_context,incentives,slider_menu"
            yield scrapy.Request(details_url, callback=self.parse_course_details, meta={'course_id': course_id})

            # Fetch course reviews
            #reviews_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/reviews/?courseId={course_id}&page=1&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html,created_formatted_with_time_since&fields[user]=@min,image_50x50,initials,public_display_name,tracking_id&fields[course_review_response]=@min,user,content_html,created_formatted_with_time_since"
            #yield scrapy.Request(reviews_url, callback=self.parse_reviews, meta={'course_id': course_id, 'reviews_fetched': 0})

        # Handle pagination for course IDs
        total_pages = data.get('pagination', {}).get('total_page', 1)
        if page < total_pages:
            next_page = page + 1
            next_url = f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={next_page}&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&label_id={label_id}&source_page=topic_page&locale=en_US&currency=usd&navigation_locale=en&skip_price=true&sos=pl&fl=lbl"
            yield scrapy.Request(next_url, callback=self.parse_course_ids, meta={'label_id': label_id, 'page': next_page})



    #def parse_course_details(self, response):
    #    # Parse course details from API response
    #    data = response.json()
    #    course_id = response.meta['course_id']

    #    # Check for curriculum content; if not found, log the course id and do not yield data
    #    curriculum_content = data.get('curriculum_context', {}).get('data', {})
    #    if not curriculum_content:
    #        self.urls_without_circc_1(response.url)
    #        return

    #    yield {
    #        'course_id': course_id,
    #        'course_url': response.url,
    #        'add_to_cart': data.get('add_to_cart', {}).get('buyables', []),
    #        'curriculum_content': curriculum_content,
    #        'incentives': data.get('incentives', {}),
    #        'slider_menu': data.get('slider_menu', {})
    #    }

    #def parse_desc(self, url):


    def parse_course_details(self, response):
        data = response.json()
        course_id = response.meta['course_id']

        curriculum_content = data.get('curriculum_context', {}).get('data', {})
        if not curriculum_content:
            self.urls_without_circc_1(response.url)
            return

        course_data = {
            'course_id': course_id,
            'course_url': response.url,  # This is the main course URL
            'add_to_cart': data.get('add_to_cart', {}).get('buyables', []),
            'curriculum_content': curriculum_content,
            'incentives': data.get('incentives', {}),
            'slider_menu': data.get('slider_menu', {})
        }

        yield scrapy.Request(
            url=f'https://www.udemy.com/api-2.0/courses/{course_id}?fields[course]=description',
            callback=self.parse_description,
            meta={'course_data': course_data, 'retry_count': 0}  # Initialize retry count
        )

    def parse_description(self, response):
        if response.status == 429:
            # Pass course_data to the retry handler
            yield from self.handle_too_many_requests(response.meta['course_data'], response)
            return
        data = response.json()
        course_data = response.meta['course_data']
        course_data['description'] = data.get('description', '')
        yield course_data

    def handle_too_many_requests(self, course_data, response):
        retry_count = response.meta.get('retry_count', 0)
        if retry_count >= 3:
            # Log the MAIN course URL (not the API endpoint)
            self.logger.error(f"Failed to fetch description for: {course_data['course_url']}")
            self.log_failed_request(course_data['course_id'])  # Log to file
            return

        time.sleep(10)
        retry_count += 1
        yield scrapy.Request(
            response.url,
            callback=self.parse_description,
            meta={**response.meta, 'retry_count': retry_count},
            dont_filter=True
        )

    #def parse_course_details(self, response):
    #    data = response.json()
    #    course_id = response.meta['course_id']

    #    curriculum_content = data.get('curriculum_context', {}).get('data', {})
    #    if not curriculum_content:
    #        self.urls_without_circc_1(response.url)
    #        return

    #    course_data = {
    #        'course_id': course_id,
    #        'course_url': response.url,
    #        'add_to_cart': data.get('add_to_cart', {}).get('buyables', []),
    #        'curriculum_content': curriculum_content,
    #        'incentives': data.get('incentives', {}),
    #        'slider_menu': data.get('slider_menu', {})
    #    }

    #    # Now yield a new request to get the description
    #    yield scrapy.Request(
    #        url=f'https://www.udemy.com/api-2.0/courses/{course_id}?fields[course]=description',
    #        callback=self.parse_description,
    #        meta={'course_data': course_data, 'response': response}
    #    )

    #def parse_description(self, response):
    #    if response.status == 429:
    #        yield from self.handle_too_many_requests(response.meta['response'])
    #        return
    #    data = response.json()
    #    description = data.get('description', '')
    #    course_data = response.meta['course_data']
    #    course_data['description'] = description
    #    yield course_data

    #def handle_too_many_requests(self, response):
    #    """
    #    Handle 429 Too Many Requests by waiting and retrying.
    #    """
    #    retry_count = response.meta.get('retry_count', 0)
    #    if retry_count >= 3:  # Stop retrying after 3 attempts
    #        self.logger.error(f"Gave up on {response.url} after too many retries.")
    #        self.log_failed_request(response.url)
    #        return

    #    # Wait for 10 seconds before retrying
    #    #self.logger.warning(f"Too many requests (429). Retrying {response.url} after waiting 10 seconds...")
    #    time.sleep(10)

    #    # Retry the request with an incremented retry count
    #    retry_count += 1
    #    yield scrapy.Request(
    #        response.url,
    #        callback=response.request.callback,
    #        meta={**response.meta, 'retry_count': retry_count},  # Pass updated meta
    #        dont_filter=True  # Ensure request is not filtered
    #    )

    def log_failed_request(self, url):
        file_name = "didnt_get_parsed.json"
        # Initialize an empty list or load existing data
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    failed_urls = json.load(f)
                except json.JSONDecodeError:
                    failed_urls = []
        else:
            failed_urls = []
        
        # Append the new URL if it is not already in the list
        if url not in failed_urls:
            failed_urls.append(url)
        
        # Write the updated list back to the file
        with open(file_name, "w") as f:
            json.dump(failed_urls, f, indent=4)

    def urls_without_circc_1(self, url):
        file_name = "urls_without_circc.json"
        # Initialize an empty list or load existing data
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    failed_urls = json.load(f)
                except json.JSONDecodeError:
                    failed_urls = []
        else:
            failed_urls = []
        
        # Append the new URL if it is not already in the list
        if url not in failed_urls:
            failed_urls.append(url)
        
        # Write the updated list back to the file
        with open(file_name, "w") as f:
            json.dump(failed_urls, f, indent=4)

    #def parse_reviews(self, response):
    #    if response.status == 429:
    #        yield from self.handle_too_many_requests(response)
    #        return

    #    # Parse reviews for a course
    #    data = response.json()
    #    course_id = response.meta['course_id']
    #    reviews_fetched = response.meta['reviews_fetched']

    #    # Extract reviews from the current page
    #    reviews = data.get('results', [])
    #    for review in reviews:
    #        yield {
    #            'course_id': course_id,
    #            'review': review
    #        }

    #    # Stop fetching after collecting 30 reviews
    #    reviews_fetched += len(reviews)
    #    if reviews_fetched >= 30:
    #        return

    #    # Fetch the next page of reviews if available
    #    next_url = data.get('next')
    #    if next_url:
    #        yield scrapy.Request(next_url, callback=self.parse_reviews, meta={
    #            'course_id': course_id,
    #            'reviews_fetched': reviews_fetched
    #        })

