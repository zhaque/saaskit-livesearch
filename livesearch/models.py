from django.db import models
import django_pipes as pipes
from django.conf import settings
from django.contrib.auth.models import User
from muaccounts.models import MUAccount

class BaseSearch:
    # override it for custom fetch
    def raw_fetch(self, query, *args, **kwargs):
        pass

    # override it for custom result parsing 
    def get_result(self, response):
        pass

    # public method, don't override it in child classes, do it with raw_fetch instead
    def fetch(self, query, *args, **kwargs):
        response = self.raw_fetch(query, *args, **kwargs)
        return self.get_result(response)

class PipeSearch(BaseSearch, pipes.Pipe):
    uri = ''
    cache_expiry = 3000000000

    def init_options(self):
        self.options = dict()

    def set_query(self, query):
        pass

    def set_count(self, count=10):
        pass

    def set_offset(self, offset=0):
        pass

    def set_market(self, market=''):
        pass

    def set_version(self, version=''):
        pass

    def set_adult(self, adult=''):
        pass

    def set_longitude(self, longitude):
        pass

    def set_latitude(self, latitude):
        pass

    def set_radius(self, radius):
        pass

    def raw_fetch(self, query, count=None, offset=None, market=None, version=None, adult=None):
        self.set_query(query)
        if count:
            self.set_count(count)
        if offset:
            self.set_offset(offset)
        if market:
            self.set_market(market)
        if version:
            self.set_version(version)
        if adult:
            self.set_adult(adult)

        return self.fetch_with_options(self.options)

    def fetch_with_options(self, options):
        resp = self.objects.get(options)
        if resp:
            return resp
        return None

class YqlSearch(PipeSearch):
    uri = "http://query.yahooapis.com/v1/public/yql"

    def init_options(self):
        super(YqlSearch, self).init_options()
        self.set_format()
        self.set_env()

    def set_query(self, query):
        self.options.update({'q':query})

    def set_format(self, format='json'):
        self.options.update({'format':format})

    def set_callback(self, callback):
        self.options.update({'callback':callback})

    def set_env(self, env='http://datatables.org/alltables.env'):
        self.options.update({'env':env})

    def get_result(self, response):
        res = dict()
        if response and hasattr(response, "query"):
            res.update({'yql':response.query,})
        elif response and hasattr(response, "error"):
            res.update({'yql':response.error,})

        return res

class GoogleSearch(PipeSearch):
    uri = "http://ajax.googleapis.com/ajax/services/search/web"

    def init_options(self):
        super(GoogleSearch, self).init_options()
        self.options.update({'v':1.0})
    
    def set_query(self, query):
        self.options.update({'q':query})

    def get_result(self, response):
        res = dict()
        if response and hasattr(response, "responseData") and hasattr(response.responseData, "results"):
            res.update({'google':response.responseData.results,})
        return res

class TwitterSearch(PipeSearch):
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 300000

    def set_query(self, query):
        self.options.update({'q':query})

    def set_count(self, count=100):
        self.count = count
        self.options.update({'rpp':count})

    def set_offset(self, offset=0):
        offset = int(offset)
        page = int(offset/self.count) + 1
        self.options.update({'page':page})

    def set_longitude(self, longitude):
        self.longitude = longitude
        self.set_geocode()

    def set_latitude(self, latitude):
        self.latitude = latitude
        self.set_geocode()

    def set_radius(self, radius):
        self.radius = radius
        self.set_geocode()

    def set_geocode(self):
        if hasattr(self,'longitude') and hasattr(self,'latitude') and hasattr(self,'radius'):
            geocode = '%s,%s,%smi' % (self.latitude, self.longitude, self.radius)
            self.options.update({'geocode':geocode})

    def set_market(self, market='en-US'):
        self.options.update({'lang':market[:2]})

    def get_result(self, response):
        res = dict()
        if response and hasattr(response, "results"):
            res.update({'twitter':response.results,})
        return res

class BingMultiple(PipeSearch):
    uri = "http://api.bing.net/json.aspx"

    def init_options(self):
        super(BingMultiple, self).init_options()
        self.options.update({
            'AppId':settings.APPID,
            'JsonType': 'raw',
            'Options': 'DisableLocationDetection',
        })
        self.set_count()
        self.set_offset()
        self.set_market()
        self.set_version()
        self.set_adult()

    def set_query(self, query):
        self.options.update({'Query':query})

    def set_market(self, market='en-US'):
        self.options.update({'Market':market})

    def set_version(self, version='2.2'):
        self.options.update({'Version':version})

    def set_longitude(self, longitude):
        if longitude:
            self.options.update({'Longitude':longitude})

    def set_latitude(self, latitude):
        if latitude:
            self.options.update({'Latitude':latitude})

    def set_radius(self, radius):
        if radius:
            self.options.update({'Radius':radius})

    def get_result(self, response):
        if response and hasattr(response, "SearchResponse"):
            response = response.SearchResponse
        else:
            return None

        res = dict()
        if hasattr(response, "Web") and hasattr(response.Web, 'Results'):
            res.update({'web':response.Web,})
        if hasattr(response, "News") and hasattr(response.News, 'Results'):
            res.update({'news':response.News,})
        if hasattr(response, "Image") and hasattr(response.Image, 'Results'):
            res.update({'images':response.Image,})
        if hasattr(response, "Video") and hasattr(response.Video, 'Results'):
            res.update({'video':response.Video,})
        if hasattr(response, 'RelatedSearch') and hasattr(response.RelatedSearch, 'Results'):
            res.update({'related': response.RelatedSearch.Results})
        if hasattr(response, 'InstantAnswer') and hasattr(response.InstantAnswer, 'Results'):
            res.update({'instant': response.InstantAnswer.Results})
        if hasattr(response, "Spell") and hasattr(response.Spell, 'Results'):
            res.update({'spell': response.Spell})
        if hasattr(response, 'Errors'):
            res.update({'errors': response.Errors})
        return res

# BingNews searches InstantAnswer
class BingInstant(BingMultiple):
    """
    resp.InstantAnswer.Results[0].keys()
[u'Url', u'ClickThroughUrl', u'ContentType', u'InstantAnswerSpecificData', u'Title']
    """

    def init_options(self):
        super(BingInstant, self).init_options()
        self.options.update({'Sources': 'InstantAnswer',})

class BingRelated(BingMultiple):
    """
    resp.RelatedSearch.Results[3].keys()
[u'Url', u'Title']
    """

    def init_options(self):
        super(BingRelated, self).init_options()
        self.options.update({'Sources': 'RelatedSearch',})

# BingNews searches news
class BingNews(BingMultiple):
    CATEGORIES = (
        ('rt_Business','Business'),
        ('rt_Entertainment','Entertainment'),
        ('rt_Health','Health'),
        ('rt_Political','Political'),
        ('rt_Scientific','Scientific'),
        ('rt_Sports','Sports'),
        ('rt_US','US'),
        ('rt_World','World'),
        ('rt_Local','Local'),
        ('rt_ScienceAndTechnology','Science and Technology'),
    )

    def init_options(self):
        super(BingNews, self).init_options()
        self.options.update({
            'Sources': 'News',
        })
        self.set_sortby()

    def set_count(self, count=15):
        if count > 15: count=15 #we have to hardcode it because if count>15 Bing return error
        self.options.update({'News.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'News.Offset':offset})

    def set_sortby(self, sortby='Date'):
        self.options.update({'News.SortBy':sortby})

    def set_category(self, category):
        self.options.update({'News.Category':category})

class BingNewsRelated(BingNews):

    def init_options(self):
        super(BingNewsRelated, self).init_options()
        self.options.update({
            'Sources': 'News RelatedSearch',
        })

class BingNewsRelatedSpell(BingNews):

    def init_options(self):
        super(BingNewsRelatedSpell, self).init_options()
        self.options.update({
            'Sources': 'News RelatedSearch Spell',
        })

class BingWeb(BingMultiple):
    """
    resp.Web.Results[0].keys()
[u'Url', u'Title', u'DisplayUrl', u'Description', u'DateTime']

    """
      # 'Web.Options':'DisableHostCollapsing+DisableQueryAlterations',

    def init_options(self):
        super(BingWeb, self).init_options()
        self.options.update({
            'Sources':'Web',
        })

    def set_count(self, count=10):
        if count > 50: count=50 #we have to hardcode it because if count>50 Bing return error
        self.options.update({'Web.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'Web.Offset':offset})

    def set_adult(self, adult='Moderate'):
        self.options.update({'Adult':adult})

class BingImage(BingWeb):

    def init_options(self):
        super(BingImage, self).init_options()
        self.options.update({
            'Sources':'Image',
        })

    def set_count(self, count=10):
        if count > 50: count=50 #we have to hardcode it because if count>50 Bing return error
        self.options.update({'Image.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'Image.Offset':offset})

class BingVideo(BingWeb):
    """
    resp2.Video.keys()
[u'Total', u'Results', u'Offset']
    resp2.Video.Results[0].keys()
[u'Title', u'SourceTitle', u'StaticThumbnail', u'ClickThroughPageUrl', u'RunTime', u'PlayUrl']
    """

    def init_options(self):
        super(BingVideo, self).init_options()
        self.options.update({
            'Sources':'Video',
        })
        self.set_sortby()

    def set_count(self, count=10):
        if count > 50: count=50 #we have to hardcode it because if count>50 Bing return error
        self.options.update({'Video.Count':count})

    def set_offset(self, offset=0):
        self.options.update({'Video.Offset':offset})

    def set_sortby(self, sortby='Date'):
        self.options.update({'Video.SortBy':sortby})

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
    muaccount = models.ForeignKey(MUAccount)

class SearchApi(models.Model):
    SEARCH_MODELS = (
        ('BingWeb','Bing Web'),
        ('BingNews','Bing News'),
        ('BingNewsRelated', 'Bing News+Related'),
        ('BingNewsRelatedSpell', 'Bing News+Related+Spell'),
        ('BingImage','Bing Image'),
        ('BingVideo','Bing Video'),
        ('TwitterSearch','Twitter Search'),
        ('GoogleSearch','Google Search'),
        ('YqlSearch','Yahoo Query Language Search'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    muaccount = models.ManyToManyField(MUAccount, blank=True, null=True, related_name='searchapis')
    search_model = models.CharField(max_length=255, choices = SEARCH_MODELS)

    def __unicode__(self):
        return self.name
  
