import django.template
from django.contrib.auth.models import User
from django.utils.html import format_html
from blog.models import Post

register = django.template.Library()

@register.filter
def author_details(author, current_user=None):
  if not isinstance(author, User):
    return ""

  if author == current_user :
    return format_html("<strong>me</strong>")
  if author.first_name and author.last_name :
    name = f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"
  
  if author.email:
      prefix = format_html('<a href="mailto:{}">', author.email)
      suffix = format_html("</a>")
  else:
      prefix = ""
      suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag(takes_context=True)
def row(context, extra_classes=""):
  return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
  return format_html('</div>')

@register.simple_tag(takes_context=True)
def col(context, extra_classes=""):
  return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
  return format_html('</div>')

import logging
logger = logging.getLogger(__name__)

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk)[:5]
  logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
  return {'title': 'Recent Posts', 'posts': posts}