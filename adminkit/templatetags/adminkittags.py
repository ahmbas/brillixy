from django.conf import settings
from django import template

register = template.Library()


@register.filter
def regroup_apps(apps, groups):
    if groups:
        # ``app_url`` is like '/admin/auth/', so tag is 'auth'
        apps_tags = map(lambda app: app['app_url'].split('/')[-2], apps)
        apps_regroup = []
        for group_name, group in groups:
            base_index = None
            for app_tag in group:
                try:
                    app_index = apps_tags.index(app_tag)
                except ValueError:
                    continue
                
                if not base_index is None:
                    app = apps[app_index]
                    apps_regroup[-1]['models'] += app['models']
                else:
                    base_index = app_index
                    app = apps[base_index]
                    app['name'] = group_name
                    apps_regroup.append(app)

        return apps_regroup
    else:
        return apps


@register.filter
def user_nice_name(user):
    for method in ('get_short_name', 'get_username', 'get_full_name'):
        if hasattr(user, method):
            name = getattr(user, method)()
            if name:
                return name
    return user.username


@register.simple_tag
def branding_logo():
    default = '%sadminkit/logo.png' % settings.STATIC_URL
    return settings.ADMINKIT_BRANDING.get('logo', default)


# @register.simple_tag
# def branding_title():
#     return settings.ADMINKIT_BRANDING.get('title', u"ADMIN")