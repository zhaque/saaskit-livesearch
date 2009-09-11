from django.http import Http404
from django.shortcuts import render_to_response
from forms import SearchesForm
from models import BingImage, BingWeb, BingVideo, BingNews, TwitterSearch, AdvancedSearch


def searches(request, results='results'):
    form = SearchesForm()
    return render_to_response('livesearch/searches.html', {'form': form,
                                                    'result': 'results',
                                                    'title': 'Search by Google and Bing ', })

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

            return render_to_response('livesearch/images.html',
                                      {
                                       'bingImage': bingImageResult,
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

            return render_to_response('livesearch/videos.html',
                                      {
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

def news_results(request):
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

            return render_to_response('livesearch/news.html',
                                      {'bingNews': bingNewsResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing News Search Results',
                                       })
    raise Http404
    
def web_results(request):
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

            return render_to_response('livesearch/web.html',
                                      {'bingweb': bingWebResult,
                                       'q': key_words,
                                       'form': form,
                                       'page': page,
                                       'prev': prev,
                                       'next': next,
                                       'page_range': page_range,
                                       'title': 'Bing Search Results',
                                       })
    raise Http404

def twitter_results(request):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()

            twitResult = TwitterSearch.fetch(key_words)

            return render_to_response('livesearch/twitter.html',
                                      {'results': twitResult,
                                       'q': key_words,
                                       'form': form,
                                       'title': 'Twitter Search Results',
                                       })
    raise Http404
