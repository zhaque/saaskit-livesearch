# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.shortcuts import render_to_response
from django.utils import simplejson
from forms import SearchForm, SearchesForm, AdminOptions
from models import GoogleSearch, BingImage, BingWeb, BingVideo, AdminSearchOption
from django.utils.functional import wraps
from django.template import RequestContext
from django.core.urlresolvers import reverse


def searches(request, results='results'):
    response = HttpResponse()
    form = SearchesForm()
    response = render_to_response('livesearch/searches.html', {'form': form,
                                                    'result': 'results',
                                                    'title': 'Search by Google and Bing ', })
    try:
        options = AdminSearchOption.objects.get(muaccount=request.muaccount)

        response.set_cookie("search_option", options.search_option)
        response.set_cookie("adult_option", options.adult_option)
        response.set_cookie("web_search", options.web_search)
        response.set_cookie("video_search", options.video_search)

    except AdminSearchOption.DoesNotExist:
        pass

    return response


def _get_search_option(option):
    result = {
                'DisableLocationDetection' : {'Options':'DisableLocationDetection'},
                'EnableHighlighting' : {'Options':'EnableHighlighting'},
                'All' : {'Options':'DisableLocationDetection+EnableHighlighting'},
              }
    return result.get(option, {})


def _get_adult_option(option):
    result = {
                'Off' : {'Adult':'Off'},
                'Moderate' : {'Adult':'Off'},
                'Strict' :  {'Adult':'Off'},
              }
    return result.get(option, {})


def _get_web_search(option):
    result = {
                'DisableHostCollapsing' : {'Web.Options':'DisableHostCollapsing'},
                'DisableQueryAlterations' : {'Web.Options':'DisableQueryAlterations'},
                'All' : {'Web.Options':'DisableHostCollapsing+DisableQueryAlterations'},
              }
    return result.get(option, lambda : {})


def _get_video_search(option):
    result = {
                'Date' : {'Video.Options':'Date'},
                'Relevance' : {'Video.Options':'Relevance'},
              }
    return result.get(option, {})


def results(request):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()
            page = request.GET.get('page', '1')

            #caculate the paginator --start
            import re
            pattern = re.compile(r"^\d+$")
            if not pattern.match(page):
                page = '1'
            page = int(page)
            options = {}
            if 'search_option' in request.COOKIES:
                options.update(_get_search_option(request.COOKIES["search_option"]))
            if 'adult_option' in request.COOKIES:
                options.update(_get_adult_option(request.COOKIES["adult_option"]))
            if 'web_search' in request.COOKIES:
                options.update(_get_web_search(request.COOKIES["web_search"]))

            bingWebResult = BingWeb.fetch_with_options(key_words, str((page-1)*10 + 1), options)
            bingResult = BingImage.fetch(key_words, 6, 0)
            bingVideoResult = BingVideo.fetch(key_words, '6', '0')

            if page*10> int(bingWebResult.Total):
                page = 1

            if page<=10:
                page_start = 1
                page_end = 13
            else:
                page_start = page - 10
                if (page + 10) * 10 <= int(bingWebResult.Total):
                    page_end = page + 10
                else:
                    page_end = int(bingWebResult.Total)/10 + 1

            prev = page - 1 or page
            next = page + 1
            page_range = range(page_start, page_end)
            #caculate the paginator  --- end

            return render_to_response('livesearch/results.html',
                                      {'bingweb': bingWebResult,
                                       'bresults': bingResult,
                                       'bingVideoResult': bingVideoResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Search Results',
                                       })


def image_results(request):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()
            page = request.GET.get('page', '1')

            #caculate the paginator --start
            import re
            pattern = re.compile(r"^\d+$")
            if not pattern.match(page):
                page = '1'
            page = int(page)

            bingWebResult = BingWeb.fetch_with_options(key_words, 0, {})
            bingImageResult = BingImage.fetch(key_words, 48, str((page-1)*10))
            bingVideoResult = BingVideo.fetch(key_words, '6', '0')

            if page*48> int(bingWebResult.Total):
                page = 1

            if page<=10:
                page_start = 1
                page_end = 13
            else:
                page_start = page - 10
                if (page + 10) * 48 <= int(bingWebResult.Total):
                    page_end = page + 10
                else:
                    page_end = int(bingWebResult.Total)/48 + 1

            prev = page - 1 or page
            next = page + 1
            page_range = range(page_start, page_end)
            #caculate the paginator  --- end

            return render_to_response('livesearch/images.html',
                                      {'bingWeb': bingWebResult,
                                       'bingImage': bingImageResult,
                                       'bingVideoResult': bingVideoResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Image Search Results',
                                       })
    raise Http404



def video_results(request):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()
            page = request.GET.get('page', '1')

            #caculate the paginator --start
            import re
            pattern = re.compile(r"^\d+$")
            if not pattern.match(page):
                page = '1'
            page = int(page)

            bingWebResult = BingWeb.fetch_with_options(key_words, 0, {})
            bingImageResult = BingImage.fetch(key_words, 6, 0)
            bingVideoResult = BingVideo.fetch(key_words, 48, str((page-1)*10))

            if page*48> int(bingWebResult.Total):
                page = 1

            if page<=10:
                page_start = 1
                page_end = 13
            else:
                page_start = page - 10
                if (page + 10) * 48 <= int(bingWebResult.Total):
                    page_end = page + 10
                else:
                    page_end = int(bingWebResult.Total)/48 + 1

            prev = page - 1 or page
            next = page + 1
            page_range = range(page_start, page_end)
            #caculate the paginator  --- end

            return render_to_response('livesearch/videos.html',
                                      {'bingWeb': bingWebResult,
                                       'bingImage': bingImageResult,
                                       'bingVideoResult': bingVideoResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Video Search Results',
                                       })
    raise Http404




def msearches(request):
    form = SearchesForm()
    return render_to_response('searches.html', {'form': form,
                                                'result': 'mresults',
                                                'title': 'Search by Google and Bing Multiple', })


def mresults(request):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()

            googleResult = GoogleSearch.fetch(key_words)
            for result in googleResult:
                '''result.bresult = BossInlink.fetch(result.unescapedUrl)'''
            result.presult =BossPagedata.fetch(googleResult[0].unescapedUrl)
            print '+++++++++++++++++++++++++++++++++++++++++'
            print result.presult.items()
            print '+++++++++++++++++++++++++++++++++++++++++'

            bingResult = BingMultiple.fetch(key_words)
            '''for result in bingResult.Web.Results:
                result.bresult = BossInlink.fetch(request.Url)
                result.presult = BossPagedata.fetch(result.Url)'''

            return render_to_response('mresults.html',
                                      {'gresults': googleResult,
                                       'bresults': bingResult,
                                       'q': key_words,
                                       'title': 'Google & Bing Search Results',
                                       })
    raise Http404

def check_owner(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated() \
            and request.user <> request.muaccount.owner:
            logout(request)
            return HttpResponseRedirect(reverse('user_signin'))
        elif not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('user_signin'))
        return func(request, *args, **kwargs)

    wrapper = wraps(func)(wrapper)
    return wrapper

@check_owner
def search_admin(request):
    options, created = AdminSearchOption.objects.get_or_create(muaccount = request.muaccount)

    if request.method == 'GET':

        form = AdminOptions(instance=options)
        return render_to_response('livesearch/admin-search.html', locals(),
                              context_instance=RequestContext(request),)
    else:
        #raise
        form = AdminOptions(request.POST, instance=options)
        if form.is_valid():
            form.save()
            options_save = 1

        return render_to_response('livesearch/admin-search.html', locals(),
                                          context_instance=RequestContext(request),)

