from urllib.parse import urlparse
from tld import get_tld

allowedTLDs = ['co.uk', 'us', 'org', 'ca', 'au', 'ie', 'ky', 'mp', 'ms', 'nz', 'sh', 'uk', 'com', 'org', 'net', 'int',
               'edu', 'gov', 'mil']
allowedSUBs = ['www', 'mail', 'remote', 'blog', 'webmail', 'server', 'ns1', 'ns2', 'smtp', 'secure', 'vpn', 'm', 'shop',
               'ftp', 'mail2', 'test', 'portal', 'ns', 'ww1', 'host', 'support', 'dev', 'web', 'bbs', 'ww42', 'mx',
               'email', 'cloud', '1', 'mail1', '2', 'forum', 'owa', 'www2', 'gw', 'admin', 'store', 'mx1', 'cdn', 'api',
               'exchange', 'app', 'gov', 'en', '']


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get subdomain name(mail.name.example.com)

def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


def getLangFolder(url):
    if url.split('/').__len__() > 1:
        langFolder = url.split('/')[1]
    else:
        return True

    if langFolder in allowedSUBs or langFolder is '':
        return True
    else:
        return False


def isAllowed(url):
    langFolder = getLangFolder(url)
    try:
        url = get_tld(url, fail_silently=True, as_object=True)
        if url.tld in allowedTLDs:
            if not langFolder:
                return False
            if url.subdomain in allowedSUBs:
                return True
        else:
            return False
    except:
        return False


