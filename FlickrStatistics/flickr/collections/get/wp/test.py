import sys
import xmlrpclib
from pyblog import WordPress

sBlogId = '729aee542766'

def main(*argv):
    oBlog = WordPress('http://ilegeul.livius.net/xmlrpc.php', 'ilegeul', 'wordpressilg')
    
    if False:
        pages = oBlog.get_page_list()
        for dPage in pages:
            print dPage
    
    dPage = oBlog.get_page(476, sBlogId)
    #print dPage
    print dPage['description']
    
    sTitle = dPage['title']  # mandatory
    sSlug = dPage['wp_slug'] # mandatory
    sDescription = dPage['description'] + ' baburiba '
    
    dContent = {}
    dContent['description'] = sDescription
    dContent['title'] = sTitle
    dContent['wp_slug'] = sSlug
    
    oRet = oBlog.edit_page(476, dContent, True, sBlogId)
    print oRet
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

