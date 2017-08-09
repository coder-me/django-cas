# django-cas (CoderMe Awesome Stuff)

### What's django-cas
* its collection of django related "stuff": middlewares, decorators and validators used internally at CoderMe.com

### Whats include/d
* Middlewares:
 - SuperCacheMiddleware
	 provide fine tunning for Cache-Control HTTP header. By setting max age for urls you can control which pages/responses get cached in web browsers and frontend caching proxy.

 - SubdomainMiddleware:
	maps subdomains to apps
    	For example an app named 'blog' which has url prefixed by 'blog'
    	can be mapped to subdomain blog.example.com like:
    		- Originally: https://www.example.com/blog/my-article
    		- Becomes: https://blog.example.com/my-article
    	or with i18n enabled as follows:
    		- Originally: https://www.example.com/en/blog/my-article
    		- Becomes: https://blog.example.com/en/my-article
* Decoators:
 - require_AJAX:
	 Allows ajax request only and raise SuspiciousOperation exception if request is not an ajax.

* Validators:
 - valid_regex: validate if value is a valid regex or raise ValidationError.
 - zeroslash_slug: validate if a value is a valid slug with no slashes valid slugs those don't contain any of the following chars:
    ! @ ~ # \ > < : ; [ ] { } % & * ( ) $ / \s ?
 - oneslash_slug: same as zeroslash_slug but value must contain one slash '/' to be considered valid.




