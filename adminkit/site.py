import types
from django.conf import settings
from django.contrib.admin import AdminSite
from adminkit import views
from adminkit.panels import AllModelsPanel


def setup(site):
    """Define custom templates and wrap default
    views with extended ones.
    """
    setup_views(site)
    setup_templates(site)


def setup_templates(site):
    """Setup custom templates for admin site.
    """
    site.index_template = AdminkitSite.index_template
    site.login_template = AdminkitSite.login_template
    site.logout_template = AdminkitSite.logout_template
    site.password_change_template = AdminkitSite.password_change_template
    site.password_change_done_template = AdminkitSite.password_change_done_template


def setup_views(site):
    """Setup custom view methods for admin site.
    """
    if hasattr(site, 'index_base'):
        raise Exception("Site %s was already setup!" % str(site))
    site.index_base = site.index
    site.index = types.MethodType(views.index, site)
    site.get_panels = types.MethodType(get_panels, site)


def get_panels(site, request):
    """Default ``get_panels`` method for site -
    returns list of panel objects for dashboard.
    """
    panels_classes = settings.ADMINKIT_INDEX.get('panels', [])
    panels = []
    if panels_classes:
        for panel in panels_classes:
            panel_mod, panel_cls = panel.rsplit('.', 1)
            module = __import__(panel_mod, fromlist=[panel_cls])
            panels.append(getattr(module, panel_cls)(site, request))
    else:
        panels.append(AllModelsPanel(site, request))
    return panels


class AdminkitSite(AdminSite):
    """Base class for AdminKit site. You can use it to setup
    custom admin interface from scratch. Probably you should not
    use it if you need only basic customizations.
    """
    index_template = 'adminkit/index.html'
    login_template = 'adminkit/login.html'
    logout_template = 'adminkit/logout.html'
    password_change_template = 'adminkit/password_change.html'
    password_change_done_template = 'adminkit/password_change_done.html'

    def get_panels(self, request):
        """Panels for admin dashboard.
        """
        return get_panels(self, request)
