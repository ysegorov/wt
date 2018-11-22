---
url: /objects/
title: Objects
modified: 2018-11-16T06:24:00Z
order: 6
next:
  url: /cli/
  title: Command-line Interface
---

# Objects

`wt` engine has several simple objects representing
[configuration][wt-configuration] and [content][wt-content] data.

For a list of **posts** `wt` uses simple `Paginator` object providing useful
pagination attributes.

Let's check these objects.


## Config

This is an object to hold configuration data loaded from **wt.yaml** file and
there is nothing special about it.

It is available within templates as `config` variable and allows access to
**wt.yaml** values using dot notation.

For example, following **wt.yaml** data:

```yaml

title: Site title
mainpage:
    subtitle: Mainpage subtitle

```
can be accessed in template as:

```jinja

<h1>{{ config.title }}</h1>
<h2>{{ config.mainpage.subtitle }}</h2>

```


## Content

This is an object to hold **page** or **post** data loaded from correspondent
directory (`content/pages/` for **page** and `content/posts/` for **post**).

This object will hold all properties defined within front matter of the source
file and following special properties:

- **`content.text`** - file content (everything except front matter if specified),
- **`content.mtime`** - file modification time (used as fallback value for `modified`
    property in case `modified` is not specified within front matter),
- **`content.prev`** - link to previous **post** in the list of `posts` variable within
    templates (this property is available **only** for **post** and **only**
    within **list of posts**),
- **`content.next`** - link to next **post** in the list of `posts` variable within
    templates (this property is available **only** for **post** and **only**
    within **list of posts**).

These and all other properties, loaded from front matter, can be accessed using
dot notation.

Here is an example of page file:

```yaml

---
title: About
url: /about/
modified: 2018-10-10T09:10:00Z
template: about.html
---

# About

This is the page about our company.

...

```

and template to render it:

```jinja

<html>
<head>
    <title>{{ content.title }}</title>
</head>
<body>
    <h1>{{ content.title }}</h1>
    <div id="content">{{ markdown(content.text) }}</div>
    <div id="footer">Modified at {{ content.modified }}</div>
</body>
</html>

```


## Paginator

Let's check `paginator` object's attributes:

- **`paginator.items`** - list of current page **post** items,
- **`paginator.has_prev`** - boolean attribute indicating previous page exists,
- **`paginator.has_next`** - boolean attribute indicating next page exists,
- **`paginator.prev_page`** - pair of **`(page_url, page_number)`** values for
  previous page,
- **`paginator.next_page`** - pair of **`(page_url, page_number)`** values for
  next page,
- **`paginator.first_page`** - pair of **`(page_url, page_number)`** values for
  first page,
- **`paginator.last_page`** - pair of **`(page_url, page_number)`** values for
  last page,
- **`paginator.num_pages`** - number of pages,
- **`paginator.pages`** - ordered dictionary of **`(page_url, page_number)`**
  pairs.

Here is a [real-life example][wt-pagination-example] of pagination in action:

```html

{% for post in paginator.items %}
<article class="blog-post">
    <header class="blog-post-header">
        <h2 class="blog-post-title"><a class="blog-post-link" href="{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a></h2>
    </header>
    <footer class="blog-post-footer">
        <span class="blog-post-published">{{ post.published.strftime("%A, %d %B %Y") if post.published else post.modified.strftime("%A, %d %B %Y") }}</span>
    </footer>
</article>
{% endfor %}

{% if paginator.has_prev or paginator.has_next %}
<div class="content-prev-next">
    <div class="content-prev">
    {% if paginator.has_prev %}
        {% set url, num = paginator.prev_page %}
        <a class="content-prev-link" href="{{ url }}">
            <i class="fa fa-angle-double-left fa-fw"></i><span class="ib">previous</span>
        </a>
    {%- endif %}
    </div>
    <div class="content-next">
    {% if paginator.has_next %}
        {% set url, num = paginator.next_page %}
        <a class="content-next-link" href="{{ url }}">
            <span class="ib">next</span><i class="fa fa-angle-double-right fa-fw"></i>
        </a>
    {%- endif %}
    </div>
</div>
{% endif %}

```


## What's next

Let's continue with [Command-line interface][wt-cli] topic.

[wt-pagination-example]: https://github.com/ysegorov/blog/blob/master/templates/mainpage.html#L19-L49
[wt-configuration]: /configuration/
[wt-content]: /content/
[wt-cli]: /cli/
