# Caching 
Caching is a technique used to improve the performance of web applications. In simple terms, caching involves storing frequently accessed data or content in a temporary storage location called a cache. This enables web applications to serve content to users more quickly, without having to fetch it from the original source every time it is requested.

Caching is suitable for frequently accessed data without negatively affecting data integrity or application functionality. 
Common use cases include serving static assets like images, stylesheets, and scripts, caching database queries or API responses, and caching pages or content for dynamic web apps. However, consider the caching strategy for each app and regularly refresh or invalidate cached content to avoid serving stale content.

## Cache Types 
### In-memory caching
In-memory caching is a type of caching that involves storing data in the computer’s RAM (Random Access Memory) instead of in a database or on disk. This type of caching is useful for applications that require high-speed access to data, such as web servers and databases. In-memory caching can significantly improve the performance of an application by reducing the number of database queries and disk reads required to retrieve data. However, it is important to note that in-memory caching is volatile and the data stored in the RAM may be lost if the system is shut down or restarted. 

### Distributed caching
Distributed caching is a type of caching that involves storing data across multiple servers or nodes in a network. This type of caching is useful for applications that require high availability and scalability. Distributed caching allows multiple servers to share the workload of storing and retrieving data, which can improve the performance of the application and reduce the risk of data loss. However, managing a distributed caching system can be complex, and ensuring consistency across multiple nodes can be challenging.


### Client-side caching
Client-side caching is a type of caching that involves storing data on the client’s device, such as a web browser. This type of caching is useful for web applications that require frequent access to static resources, such as images and JavaScript files. Client-side caching can significantly improve the performance of a web application by reducing the number of requests made to the server. However, it is important to note that client-side caching can lead to issues with stale data, as the cached data may not always be up-to-date. Therefore, careful consideration should be given to the caching policies and expiration times used in client-side caching.


## Types of Caching in DRF

### 1. **Per-View Caching**
Per-view caching allows you to cache the response of an entire view. This is useful for read-heavy views that do not change often.

```python
from django.views.decorators.cache import cache_page
from django.conf import settings

@cache_page(settings.CACHE_TTL)
def my_view(request):
    # Your view logic here
```

### 2. **Template Fragment Caching**
Template fragment caching is used to cache parts of a template. This is helpful when only certain sections of a template need to be cached.

```django
{% load cache %}
{% cache 500 sidebar %}
    <!-- Expensive sidebar code here -->
{% endcache %}
```

### 3. **Low-Level Caching**
Low-level caching provides more control over what and how you cache. You can cache specific data and manage it directly.

```python
from django.core.cache import cache

# Setting a cache
cache.set('my_key', 'my_value', timeout=60*15)

# Getting from cache
value = cache.get('my_key')
```
### Memcached 
Memcached is a simple, open-source, in-memory caching system that can be used as a temporary in-memory data storage. The stored data in memory has high read and write performance and distributes data into multiple servers. It is a key-value of string object that is stored in memory and the API is available for all the languages. Memcached is very efficient for websites.

### Redis 
Redis is an open-source, key-value, NoSQL database. It is an in-memory data structure that stores all the data served from memory and uses disk for storage. It offers a unique data model and high performance that supports various data structures like string, list, sets, hash, which it uses as a database cache or message broker. It is also called Data Structure Server. It does not support schema RDBMS, SQL, or ACID transactions.
## Redis vs. Memcached

| Feature               | Redis                                  | Memcached                          |
|-----------------------|----------------------------------------|------------------------------------|
| Data Types            | Supports various data types (strings, lists, sets, hashes, etc.) | Only supports string values       |
| Scalability           | Supports data sharding and clustering  | Easy to scale horizontally         |
| Performance           | Extremely fast, slightly slower for complex data types | Very fast, optimized for simple key-value pairs |
| Memory Management     | Uses more memory for advanced data structures | Efficient memory management       |
| Use Cases             | Suitable for complex caching, real-time analytics, message brokering | Best for simple caching scenarios |
| Commands              | Rich set of commands for various operations | Limited set of commands            |
