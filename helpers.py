def extract_domain(site):
    site = site[site.find('w'):]
    slash = site.find('/')
    new_site = site[:slash]
    return new_site
