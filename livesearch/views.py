from django.http import Http404
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from livesearch.forms import SearchesForm
from livesearch.models import BingImage, BingWeb, BingVideo, BingNews, TwitterSearch, AdvancedSearch, SearchApi, BingNewsRelatedSpell, GoogleSearch, YqlSearch
from django.views.generic.simple import direct_to_template


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

def search(request, slug):
    if request.muaccount:
        api = SearchApi.objects.get(slug=slug)
        available_apis = SearchApi.objects.filter(muaccount = request.muaccount)
        context_vars = {'api':api, 'available_apis':available_apis}
        if api in available_apis:
            return search_results(request, context_vars)
        else:
            raise Http404
            #TODO: show api unavailable page
          
def search_results(request, context_vars):
    searchModel = globals()[context_vars['api'].search_model]()

    if isinstance(searchModel, BingNews):
        context_vars['title'] = 'Bing News Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, BingImage):
        context_vars['title'] = 'Bing Image Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, BingVideo):
        context_vars['title'] = 'Bing Video Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, BingWeb):
        context_vars['title'] = 'Bing Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, TwitterSearch):
        context_vars['title'] = 'Twitter Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, BingNewsRelatedSpell):
        context_vars['title'] = 'Bing News+Related+Spell Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, GoogleSearch):
        context_vars['title'] = 'Google Search Results'
        return multi_results(request, context_vars)
    elif isinstance(searchModel, YqlSearch):
        context_vars['title'] = 'Yahoo Query Language Search Results'
        return multi_results(request, context_vars)
    raise Http404

def get_paging_context(paginated_result, current_page, results_per_page):
    import re
    pattern = re.compile(r"^\d+$")
    if not pattern.match(current_page):
        current_page = '1'
    current_page = int(current_page)
    
    if current_page*results_per_page> int(paginated_result.Total):
        current_page = 1
    
    if current_page<=10:
        page_start = 1
        page_end = 13
    else:
        page_start = current_page - 10
        if (current_page + 10) * results_per_page <= int(paginated_result.Total):
            page_end = current_page + 10
        else:
            page_end = int(paginated_result.Total)/results_per_page + 1
    
    prev = current_page - 1 or current_page
    next = current_page + 1
    page_range = range(page_start, page_end)
    return {
            'page': current_page,
            'prev': prev,
            'next': next,
            'page_range': page_range,
            }

def multi_results(request, context_vars):
    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()
            page = request.GET.get('page', '1')

            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(muaccount = request.muaccount)
              except ObjectDoesNotExist:
                advSearch = AdvancedSearch()
                advSearch.count = 10
                advSearch.market = None
                
            
            search_obj = globals()[context_vars['api'].search_model]()
            search_obj.init_options()
            result = search_obj.fetch(query=key_words, count=advSearch.count, offset=str((int(page)-1)*advSearch.count), market=advSearch.market)
            
            paginated_res = None
            if 'news' in result: paginated_res = result['news']
            elif 'web' in result: paginated_res = result['web'] 
            elif 'images' in result: paginated_res = result['images'] 
            elif 'video' in result: paginated_res = result['video'] 
            
            if paginated_res:
                context_vars.update(get_paging_context(paginated_res, page, advSearch.count))

            context_vars.update({
                                  'results': result,
                                  'q': key_words,
                                  'form': form,
                                  })
            return direct_to_template(request, template = 'livesearch/multi.html', extra_context = context_vars)
    raise Http404

def combined(request):
    if request.muaccount:
        available_apis = SearchApi.objects.filter(muaccount = request.muaccount)

    if request.method == 'GET':
        form = SearchesForm(request.GET)
        if form.is_valid():
            key_words = form.get_keywords()
 
            if request.user.is_authenticated():
              try:
                advSearch = AdvancedSearch.objects.get(muaccount = request.muaccount)
              except ObjectDoesNotExist:
                advSearch = AdvancedSearch()
                advSearch.market = None

            results = dict()                
            for api in available_apis:            
              search_obj = globals()[api.search_model]()
              search_obj.init_options()
              result = search_obj.fetch(query=key_words, count=5, market=advSearch.market)
              results[api.search_model] = {'result': result, 'api': api}

            context_vars = {
              'available_apis':available_apis,
              'results': results,
              'q': key_words,
              'form': form,
              'title':'Combined Search Results',
            }
            return direct_to_template(request, template = 'livesearch/combined.html', extra_context = context_vars)
    raise Http404
