"""
Helper form baseclasses for bootstrap styling.
"""

from django.forms import Form, ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.template import Context, Template


class _BootstrapFormBase(object):
    """
    Baseclass for BootstrapForm and BootstrapModelForm.

    Based on:
        http://duganchen.ca/rendering-django-forms-for-the-twitter-bootstrap/

    """

    def __unicode__(self):
        context = Context({'form': self})
        template = Template(self.template)
        return template.render(context)

    template = \
        u'''
            {% for field in form %}
                <div class="control-group {% if field.errors %}error{% endif %}">
                    <label class="control-label">{{ field.label }}</label>
                    <div class="controls">
                        {{ field }}<span class="help-inline">{{ field.errors|first }}</span>
                    </div>
                </div>
            {% endfor %}
        '''


class BootstrapForm(_BootstrapFormBase, Form):
    """
    Form that is styled for Bootstrap.
    """


class BootstrapModelForm(_BootstrapFormBase, ModelForm):
    """
    ModelForm that is styled for Bootstrap.
    """


class BootstrapUserCreationForm(_BootstrapFormBase, UserCreationForm):
    """
    Bootstrap style version of django.contrib.auth.forms.UserCreationForm
    """


class BootstrapPasswordChangeForm(_BootstrapFormBase, PasswordChangeForm):
    """
    Bootstrap style version of django.contrib.auth.forms.PasswordChangeForm
    """
