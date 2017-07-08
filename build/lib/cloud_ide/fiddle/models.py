from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from compression import CompressedTextField
from django.db.models import permalink, Count
from django.utils.translation import ugettext_lazy as _

class Language(models.Model):
    name = models.CharField(max_length=30)

    @permalink
    def get_absolute_url(self):
        return ('fiddle_language_detail', (), {'slug': self.name})

class SnippetManager(models.Manager):
    def top_authors(self):
        return User.objects.annotate(score=Count('snippet')).order_by('-score', 'username')
    def top_tags(self):
        return self.model.tags.most_common().order_by('-num_times', 'name')

    def matches_tag(self, tag):
        return self.filter(tags__in=[tag])

class Snippet(models.Model):
    title = models.CharField(_('Title'), max_length=80)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(User)
    description = models.CharField(_('Description'), max_length=300)
    tags = TaggableManager(_('Tags'))
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
        if Language.objects.count() > 1:
            return "/%s/%s/" % (self.language.name, self.slug)
        else:
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
        'description': 'Write CoffeeScript and preview the compiled JavaScript side-by-side. HTML DOM is refreshed automatically as you write CoffeeScript. ',
        'keywords': 'coffeescript ide, coffeescript, coffee script ide, coffeescript fiddle, coffeescript debugging'
    },
    'opal': {
        'title': 'Live Opalrb Editor',
        'description': 'Try Opal, a Ruby to JavaScript compiler which includes an implementation of the Ruby corelib. ',
        'keywords': 'opal ide, opalrb, opal ruby ide'
    },
    'typescript': {
        'title': 'TypeScript Web IDE',
        'description': 'Write TypeScript and preview the compiled JavaScript side-by-side. HTML DOM is refreshed automatically as you write TypeScript. ',
        'keywords': 'typescript ide, typescript, type script ide, typescript fiddle'
    },
    'babel': {
        'title': 'Live Babel + JSX Editor',
        'description': 'Write JSX/ES6 and preview the compiled JavaScript side-by-side. HTML DOM is refreshed automatically as you type. ',
        'keywords': 'jsx ide, jsx, es6 ide, jsx fiddle'
    },
    'javascript': {
        'title': 'JavaScript & jQuery IDE',
        'description': 'JavaScript and jQuery IDE with code completion, on-the-fly code analysis, and a hands-on learning environment. ',
        'keywords': 'javascript fiddle, jquery ide, javascript editor'
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
        'keywords': 'less css editor, lesscss, lesscss ide'
    },
    'stylus': {
        'title': 'Stylus & Nib Editor',
        'description': 'Stylus and HTML editor with code and tag completion, a real-time results panel, and compiled CSS by the side. ',
        'keywords': 'stylus support, ide with stylus support'
    },
    'css': {
        'title': 'CSS Playground',
        'description': 'Experiment with HTML, CSS, and live preview all in flexible windows that can be dragged and resized. ',
        'keywords': 'css fiddle, css preview, wysiwyg css editor'
    },
    'html': {
        'title': 'HTML Editor with Preview',
        'description': 'Edit HTML with a preview panel on the side. Test the latest HTML5 tags and CSS3 styles. See everything you need at once with panels for CSS, JavaScript, and HTML. ',
        'keywords': 'wysiwyg web ide, wysiwyg html editor, live html editor'
    },
    'haml': {
        'title': 'HAML & CSS Editor',
        'description': 'Edit HAML with an auto-updating preview and tooltips for CSS fonts, colors, sizes, and images. ',
        'keywords': 'haml editor, wysiwyg haml editor, live haml editor'
    },
    'jade': {
        'title': 'Jade Template Language Editor',
        'description': 'Compile Jade templates to HTML and preview the result with syntax highlighting. Convert HTML to Jade with the built-in HTML to Jade converter.  ',
        'keywords': 'jade support, ide with jade support'
    },
    'coffeekup': {
        'title': 'Coffeekup Template Language Editor',
        'description': 'Coffeekup and CSS editor with syntax highlighting and live results. ',
        'keywords': 'coffeekup editor, online coffeekup editor'
    },
    'roy': {
        'title': 'Programming with Roy',
        'description': 'Compile Roy to JavaScript. Debug and run Roy in an interactive playground along with HTML and CSS. ',
        'keywords': 'roy editor, roy syntax highlighting, roy compiler, roy language'
    },
    'markdown': {
        'title': 'Online Markdown Editor',
        'description': 'Edit Markdown live with preview, syntax highlighting. ',
        'keywords': 'markdown editor, online markdown editor'
    },
    'zencoding': {
        'title': 'Zen Coding',
        'description': 'Write HTML quickly using a CSS-like selector syntax. Preview document and style changes instantly. ',
        'keywords': 'zen coding, zen coding editor'
    },
}

