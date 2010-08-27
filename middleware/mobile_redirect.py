import re

agents_list = [
    'Nokia','bMOT','^LGE?b','SonyEricsson',
    'Ericsson','BlackBerry','DoCoMo','Symbian',
    'Windows CE','NetFront','Klondike','PalmOS',
    'PalmSource','portalmm','S[CG]H-','bSAGEM',
    'SEC-','jBrowser-WAP','Mitsu','Panasonic-',
    'SAMSUNG-','Samsung-','Sendo','SHARP-',
    'Vodaphone','BenQ','iPAQ','AvantGo',
    'Go.Web','Sanyo-','AUDIOVOX','PG-',
    'CDM[-d]','^KDDI-','^SIE-','TSM[-d]',
    '^KWC-','WAP','^KGT [NC]','iPhone', 'Android'
]

def is_mobile(user_agent):
    if not user_agent:
        return False
    for agent in agents_list:
        if re.search(agent, user_agent):
            return True
    return False

class MobileRedirect(object):
    def process_request(self, request):
        if not request.session.get('checked_ua', False):
            if is_mobile(request.META.get('HTTP_USER_AGENT', None)):
                request.session['is_mobile'] = True
            else:
                request.session['is_mobile'] = False
            request.session['checked_ua'] = True
        return None
