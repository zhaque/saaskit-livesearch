from django.http import Http404
from django.shortcuts import render_to_response
from livesearch.forms import SearchesForm
from livesearch.models import BingImage, BingWeb, BingVideo, BingNews, TwitterSearch, AdvancedSearch, SearchApi


def searches(request, results='results'):
    search_apis = SearchApi.objects.all()
    for api in search_apis:
      if api.search_model != 'BingWeb':
          continue
      webapi = api
    form = SearchesForm()
    return render_to_response('livesearch/searches.html', {'form': form,
                                                    'result': 'results',
                                                    'api': webapi,
                                                    'title': 'Search by Google and Bing ', })

# deprecatied 
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

            #get search options
            weboptions = {}
            videooptions = {}
            imageoptions = {}
            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(user = request.user)
                weboptions = {'Web.Count': advSearch.count, 'Market': advSearch.market,}  
                videooptions = {'Video.Count': advSearch.count, 'Market': advSearch.market,}
                imageoptions = {'Image.Count': advSearch.count, 'Market': advSearch.market,}
              except:
                raise
            
            bingWebResult = BingWeb.fetch_with_options(key_words, str((page-1)*10 + 1), weboptions)
            bingResult = BingImage.fetch_with_options(key_words, 0, imageoptions)
            bingVideoResult = BingVideo.fetch_with_options(key_words, '0', videooptions)

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


def image_results(request, context_vars):
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

            imageoptions = {}
            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(user = request.user)
                imageoptions = {'Image.Count': advSearch.count, 'Market': advSearch.market,}
              except:
                raise
            
            bingImageResult = BingImage.fetch_with_options(key_words, str((page-1)*10), imageoptions)

            if page*48> int(bingImageResult.Total):
                page = 1

            if page<=10:
                page_start = 1
                page_end = 13
            else:
                page_start = page - 10
                if (page + 10) * 48 <= int(bingImageResult.Total):
                    page_end = page + 10
                else:
                    page_end = int(bingImageResult.Total)/48 + 1

            prev = page - 1 or page
            next = page + 1
            page_range = range(page_start, page_end)
            #caculate the paginator  --- end

            context_vars.update({
                                       'bingImage': bingImageResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Image Search Results',
                                       })
            return render_to_response('livesearch/images.html', context_vars)
    raise Http404



def video_results(request, context_vars):
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

            videooptions = {}
            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(user = request.user)
                videooptions = {'Video.Count': advSearch.count, 'Market': advSearch.market,}
              except:
                raise
            
            bingVideoResult = BingVideo.fetch_with_options(key_words, str((page-1)*10), videooptions)

            if page*48> int(bingVideoResult.Total):
                page = 1

            if page<=10:
                page_start = 1
                page_end = 13
            else:
                page_start = page - 10
                if (page + 10) * 48 <= int(bingVideoResult.Total):
                    page_end = page + 10
                else:
                    page_end = int(bingVideoResult.Total)/48 + 1

            prev = page - 1 or page
            next = page + 1
            page_range = range(page_start, page_end)
            #caculate the paginator  --- end

            context_vars.update({
                                       'bingVideoResult': bingVideoResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Video Search Results',
                                       })
            return render_to_response('livesearch/videos.html', context_vars)
    raise Http404

def news_results(request, context_vars):
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

            newsoptions = {}
            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(user = request.user)
                newsoptions = {'Market': advSearch.market,}
              except:
                raise
            
            bingNewsResult = BingNews.fetch_with_options(key_words, str((page-1)*10 + 1), newsoptions)

            if page*10> int(bingNewsResult.Total):
                page = 1

            if page<=10:
                page_start = 1
                page_end = 13
            else:
                page_start = page - 10
                if (page + 10) * 10 <= int(bingNewsResult.Total):
                    page_end = page + 10
                else:
                    page_end = int(bingNewsResult.Total)/10 + 1

            prev = page - 1 or page
            next = page + 1
            page_range = range(page_start, page_end)
            #caculate the paginator  --- end

            context_vars.update({'bingNews': bingNewsResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing News Search Results',
                                       })
            return render_to_response('livesearch/news.html', context_vars)
    raise Http404
    
def web_results(request, context_vars):
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

            weboptions = {}
            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(user = request.user)
                weboptions = {'Web.Count': advSearch.count, 'Market': advSearch.market,}  
              except:
                raise
            
            bingWebResult = BingWeb.fetch_with_options(key_words, str((page-1)*10 + 1), weboptions)

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

            context_vars.update({'bingweb': bingWebResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Search Results',
                                       })
            return render_to_response('livesearch/web.html', context_vars)
    raise Http404

def twitter_results(request, context_vars):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()

            twitResult = TwitterSearch.fetch(key_words)

            context_vars.update({'results': twitResult,
                                       'q': key_words,
                                       'form': form,
                                       'title': 'Twitter Search Results',
                                       })
            return render_to_response('livesearch/twitter.html', context_vars)
    raise Http404

def search(request, slug):
    if request.muaccount:
        api = SearchApi.objects.get(slug=slug)
        available_apis = SearchApi.objects.filter(muaccount = request.muaccount)
        context_vars = {'api':api, 'available_apis':available_apis}
        if api in available_apis:
            return search_results(request, context_vars)
        else:
            raise Http404
            #TODO show api unavailable page
          
def search_results(request, context_vars):
    searchModel = globals()[context_vars['api'].search_model]()

    if isinstance(searchModel, BingNews):
        return news_results(request, context_vars)
    elif isinstance(searchModel, BingImage):
        return image_results(request, context_vars)
    elif isinstance(searchModel, BingVideo):
        return video_results(request, context_vars)
    elif isinstance(searchModel, BingWeb):
        return web_results(request, context_vars)
    elif isinstance(searchModel, TwitterSearch):
        return twitter_results(request, context_vars)
#    raise Http404
