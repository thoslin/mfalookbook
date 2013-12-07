from scrapy import log
from scrapy.dupefilter import BaseDupeFilter
from lookbook.models import Session, Post


class DBRDupeFilter(BaseDupeFilter):
    """Database Records duplicates filter"""

    def __init__(self):
        self.session = Session()

    def request_seen(self, request):
        # Strip "?limit=500" we added in spider rules
        record = self.session.query(Post).filter_by(permalink=request.url[:-10]).first()
        if record:
            return True

    def close(self, reason):
        self.session.close()

    def log(self, request, spider):
        fmt = "Filtered duplicate request: %(request)s - no more duplicates will be shown (see DUPEFILTER_CLASS)"
        log.msg(format=fmt, request=request, level=log.DEBUG, spider=spider)