import scrapy
from scrappingecom.items import FundrazrItem


class Fundrazr(scrapy.Spider):
    name = "fundrazr"

    url_default = "https://fundrazr.com/find?%s"
    query = "category="
    css_topic = "a.campaign-link::attr(href)"

    url_base = url_default % query
    start_urls = [url_base]

    nb_pages = 3
    for i in range(2, 2+nb_pages):
        start_urls.append(url_base + "&page="+str(i))

    def __init__(self, category=None, *args, **kwargs):
        self.query = self.query + category
        super(Fundrazr, self).__init__(*args, **kwargs)

    def parse(self, response):
        # parsing topics
        topics = response.css(self.css_topic).getall()
        for topic in topics:
            topic = "https:{}".format(topic)
            yield scrapy.Request(url=topic, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = FundrazrItem()

        # Getting Campaign Title
        item['campaignTitle'] = response.xpath("//div[contains(@id, 'campaign-title')]/descendant::text()").extract()[0].strip()

        # Getting Amount Raised
        item['amountRaised'] = response.xpath(
            "//span[contains(@class, 'stat')]/span[contains(@class, 'amount-raised')]/descendant::text()").extract()

        # Goal
        item['goal'] = " ".join(response.xpath(
            "//div[contains(@class, 'stats-primary with-goal')]//span[contains(@class, 'stats-label hidden-phone')]/text()").extract()).strip()

        # Currency Type (US Dollar Etc)
        item['currencyType'] = response.xpath("//div[contains(@class, 'stats-primary with-goal')]/@title").extract()

        # Campaign End (Month year etc)
        item['endDate'] = "".join(response.xpath(
            "//div[contains(@id, 'campaign-stats')]//span[contains(@class,'stats-label hidden-phone')]/span[@class='nowrap']/text()").extract()).strip()

        # Number of contributors
        item['numberContributors'] = response.xpath(
            "//div[contains(@class, 'stats-secondary with-goal')]//span[contains(@class, 'donation-count stat')]/text()").extract()

        # Getting Story
        story_list = response.xpath("//div[contains(@id, 'full-story')]/descendant::text()").extract()
        story_list = [x.strip() for x in story_list if len(x.strip()) > 0]
        item['story'] = " ".join(story_list)

        # Url (The link to the page)
        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        yield item



