from apps.siteconfig.models import SiteConfiguration


def site_configuration(request):
    return {
        "site_configuration": SiteConfiguration.get_solo(),
    }
