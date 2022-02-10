import django.contrib.auth.models
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from blog.models import Post
user_model = get_user_model()


register = template.Library()

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk)[:5]
  print(posts)
  return {"posts": posts, "title": "Recent Posts"}


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")

@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")


@register.filter
def author_details(author, current_user=None):
  if not isinstance(author, user_model):
    # return empty string as safe default
    return ""

  print(f"{author}, {current_user}")
  if author == current_user:
    return format_html("<strong>me</strong>")

  if author.first_name and author.last_name:
    name = escape(f"{author.first_name} {author.last_name}")
  else:
    name = escape(f"{author.username}")

  if author.email:
    email = author.email
    prefix = format_html('<a href="mailto:{}">',email)
    suffix = "</a>"
  else:
    prefix = ""
    suffix = ""

  return format_html(f"{prefix}{name}{suffix}")


