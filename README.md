# webflex

collection of python tools to make static website generators

the intention of webflex is to write websites in python and help generate them as pure html files rather than have 10 million `with` blocks.
just create a generator:

```py
from webflex.generator import Generator
from webflex.templates import HTML5

gen = Generator('docs/') # directory where everything should be generated
```

then write your webpage, here we'll just create a hello world example:

```py
def index(data):
    return HTML5(
        header = '<title>My website!</title>',
        body = '<p>Hello, World!</p>'
    )

# and then we can just tell the generator to make our page

gen.make_page('index', index)
```

and once you get really into it you can make more dynamic stuff like:

```py
from webflex.generator import Generator
from webflex.templates import CommonHTML5

HTML5 = CommonHTML5(
    stylesheet = 'docs/style.css',
)

gen = Generator('docs/')

def Header(focused_tab):
    tabs = {
        'home': ['Home', 'index.html'],
        'about': ['About', 'about.html'],
        'contact': ['Contact', 'contact.html'],
    }

    comp = '<div class="header">'
    for key in tabs:
        if focused_tab == key:
            node = f'<a class="focused" href={tabs[key][1]}>'
        else:
            node = f'<a href={tabs[key][1]}>'
        node += tabs[key][0] + '</a>'
        comp += node
    comp += '</div>'

def index(data):
    return HTML5(
        header = '<title>Welcome!</title>',
        body = Header('home')
    )
def about(data):
    return HTML5(
        header = '<title>Welcome!</title>',
        body = Header('about')
    )
def contact(data):
    return HTML5(
        header = '<title>Welcome!</title>',
        body = Header('contact')
    )

gen.make_page('index', index)
gen.make_page('about', about)
gen.make_page('contact', contact)
```
