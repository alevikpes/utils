# create random request header
# https://github.com/FantomNet/DDoS/blob/master/BlackHorizon.py

import random
import time

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': ['Linux x86_64', 'Linux i386'],
            'ext': ['X11'],
        },
        'windows': {
            'name': ['Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1',
                    'Windows NT.6.2'],
            'ext': ['WOW64', 'Win64; x64'],
        },
        'mac': {
            'name': ['Macintosh'],
            'ext': ['Intel Mac OS X %d_%d_%d' % (random.randint(10, 11),
                    random.randint(0, 9), random.randint(0, 5))
                    for i in range(1, 10)],
        },
    },
    'platform': {
        'webkit': {
            'name': ['AppleWebKit/%d.%d' % (random.randint(535, 537),
                        random.randint(1,36)) for i in range(1, 30)],
            'details': ['KHTML, like Gecko'],
            'extensions': ['Chrome/%d.0.%d.%d Safari/%d.%d'
                           % (random.randint(6, 32), random.randint(100, 2000),
                           random.randint(0, 100), random.randint(535, 537),
                           random.randint(1, 36)) for i in range(1, 30)] +
                          ['Version/%d.%d.%d Safari/%d.%d'
                           % (random.randint(4, 6), random.randint(0, 1),
                           random.randint(0, 9), random.randint(535, 537),
                           random.randint(1, 36)) for i in range(1, 10)],
        },
        'iexplorer': {
            'browser_info': {
                'name': ['MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b',
                         'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0'],
                'ext_pre': ['compatible', 'Windows; U'],
                'ext_post': ['Trident/%d.0' % i for i in range(4, 6)] +
                            ['.NET CLR %d.%d.%d' % (random.randint(1, 3),
                             random.randint(0, 5),
                             random.randint(1000, 30000))
                             for i in range(1, 10)],
            }
        },
        'gecko': {
            'name': ['Gecko/%d%02d%02d Firefox/%d.0'
                     % (random.randint(2001, 2010), random.randint(1,31),
                     random.randint(1,12) , random.randint(10, 25))
                     for i in range(1, 30)],
            'details': [],
            'extensions': [],
        }
    }
}


class Headers():

    _referers = [
        'http://www.google.com/?q=',
        'http://www.usatoday.com/search/results?q=',
        'http://engadget.search.aol.com/search?q=',
        'http://www.bing.com/search?q=',
        'http://search.yahoo.com/search?p=',
        'http://www.ask.com/web?q=',
        'http://search.lycos.com/web/?q=',
        'http://busca.uol.com.br/web/?q=',
        'http://us.yhs4.search.yahoo.com/yhs/search?p=',
        'http://www.dmoz.org/search/search?q=',
        'http://www.baidu.com.br/s?usm=1&rn=100&wd=',
        'http://yandex.ru/yandsearch?text=',
        'http://www.zhongsou.com/third?w=',
        'http://hksearch.timway.com/search.php?query=',
        'http://find.ezilon.com/search.php?q=',
        'http://www.sogou.com/web?query=',
        'http://api.duckduckgo.com/html/?q=',
        'http://boorow.com/Pages/site_br_aspx?query=',
    ]

    #builds random ascii string
    def buildblock(self, size):
        out_str = ''

        _LOWERCASE = list(range(97, 122))
        _UPPERCASE = list(range(65, 90))
        _NUMERIC   = list(range(48, 57))

        validChars = _LOWERCASE + _UPPERCASE + _NUMERIC
        for i in range(0, size):
            a = random.choice(validChars)
            out_str += chr(a)

        return out_str


    def generate_query_string(self, ammount=1):
        query_string = []
        for i in range(ammount):
            key = self.buildblock(random.randint(3,10))
            value = self.buildblock(random.randint(3,20))
            element = "{0}={1}".format(key, value)
            query_string.append(element)

        return '&'.join(query_string)


    def get_user_agent(self):
        # Mozilla/[version] ([system and browser information]) [platform]
        # ([platform details]) [extensions]

        ## Mozilla Version
        # hardcoded for now, almost every browser is on this version except IE6
        mozilla_version = "Mozilla/5.0"

        ## System And Browser Information
        # Choose random OS
        os = USER_AGENT_PARTS['os'][
            random.choice(list(USER_AGENT_PARTS['os']))]
        os_name = random.choice(os['name'])
        sysinfo = os_name

        # Choose random platform
        platform = USER_AGENT_PARTS['platform'][
                    random.choice(list(USER_AGENT_PARTS['platform']))]

        # Get Browser Information if available
        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']
            browser_string = random.choice(browser['name'])
            if 'ext_pre' in browser:
                browser_string = "%s; %s" % (random.choice(browser['ext_pre']),
                                             browser_string)

            sysinfo = "%s; %s" % (browser_string, sysinfo)
            if 'ext_post' in browser:
                sysinfo = "%s; %s" % (
                    sysinfo, random.choice(browser['ext_post']))

        if 'ext' in os and os['ext']:
            sysinfo = "%s; %s" % (sysinfo, random.choice(os['ext']))

        ua_string = "%s (%s)" % (mozilla_version, sysinfo)

        if 'name' in platform and platform['name']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['name']))

        if 'details' in platform and platform['details']:
            ua_string = "%s (%s)" % (
                ua_string, random.choice(platform['details'])
                if len(platform['details']) > 1
                else platform['details'][0])

        if 'extensions' in platform and platform['extensions']:
            ua_string = "%s %s" % (ua_string,
                                   random.choice(platform['extensions']))

        return ua_string


    def generate_random_headers(self):
        # Random no-cache entries
        nocache_directives = ['no-cache', 'max-age=0']
        random.shuffle(nocache_directives)
        nr_nocache = random.randint(1, (len(nocache_directives)-1))
        nocache = ', '.join(nocache_directives[:nr_nocache])

        # Random accept encoding
        accept_encoding = ['\'\'','*','identity','gzip','deflate']
        random.shuffle(accept_encoding)
        nr_encodings = random.randint(1, len(accept_encoding))
        round_encodings = accept_encoding[:nr_encodings]

        http_headers = {
            # use randomly generated user-agent
            'User-Agent': self.get_user_agent(),
#            # use a user-agent from the list
#            'User-Agent': self.get_user_agent_from_list(),
            'Cache-Control': nocache,
            'Accept-Encoding': ', '.join(round_encodings),
            'Connection': 'keep-alive',
            'Keep-Alive': str(random.randint(1,1000)),
    #        'Host': self.host,
        }

        # Randomly-added headers
        # These headers are optional and are
        # randomly sent thus making the
        # header count random and unfingerprintable
        if random.randrange(2) == 0:
            # Random accept-charset
            accept_charset = ['ISO-8859-1', 'utf-8', 'Windows-1251',
                             'ISO-8859-2', 'ISO-8859-15',]
            random.shuffle(accept_charset)
            http_headers['Accept-Charset'] = '{0},{1};q={2},*;q={3}'.format(
                    accept_charset[0],
                    accept_charset[1],round(random.random(), 1),
                    round(random.random(), 1))

        if random.randrange(2) == 0:
            # Random Referer
            url_part = self.buildblock(random.randint(5,10))
            random_referer = random.choice(self._referers) + url_part
            if random.randrange(2) == 0:
                random_referer = (random_referer + '?' +
                                  self.generate_query_string(
                                      random.randint(1, 10)))

            http_headers['Referer'] = random_referer

        if random.randrange(2) == 0:
            # Random Content-Type
            http_headers['Content-Type'] = random.choice([
                'multipart/form-data', 'application/x-url-encoded'])

        if random.randrange(2) == 0:
            # Random Cookie
            http_headers['Cookie'] = self.generate_query_string(
                random.randint(1, 5))

        # random time pause between requests
        #time.sleep(random.randint(3, 7))
        return http_headers

    def get_user_agent_from_list(self):
        ua_list = [
            ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
             'AppleWebKit/525.19 (KHTML, like Gecko) '
             'Chrome/1.0.154.53 Safari/525.19'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
             'AppleWebKit/525.19 (KHTML, like Gecko) '
             'Chrome/1.0.154.36 Safari/525.19'),
            ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
             'AppleWebKit/534.10 (KHTML, like Gecko) '
             'Chrome/7.0.540.0 Safari/534.10'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) '
             'AppleWebKit/534.4 (KHTML, like Gecko) C'
             'hrome/6.0.481.0 Safari/534.4'),
            ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US'
             ') AppleWebKit/533.4 (KHTML, like Gecko)'
             ' Chrome/5.0.375.86 Safari/533.4'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
             'AppleWebKit/532.2 (KHTML, like Gecko) C'
             'hrome/4.0.223.3 Safari/532.2'),
            ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
             'AppleWebKit/532.0 (KHTML, like Gecko) C'
             'hrome/4.0.201.1 Safari/532.0'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) '
             'AppleWebKit/532.0 (KHTML, like Gecko) C'
             'hrome/3.0.195.27 Safari/532.0'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
             'AppleWebKit/530.5 (KHTML, like Gecko) C'
             'hrome/2.0.173.1 Safari/530.5'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) '
             'AppleWebKit/534.10 (KHTML, like Gecko) '
             'Chrome/8.0.558.0 Safari/534.10'),
            ('Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleW'
             'ebKit/540.0 (KHTML,like Gecko) Chrome/9'
             '.1.0.0 Safari/540.0'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) '
             'AppleWebKit/534.14 (KHTML, like Gecko) '
             'Chrome/9.0.600.0 Safari/534.14'),
            ('Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleW'
             'ebKit/534.12 (KHTML, like Gecko) Chrome'
             '/9.0.587.0 Safari/534.12'),
            ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
             'AppleWebKit/534.13 (KHTML, like Gecko) '
             'Chrome/9.0.597.0 Safari/534.13'),
            ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) '
             'AppleWebKit/534.16 (KHTML, like Gecko) '
             'Chrome/10.0.648.11 Safari/534.16'),
            ('Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) '
             'AppleWebKit/534.20 (KHTML, like Gecko) '
             'Chrome/11.0.672.2 Safari/534.20'),
            ('Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 ('
             'KHTML, like Gecko) Chrome/14.0.792.0 Sa'
             'fari/535.1'),
            ('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 ('
             'KHTML, like Gecko) Chrome/15.0.872.0 Sa'
             'fari/535.2'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '535.7 (KHTML, like Gecko) Chrome/16.0.9'
             '12.36 Safari/535.7'),
            ('Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/'
             '535.11 (KHTML, like Gecko) Chrome/17.0.'
             '963.66 Safari/535.11'),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) A'
             'ppleWebKit/535.19 (KHTML, like Gecko) C'
             'hrome/18.0.1025.45 Safari/535.19'),
            ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/'
             '535.24 (KHTML, like Gecko) Chrome/19.0.'
             '1055.1 Safari/535.24'),
            ('Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 ('
             'KHTML, like Gecko) Chrome/20.0.1090.0 S'
             'afari/536.6'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '537.1 (KHTML, like Gecko) Chrome/22.0.1'
             '207.1 Safari/537.1'),
            ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/'
             '537.15 (KHTML, like Gecko) Chrome/24.0.'
             '1295.0 Safari/537.15'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/27.0.'
             '1453.93 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/28.0.1467.0 '
             'Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/30.0.'
             '1599.101 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/31.0.'
             '1623.0 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/34.0.'
             '1847.116 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/37.0.'
             '2062.103 Safari/537.36'),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/40.0.2214.38 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/46.0.'
             '2490.71 Safari/537.36'),
            ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/'
             '537.36 (KHTML, like Gecko) Chrome/51.0.'
             '2704.103 Safari/537.36'),
            ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; '
             'en-US; rv:1.9.1b3) Gecko/20090305 Firef'
             'ox/3.1b3 GTB5'),
            ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; '
             'ko; rv:1.9.1b2) Gecko/20081201 Firefox/'
             '3.1b2'),
            ('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8'
             '.1.12) Gecko/20080214 Firefox/2.0.0.12'),
            ('Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8'
             '.0.5) Gecko/20060819 Firefox/1.5.0.5'),
            ('Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; '
             'rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3'),
            ('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7'
             '.9) Gecko/20050711 Firefox/1.0.5'),
            ('Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) '
             'Gecko/20100720 Firefox/4.0b2'),
            ('Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/'
             '20100818 Firefox/4.0b4'),
            ('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2'
             ') Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1'),
            ('Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gec'
             'ko/20110111 Firefox/4.0b9pre'),
            ('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b'
             '9pre) Gecko/20101228 Firefox/4.0b9pre'),
            ('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a'
             '1pre) Gecko/20110324 Firefox/4.2a1pre'),
            ('Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/'
             '20100101 Firefox/5.0 (Debian)'),
            ('Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0)'
             ' Gecko/20100101 Firefox/12.0'),
            ('Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/2012'
             '0716 Firefox/15.0a2'),
            ('Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0)'
             ' Gecko/20100101 Firefox/17.0'),
            ('Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/2013'
             '0328 Firefox/21.0'),
            ('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0'
             ') Gecko/20130328 Firefox/22.0'),
            ('Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/2010'
             '0101 Firefox/25.0'),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:'
             '25.0) Gecko/20100101 Firefox/25.0'),
            ('Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/2010'
             '0101 Firefox/28.0'),
            ('Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/201'
             '00101 Firefox/30.0'),
            ('Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/2010'
             '0101 Firefox/31.0'),
        ]
        return random.choice(ua_list)
