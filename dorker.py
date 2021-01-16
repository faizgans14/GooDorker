import requests
from re import findall as cari
import random
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

CSE_TOKEN = 'partner-pub-2698861478625135:3033704849'

headers = {}
headers['Referer'] = 'https://cse.google.com/cse?cx='+CSE_TOKEN
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.'+str(random.randint(0000, 3333))+'.169 Safari/537.36'

alldomain = []

def get():
    try:
        getInfo = requests.get('https://cse.google.com/cse.js?hpg=1&cx='+CSE_TOKEN, timeout=30, headers=headers)
        try:
            csiLib = cari('"cselibVersion":\s"(.*?)",\n', getInfo.text)
            cx = cari('"cx":\s"(.*?)"', getInfo.text)
            cseToken = cari('"cse_token":\s"(.*?)",\n', getInfo.text)
            exp = cari('"exp": \["(.*?)",\s"(.*?)"\],\n', getInfo.text)[0]
            rsz = cari('"resultSetSize": "(.*?)",\n', getInfo.text)
        except:
            pass
    except:
        pass
    finally:
        return csiLib, cx, cseToken, exp, rsz
        
def dorking(dork, fullurl):
    global alldomain
    dork = urllib.parse.quote(dork)
    csiLib, cx, cseToken, exp, rsz = get()
    try:
        page = 0
        while page <= 500:
            dorker = requests.get('https://cse.google.com/cse/element/v1?rsz='+rsz[0]+'&num=10&&start='+str(page)+'&hl=en&source=gcsc&gss=.com&cselibv='+csiLib[0]+'&cx='+cx[0]+'&q='+dork+'&safe=off&cse_tok='+cseToken[0]+'&exp='+exp[0]+','+exp[1]+'&callback=google.search.cse.api16950', headers=headers)
            domain = [cari('&q=(.*?)&sa', x)[0] for x in cari('"clicktrackUrl": "(.*?)"', dorker.text)]
            if len(domain) != 0:
                print('[OK] TOTAL DOMAIN >> '+str(len(alldomain)))
                print('[DORK] '+str(dork))
                for doms in domain:
                    if (fullurl == 'y') or (fullurl == 'Y'):
                        doms = urllib.parse.unquote(doms)
                        if doms in alldomain:
                            print('[DUPLICATE] '+doms)
                        else:
                            print('[*] '+doms+' [*]')
                            save = open('result.txt', 'a')
                            save.write(doms+'\n')
                            save.close()
                            alldomain.append(doms)
                    else:
                        doms = cari('(http.?://.*?)/', doms)[0]
                        if doms in alldomain:
                            print('[DUPLICATE] '+doms)
                        else:
                            print('[*] '+doms+' [*]')
                            save = open('result.txt', 'a')
                            save.write(doms+'\n')
                            save.close()
                            alldomain.append(doms)
                        
            else:
                print('[NOT OK] NO RESULTS FOUND!!!')
                print('[DORK] '+str(dork))
                break
            page += 10
    except Exception as ex:
        print(str(ex))

def Main():
    ban = """
╔═══╗─────╔═══╗────╔╗
║╔═╗║─────╚╗╔╗║────║║
║║─╚╬══╦══╗║║║╠══╦═╣║╔╦══╦═╗
║║╔═╣╔╗║╔╗║║║║║╔╗║╔╣╚╝╣║═╣╔╝
║╚╩═║╚╝║╚╝╠╝╚╝║╚╝║║║╔╗╣║═╣║
╚═══╩══╩══╩═══╩══╩╝╚╝╚╩══╩╝ By FaizGanz14
"""
    try:
        print(ban)
        xxx = open(input('DORK ~# '), 'r').read().splitlines()
        yyy = input('Full URL Y/n : ')
    except IOError:
        Main()
    with ThreadPoolExecutor(max_workers=7) as exc:
        for targ in xxx:
            exc.submit(dorking, targ, yyy)

if __name__ == '__main__':
    Main()
