from django import template
from youtube_app.forms import user_files_Form
register=template.Library()
@register.inclusion_tag('youtube_app/basic.html')
def render_upload_form():
    form=user_files_Form()
    return{'form':form}