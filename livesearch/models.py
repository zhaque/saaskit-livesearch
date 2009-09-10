from django.db import models
import django_pipes as pipes
from django.conf import settings
from muaccounts.models import MUAccount


class GoogleSearch(pipes.Pipe):
    uri = "http://ajax.googleapis.com/ajax/services/search/web"
    cache_expiry = 3000000000

    @staticmethod
    def fetch(q):
        resp = GoogleSearch.objects.get({'v':1.0, 'q':q})

        if resp and hasattr(resp, "responseData") and hasattr(resp.responseData, "results"):
            return resp.responseData.results

class TwitterSearch(pipes.Pipe):
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 300000
    
    @staticmethod
    def fetch(q):
        resp = TwitterSearch.objects.get({'q':q})
        if resp and hasattr(resp, "results"):
            return resp.results

class BingImage(pipes.Pipe):
    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 3000000000

    @staticmethod
    def fetch(q, count, offset):
        resp = BingImage.objects.get({'Version':2.0, 'Query':q, 'AppId':settings.APPID,
                                       'Sources':'Image', 'Market': 'en-us', 'Image.Count': 10,
                                       'Image.Count':count, 'Image.Offset':offset,
                                       'JsonType':'callback', 'JsonCallbak':'SearchCompleted',

                                       })


        if resp and hasattr(resp, "SearchResponse") and hasattr(resp.SearchResponse, "Image") and hasattr(resp.SearchResponse.Image, 'Results'):

            return resp.SearchResponse.Image

    @staticmethod
    def fetch2(q):
        resp = BingSearch.objects.get({'v':1.0, 'q':q, 'AppId':settings.APPID,}, html=False)
        return resp

# BingMultiple searches spell + web
class BingMultiple(pipes.Pipe):
    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 3000000000

    @staticmethod
    def fetch(q):
        resp = BingMultiple.objects.get({
            'AppId':settings.APPID, 'Version':'2.2',
            'Market':'en-US', 'Query':q,
            'JsonType': 'raw',
            'web.count': '4',})

        if resp and hasattr(resp, "SearchResponse"):
            return resp.SearchResponse

# BingNews searches news
class BingNews(pipes.Pipe):
    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 30000000000

    @staticmethod
    def fetch(q):
        resp = BingNews.objects.get ({
            'AppId': settings.APPID, 'Version': '2.2',
            'Sources': 'News', 'Market': 'en-us',
            #'Options': 'EnableHighlighting',
            'News.Offset': '0', 'News.SortBy': 'Relevance',
            'JsonType': 'callback', 'Query': q,
            })

        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, "News"):
            return resp.SearchResponse.News

# BingNews searches InstantAnswer
class BingInstant(pipes.Pipe):
    """
    resp.InstantAnswer.Results[0].keys()
[u'Url', u'ClickThroughUrl', u'ContentType', u'InstantAnswerSpecificData', u'Title']
    """

    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 30000000000

    @staticmethod
    def fetch(q):
        resp = BingInstant.objects.get ({
            'AppId': settings.APPID, 'Version': '2.2',
            'Sources': 'News', 'Market': 'en-us',
            #'Options': 'EnableHighlighting',
            'Sources': 'InstantAnswer',
            'JsonType': 'callback', 'Query': q,
            })

        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'InstantAnswer') and hasattr(resp.SearchResponse.InstantAnswer, 'Results'):
            return resp.SearchResponse.InstantAnswer.Results

# BingNews searches news
class BingRelated(pipes.Pipe):
    """
    resp.RelatedSearch.Results[3].keys()
[u'Url', u'Title']
    """

    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 30000000000

    @staticmethod
    def fetch(q):
        resp = BingNews.objects.get ({
            'AppId': settings.APPID, 'Version': '2.2',
            'Market': 'en-us',
            #'Options': 'EnableHighlighting',
            'Sources': 'RelatedSearch',
            'JsonType': 'callback', 'Query': q,
            })

        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'RelatedSearch') and hasattr(resp.SearchResponse.RelatedSearch, 'Results'):
            return resp.SearchResponse.RelatedSearch.Results

# BingNews searches news
class BingWeb(pipes.Pipe):
    """
    resp.Web.Results[0].keys()
[u'Url', u'Title', u'DisplayUrl', u'Description', u'DateTime']

    """
    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 30000000000

    @staticmethod
    def fetch(q, offset):
        bing_options = {
                        'AppId': settings.APPID,
                        'Sources':'Web', 'Version': '2.0', 'Market':'en-us',
                        'Adult': 'Moderate',
                        'Web.Count': '10', 'Web.Offset': offset,
                        # 'Web.Options':'DisableHostCollapsing+DisableQueryAlterations',
                        'JsonType': 'raw', 'Query': q,
                        }
        resp = BingNews.objects.get ()


        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'Web') and hasattr(resp.SearchResponse.Web, 'Results'):
            return resp.SearchResponse.Web


    @staticmethod
    def fetch_with_options(q, offset, options):
        bing_options = {
                        'AppId': settings.APPID,
                        'Sources':'Web', 'Version': '2.0', 'Market':'en-us',
                        'Adult': 'Moderate',
                        'Web.Count': '10', 'Web.Offset': offset,
                        # 'Web.Options':'DisableHostCollapsing+DisableQueryAlterations',
                        'JsonType': 'raw', 'Query': q,
                        }
        bing_options.update(options)
        resp = BingNews.objects.get(bing_options)


        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'Web') and hasattr(resp.SearchResponse.Web, 'Results'):
            return resp.SearchResponse.Web



# BingNews searches news
class BingVideo(pipes.Pipe):
    """
    resp2.Video.keys()
[u'Total', u'Results', u'Offset']
    resp2.Video.Results[0].keys()
[u'Title', u'SourceTitle', u'StaticThumbnail', u'ClickThroughPageUrl', u'RunTime', u'PlayUrl']


    """
    uri = "http://api.bing.net/json.aspx"
    cache_expiry = 30000000000

    @staticmethod
    def fetch(q, count, offset):
        resp = BingNews.objects.get ({
            'AppId': settings.APPID, 'Version': '2.2',
            'Sources': 'Video', 'Market': 'en-us',
            #'Options': 'EnableHighlighting',
             'Video.Count': count, 'Video.Offset': offset,
            'JsonType': 'callback', 'Query': q,
            })

        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'Video'):
            return resp.SearchResponse.Video


def make_map(adict):
    """
    make a dict of 256 members who's value is maped to itself except the ones in a dict.
    """
    slash_map = {}
    for i in xrange(256):
        c = chr(i)
        slash_map[c] = c
    slash_map.update(adict)
    return slash_map

slash_map = make_map({'/': '%2f',
                      '?': '%3f',
                      '&': '%26',
                      ';': '%3b',
                      ':': '%3a',
                      '@': '%40',
                      ',': '%2c',
                      '$': '%24',
                      '=': '%3d',
                      '\x20': '%20',
                      '%': '%25',
                      '"': '%22',
                      '+': '%2b',
                      '#': '%23',
                      '*': '%2a',
                      '<': '%3c',
                      '>': '%3e',
                      '{': '%7b',
                      '}': '%7d',
                      '|': '%7c',
                      '[': '%5b',
                      ']': '%5d',
                      '^': '%5e',
                      '\\': '%5c',
                      '\x60': '%60',
                      })


class BossInlink(pipes.Pipe):
    inlink_url = "http://boss.yahooapis.com/ysearch/se_inlink/v1/"
    cache_expiry = 3000000000000

    @classmethod
    def fetch(cls, q):
        q = q.strip()
        site = ''.join(map(slash_map.__getitem__, q))
        cls.uri = "%s%s" % (cls.inlink_url, site)
        resp = cls.objects.get({
            'appid': settings.YAHOOID,
            'format': 'json',
            'count': '100',
            })

        if resp and hasattr(resp, 'ysearchresponse'):
            return resp.ysearchresponse



class BossPagedata(pipes.Pipe):
    pagedata_url = "http://boss.yahooapis.com/ysearch/se_pagedata/v1/"
    cache_expiry = 3000000

    @classmethod
    def fetch(cls, q):
        q = q.strip()
        q = ''.join(map(slash_map.__getitem__, q))
        cls.uri = "%s%s" % (cls.pagedata_url, q)
        resp = cls.objects.get({
            'appid': settings.YAHOOID,
            'format': 'json',
            'count': '100',
            })

        if resp and hasattr(resp, 'ysearchresponse'):
            return resp.ysearchresponse


class AdminSearchOption(models.Model):

    search_option_choices=(
                ('DisableLocationDetection', 'DisableLocationDetection'),
                ('EnableHighlighting', 'EnableHighlighting'),
                ('All', 'All'),
                ('None', 'None'),
            )
    adult_option_choices=(('Off', 'Off'), ('Moderate', 'Moderate'), ('Strict', 'Strict'), ('None', 'None'))
    web_search_choices=(
                        ('DisableHostCollapsing', 'DisableHostCollapsing'),
                        ('DisableQueryAlterations', 'DisableQueryAlterations'),
                        ('All', 'All'),
                        ('None', 'None'),
                        )
    video_search_choices=(
                            ('Date', 'Date'),
                            ('Relevance', 'Relevance'),
                            ('None', 'None'),
                          )
    search_option = models.CharField(max_length=30, choices=search_option_choices, default='None')
    adult_option = models.CharField(max_length = 8, choices=adult_option_choices, default='None')
    web_search = models.CharField(max_length=30, choices=web_search_choices, default = 'None')
    video_search = models.CharField(max_length=15, choices=video_search_choices, default='None')
    muaccount = models.OneToOneField(MUAccount, blank=True, null=True)
