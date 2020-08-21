def extract_domain(site):
    if site.endswith('/'):
        site = site[:-1]

    new_site = site[:site.rfind('/')]

    return new_site
