# imports - compat imports
from upyog._compat import PY2

# imports - standard imports
import os.path as osp

if PY2:
    import cgi as module_escape
else:
    import html as module_escape

# imports - module imports
from upyog.util.system import read
from upyog.util.array  import sequencify
from upyog.util.imports import import_or_raise
from upyog.log         import get_logger
from upyog.exception   import TemplateNotFoundError
from upyog.util.string import _REGEX_HTML
from upyog._compat     import iteritems, StringIO
from upyog.config      import PATH

logger = get_logger()

def _render_template_jinja(template, context = None):
    jinja2 = import_or_raise("jinja2", "Jinja2")

    with open(template, "r") as f:
        content = f.read()
    
    with StringIO() as out:
        jinja2.Template(content) \
            .stream(context) \
            .dump(out)

        return out.getvalue()

def render_template(template, context = None, dirs = [ ], **kwargs):
    """
    Renders a template. The template must be of the string format. For more 
    details, see 
    https://docs.python.org/3.4/library/string.html#string-formatting.

    :param template: Path to template file.
    :param context: The context passed to the template.
    :param dirs: Path/List of Directory Paths to search for templates.

    :return: Returns the rendered template.
    :rtype: str

    Usage::

        >>> from ccapi.template import render_template
        >>> render_template("test.html", context = dict(name = "Test"))
        'Hello, Test!'
        >>> render_template("test.html", name = "Test")
        'Hello, Test!'
        >>> render_template("foobar.html", dirs = "templates", bar = "baz")
        'foobaz'
    """
    jinja = kwargs.get("jinja", False)
    if jinja:
        return _render_template_jinja(template, context = context)

    dirs  = sequencify(dirs)
    if PATH["TEMPLATES"] not in dirs:
        dirs.append(PATH["TEMPLATES"])

    dirs = [osp.abspath(dir_) for dir_ in dirs]

    logger.info("Searching for templates within directories: %s" % dirs)

    path = None
    for dir_ in dirs:
        temp = osp.join(dir_, template)
        if osp.exists(temp):
            path = temp
            break
    
    if not path:
        as_string = kwargs.get("as_string", False)

        if as_string:
            rendered = template
        else:
            raise TemplateNotFoundError("Template %s not found." % template)
    else:
        html     = read(path)
        rendered = html

    if not context:
        context = kwargs

    if context:
        for name, item in iteritems(context):
            item = str(item)
            item = module_escape.escape(item)
            
            context[name] = item

        rendered = rendered.format(**context)
    
    return rendered