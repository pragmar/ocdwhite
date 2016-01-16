ocdwhite
========

Django HTML Pretty Print Middleware

Django templates are great, but the better they look the worse the HTML outputs. There's no reason to not have both readable templates and HTML output that doesn't look like whitespace vomit. 

This middleware uses the lxml python package which is built on the super-fast libxml2/libxslt libraries. It will add additional (negligible) processing to each page that passes through, but you already knew that. If your current django html doesn't bother you, don't use this. It's called OCD White for a reason - it's designed for those of us who are a bit obsessive about the HTML we serve.

![OCDWhite](http://i.imgur.com/IDlOXrr.png)![OCDWhite](http://i.imgur.com/IDlOXrr.png)

To add to a project, open up settings and point at the OCDWhiteMiddleware.

```
MIDDLEWARE_CLASSES = (
    ...
    '<path>.ocdwhite.OCDWhiteMiddleware',
)
```

For examples of production use, refer to:
 * [weathertronic](http://weathertronic.com)
 * [ohdowas.com](http://ohdowas.com)

