from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from compression import CompressedTextField

class Language(models.Model):
    name = models.CharField(max_length=30)

    def get_absolute_url(self):
        return "/%s/" % self.name

class SnippetManager(models.Manager):
    def top_tags(self):
        return self.model.tags.most_common().order_by('-num_times', 'name')
    
    def matches_tag(self, tag):
        return self.filter(tags__in=[tag])

class Snippet(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(User)
    description = models.CharField(max_length=300)
    tags = TaggableManager()
    last_modified = models.DateTimeField(auto_now=True)
    code = CompressedTextField()
    language = models.ForeignKey(Language)
    
    objects = SnippetManager()
    
    class Meta:
        ordering = ('-last_modified',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Snippet, self).save(*args, **kwargs)

    def get_tagstring(self):
        return ", ".join([t.name for t in self.tags.all()])

    def get_absolute_url(self):
        return "/%s/" % self.slug
    
    def __unicode__(self):
        return self.title

defaultFiddle = {
    'newFiddle': True,
    'isOwner': True
}

defaultMeta = {
    'title': 'Python Cloud IDE',
    'description': 'The Python IDE for the web. Play around with and modify live example code. Share or demonstrate solutions to problems.',
    'keywords': 'python, rapid prototyping'
}

languageMeta = {
    'python': {
        'title': 'Python Scripting for the Browser',
        'description': 'FiddleSalad is a leading provider of fast paced web development environments. FiddleSalad\'s Python to JavaScript compiler lets you develop client-side web applications in Python, in the same way Node JS lets you develop server-side applications in JavaScript. ',
        'keywords': 'client-side python, python to javascript compiler'
    },
    'coffeescript': {
        'title': 'Live CoffeeScript IDE',
        'description': 'Write CoffeeScript and preview the compiled JavaScript side-by-side. Results are updated on the fly with the compiled CoffeeScript. ',
        'keywords': 'coffeescript, preview compiled javascript, coffeescript debugging'
    },
    'javascript': {
        'title': 'JavaScript & jQuery IDE',
        'description': 'JavaScript and jQuery IDE with code completion, on-the-fly code analysis, and a hands-on learning environment. ',
        'keywords': 'javascript, javascript editor, javascript auto-complete, jquery auto-complete, javascript debugging'
    },
    'sass': {
        'title': 'SASS & Compass Editor',
        'description': 'SASS and HTML editor with sytax highlighting and code completion. Style changes are updated instantly without reloading the results. ',
        'keywords': 'sass compile'
    },
    'scss': {
        'title': 'SCSS & Compass Editor',
        'description': 'SCSS and HTML editor with syntax highlighting, CSS property auto-complete, and instant preview. ',
        'keywords': 'scss editor, sass documentation'
    },
    'less': {
        'title': 'Less CSS Editor',
        'description': 'Simplify your style sheets with LESS, an extension of CSS. Preview results and view source in separate panels on the side. ',
        'keywords': 'lesscss, lesscss ide'
    },
    'stylus': {
        'title': 'Stylus & Nib Editor',
        'description': 'Stylus and HTML editor with code and tag completion, a real-time results panel, and compiled CSS by the side. ',
        'keywords': 'stylus support, ide with stylus support'
    },
    'css': {
        'title': 'Instant CSS Coding Environment',
        'description': 'Experiment with HTML, CSS, and live preview all in flexible windows that can be dragged and resized. ',
        'keywords': 'css preview, wysiwyg css editor'
    },
    'html': {
        'title': 'HTML Editor with Preview',
        'description': 'Edit HTML with a preview panel on the side. Test the latest HTML5 tags and CSS3 styles. ',
        'keywords': 'wysiwyg web ide, wysiwyg html editor, live html editor'
    },
    'haml': {
        'title': 'HAML & CSS Editor',
        'description': 'Edit HAML with an auto-updating preview and tooltips for CSS fonts, colors, sizes, and images. ',
        'keywords': 'haml editor, wysiwyg haml editor, live haml editor'
    },
    'jade': {
        'title': 'Jade Template Language Editor',
        'description': 'Compile Jade templates to HTML and preview the result with syntax highlighting. See everything you need at once with panels for CSS, JavaScript, and Jade. ',
        'keywords': 'jade support, ide with jade support'
    },
    'coffeecup': {
        'title': 'Coffeecup Template Language Editor',
        'description': 'Coffeecup and CSS editor with syntax highlighting and live results. ',
        'keywords': 'coffeecup editor, online coffeecup editor'
    },
    'zencoding': {
        'title': 'Zen Coding',
        'description': 'Write HTML quickly using a CSS-like selector syntax. Preview document and style changes instantly. ',
        'keywords': 'zen coding, zen coding editor'
    },
}
