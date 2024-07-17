from django.core.cache import cache

def book__cache(cache_key, queryset, timeout=100):
    if cache_key in cache:
        print('Data fetched from cache')
        return cache.get(cache_key)
    else:
        print('Data fetched from database')
        queryset = queryset()
        cache.set(cache_key, list(queryset), timeout=timeout)
        return queryset
    
def top_book_cache(cache_key,queryset_fun,timeout=60*60*2):
    if cache_key in cache:
        print('from cache')
        return cache.get(cache_key)
    print('from database')
    queryset=queryset_fun()
    cache.set(cache_key,list(queryset),timeout=timeout)
    return queryset



