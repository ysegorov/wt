# Changelog



## 0.4.0 (?)

- [+] #23 yaml configuration can be splitted into multiple files
- [\*] #24 tests rewritten using pytest-describe plugin
- [\*] #25 [!] `wt.base` module refactored, module api breakage


## 0.3.1 (2017-03-21)

- [\*] minor fix for pypi targeted readme translation from md to rst
  (`pypandoc` was not installed in virtualenv during build)


## 0.3.0 (2017-03-21)

- [+] #21 wt instance in rendering context
- [+] #20 allow jinja filters and globals to be extended using `jinja_helpers`
  module
- [+] #18 page and post configuration can have custom template for rendering
- [+] #17 wt.yaml values can have placeholders like `${URL}` to be replaced by
  environment variables, missed variables will be skipped
- [+] #4, #16, #22 local links validation
- [+] #7 add option to skip feed rendering
- [\*] #8 render mainpage only once in case mainpage content is in pages
- [+] #2 pagination for posts (mainpage) list


## 0.2.0 (2016-10-05)

- [+] #6 add `wt init` command to bootstrap project
- [+] #5 use travis ci for testing


## 0.1.0 (2016-09-22)

- initial release
