---
url: /content/
title: Content
modified: 2018-11-05T11:50:00+04:00
order: 4
next:
  url: /templates/
  title: Templates
---

# Content

## Files location

Currently **wt** supports two types of content:

- **pages** - regular pages like About, Contacts, etc.,
- **posts** - stream of posts, news or whatever you'd like to paginate within
  your project.

**`wt`** engine will look for source files for **pages** and **posts** in
two different directories.
For **pages** it is **`content/pages/`** directory and for **posts** it's
**`content/posts/`** directory.

## Text

By default content within **pages** and **posts** files should be written using
`markdown` but you are not forced to do so - you can use even raw html if you
like.

Your **pages** and **posts** content will be available in templates as `text`
property of the `content` variable.

Here is an example of `jinja` template to render content written in `markdown`:

```jinja
<div>{{ markdown(content.text) }}</div>
```

`markdown()` function in the example above is a global function registered in
`jinja` environment by `wt` engine. There is another one global function
available in `jinja` environment - `baseurl()`. Please check
[Templates][wt-templates] page for details.

Here is an example of `jinja` template in case you'd like to write content as
plain html:

```jinja
{% autoescape false %}
{{ content.text }}
{% endautoescape %}
```

## Front matter properties

`wt` engine supports following properties defined in front matter:

- **`url`** (required) - url for page or post,
- **`modified`** (required) - [ISO 8601][iso8601] formatted content
    modification timestamp,
- **`template`** (optional) - individual template to render this **page** or
    **post**,
- **`draft`** (optional, **post** only) - boolean (`true` or `false`) value,
    indicating **post** is not ready to be published yet; `true` value means
    **post** will be accessible while developing but will be skipped while
    building the project.

You can define any other front matter property as needed.

All front matter properties are available in template rendering context as
properties of `content` variable. For example, suppose you have `title`
property defined in page front matter:

```yaml
title: Some page title
```

which you can reference in template as:

```html
<h1>{{ content.title }}</h1>
```

### Url

You can configure **`url`** in two ways - pointing to resulting html file name
or pointing to a directory.

Resulting html file name can have any path and filename specified according to
your needs (it can be **`/info.html`** or **`/foo/info.html`** or
**`/foo/bar/info.html`**).

In case **`url`** points to a directory **`wt`** engine will automatically
create **`index.html`** file inside.

### Modified

Modification timestamp is used to sort **posts** for pagination and can be used
to place somewhere in generated html.

It is pretty easy to handle [ISO 8601][iso8601] format even though it might
look a bit unusual. This is a standard and it can be automatically parsed and
this timestamp will be available within templates as native python's datetime
instance.

## Examples

Here are examples of **page** and **post** front matter definitions.

### Page

```yaml
---
url: /foo/                             # Page url
title: Foo page title                  # Title
modified: 2016-09-18T11:31:00+04:00    # Modification date/time
template: foo.html                     # Template for this page
---

Here goes page content
```

### Post

```yaml
---
url: /baz/                             # Page url
title: Baz page title                  # Title
modified: 2016-09-20T20:10:00+04:00    # Modification date/time
template: posts/baz.html               # Template for this page
---

Here goes post content
```

Single **post** properties definitions are just like regular **page**
properties definitions.

Just remember that **pages** and **posts** are expected to be in different
directories.

One more thing worth noting is **post** representation within templates.
As **posts** is a stream sometimes there is a need for forward and backward
navigation between posts. You will have this feature for **post** only. Each
**post** definition will have **`prev`** and **`next`** attributes pointing to
correspondent **posts** (sorted by **`modified`** property in reversed order).

Here is an example of template with navigation to previous or next **post**
in the stream:

```html

{% if content.prev %}
<a href="{{ content.prev.url }}">{{ content.prev.title }}</a>
{% endif %}
{% if content.next %}
<a href="{{ content.next.url }}">{{ content.next.title }}</a>
{% endif %}

```

## What's next

Let's continue with [Templates][wt-templates] topic.


[iso8601]: https://en.wikipedia.org/wiki/ISO_8601
[wt-templates]: /templates/
[wt-configuration]: /configuration/#templates
