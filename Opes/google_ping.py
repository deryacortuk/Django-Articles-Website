from django.contrib.sitemaps import ping_google
import requests
import logging

logger = logging.getLogger(__name__)

class SpiderNotify():
    @staticmethod
    def __google_notify():
        try:
            ping_google('/sitemap.xml')
        except Exception as e:
            logger.error(e)
            
    @staticmethod
    def notify(url):
        SpiderNotify.__google_notify()