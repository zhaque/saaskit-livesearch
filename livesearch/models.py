from django.db import models
import django_pipes as pipes
from django.conf import settings
from django.contrib.auth.models import User
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
    def fetch_with_options(q, offset, options):
        bing_options = {'Version':2.0, 'Query':q, 'AppId':settings.APPID,
                        'Sources':'Image', 'Market': 'en-us',
                        'Image.Count':'10', 'Image.Offset':offset,
                        'JsonType':'callback', 'JsonCallbak':'SearchCompleted',}
        bing_options.update(options)
        resp = BingImage.objects.get(bing_options)

        if resp and hasattr(resp, "SearchResponse") and hasattr(resp.SearchResponse, "Image") and hasattr(resp.SearchResponse.Image, 'Results'):
            return resp.SearchResponse.Image

    @staticmethod
    def fetch(q, count, offset):
        return BingImage.fetch_with_options(q, offset, {})
        
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
    def fetch_with_options(q, offset, options):
        bing_options = {
            'AppId': settings.APPID, 'Version': '2.2',
            'Sources': 'News', 'Market': 'en-us',
            #'Options': 'EnableHighlighting',
            'News.Offset': offset, 'News.SortBy': 'Relevance',
            'JsonType': 'callback', 'Query': q,
        }
        bing_options.update(options)
        resp = BingNews.objects.get(bing_options)

        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, "News"):
            return resp.SearchResponse.News

    @staticmethod
    def fetch(q, offset):
        return BingNews.fetch_with_options(q, offset, {})

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
        resp = BingWeb.objects.get(bing_options)


        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'Web') and hasattr(resp.SearchResponse.Web, 'Results'):
            return resp.SearchResponse.Web

    @staticmethod
    def fetch(q, offset):
        return BingWeb.fetch_with_options(q, offset, {})



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
    def fetch_with_options(q, offset, options):
        bing_options = {
            'AppId': settings.APPID, 'Version': '2.2',
            'Sources': 'Video', 'Market': 'en-us',
            #'Options': 'EnableHighlighting',
             'Video.Count': '10', 'Video.Offset': offset,
            'JsonType': 'callback', 'Query': q,
                        }
        bing_options.update(options)
        resp = BingVideo.objects.get(bing_options)

        if resp and hasattr(resp, 'SearchResponse') and hasattr(resp.SearchResponse, 'Video'):
            return resp.SearchResponse.Video

    @staticmethod
    def fetch(q, offset):
        return BingVideo.fetch_with_options(q, offset, {})


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

class AdvancedSearch(models.Model):
    COUNT_CHOICE = (
      (10, 10),
      (20, 20),
      (50, 50),
    )
    MARKETS = (
      ('ar-XA', 'Arabic - Arabia'),
      ('bg-BG', 'Bulgarian - Bulgaria'),
      ('cs-CZ', 'Czech - Czech Republic'),
      ('da-DK', 'Danish - Denmark'),
      ('de-AT', 'German - Austria'),
      ('de-CH', 'German - Switzerland'),
      ('de-DE', 'German - Germany'),
      ('el-GR', 'Greek - Greece'),
      ('en-AU', 'English - Australia'),
      ('en-CA', 'English - Canada'),
      ('en-GB', 'English - United Kingdom'),
      ('en-ID', 'English - Indonesia'),
      ('en-IE', 'English - Ireland'),
      ('en-IN', 'English - India'),
      ('en-MY', 'English - Malaysia'),
      ('en-NZ', 'English - New Zealand'),
      ('en-PH', 'English - Philippines'),
      ('en-SG', 'English - Singapore'),
      ('en-US', 'English - United States'),
      ('en-XA', 'English - Arabia'),
      ('en-ZA', 'English - South Africa'),
      ('es-AR', 'Spanish - Argentina'),
      ('es-CL', 'Spanish - Chile'),
      ('es-ES', 'Spanish - Spain'),
      ('es-MX', 'Spanish - Mexico'),
      ('es-US', 'Spanish - United States'),
      ('es-XL', 'Spanish - Latin America'),
      ('et-EE', 'Estonian - Estonia'),
      ('fi-FI', 'Finnish - Finland'),
      ('fr-BE', 'French - Belgium'),
      ('fr-CA', 'French - Canada'),
      ('fr-CH', 'French - Switzerland'),
      ('fr-FR', 'French - France'),
      ('he-IL', 'Hebrew - Israel'),
      ('hr-HR', 'Croatian - Croatia'),
      ('hu-HU', 'Hungarian - Hungary'),
      ('it-IT', 'Italian - Italy'),
      ('ja-JP', 'Japanese - Japan'),
      ('ko-KR', 'Korean - Korea'),
      ('lt-LT', 'Lithuanian - Lithuania'),
      ('lv-LV', 'Latvian - Latvia'),
      ('nb-NO', 'Norwegian - Norway'),
      ('nl-BE', 'Dutch - Belgium'),
      ('nl-NL', 'Dutch - Netherlands'),
      ('pl-PL', 'Polish - Poland'),
      ('pt-BR', 'Portuguese - Brazil'),
      ('pt-PT', 'Portuguese - Portugal'),
      ('ro-RO', 'Romanian - Romania'),
      ('ru-RU', 'Russian - Russia'),
      ('sk-SK', 'Slovak - Slovak Republic'),
      ('sl-SL', 'Slovenian - Slovenia'),
      ('sv-SE', 'Swedish - Sweden'),
      ('th-TH', 'Thai - Thailand'),
      ('tr-TR', 'Turkish - Turkey'),
      ('uk-UA', 'Ukrainian - Ukraine'),
      ('zh-CN', 'Chinese - China'),
      ('zh-HK', 'Chinese - Hong Kong SAR'),
      ('zh-TW', 'Chinese - Taiwan'),
    )
    
    count = models.PositiveSmallIntegerField(choices = COUNT_CHOICE)
    market = models.CharField(max_length=5, choices = MARKETS)
    user = models.ForeignKey(User)

class SearchApi(models.Model):
    SEARCH_MODELS = (
        ('BingNews','Bing News'),
        ('BingWeb','Bing Web'),
        ('BingImage','Bing Image'),
        ('BingVideo','Bing Video'),
        ('TwitterSearch','Twitter Search'),
        ('GoogleSearch','Google Search'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    muaccount = models.ManyToManyField(MUAccount, blank=True, null=True, related_name='searchapis')
    search_model = models.CharField(max_length=255, choices = SEARCH_MODELS)

    def __unicode__(self):
        return self.name    
