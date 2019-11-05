import re
import orodja
import os

#Imam tri glavne urlje-za vsako gorovje. Njihovi htmlji hranijo urlje s povezavo na stran s podatki za posamezno goro. Končni html se bo torej nanašal le na eno goro.
MAPA1 = "zajeti-podatki"
MAPA2 = "obdelani-podatki"

URL_JULIJSKE_ALPE = 'https://www.hribi.net/gorovje/julijske_alpe/1' #seznam gor v Julijskih Alpah
URL_KAMNIŠKO_SAVINJSKE_ALPE = 'https://www.hribi.net/gorovje/kamnisko_savinjske_alpe/3' #seznam gor v Kamniških in Savinjskih Alpah
URL_KARAVANKE = 'https://www.hribi.net/gorovje/karavanke/11' #seznam gor v Karavankah
splosni_url = [URL_JULIJSKE_ALPE, URL_KAMNIŠKO_SAVINJSKE_ALPE, URL_KARAVANKE] #seznam url-jev, s katerih bom pridobila url-je in html-je spletnih strani s podatki za posamezno goro




#blok v html gorovja, v katerem se nahaja url za posamezno goro
vzorec_bloka_za_url = re.compile( 
    r'tr bgcolor.*?'
    r'bgcolor="#cccccc"></td></tr></table></td></tr>',
    flags=re.DOTALL
)

#url za posamezno goro
vzorec_url = re.compile(
    r'<a\shref="(?P<url>.*?)">&nbsp.*?</a>',
    flags=re.DOTALL
)



#podatki o posamezni točki
vzorec_tocke = re.compile(
    r'.*?<td class="naslov1"><b>&nbsp;&nbsp;<h1>(?P<ime>.*?)</h1></b></td>.+?'
    r'<b>Gorovje:</b> <a\s.*?>(?P<gorovje>.*?)</a>.+?'
    r'<b>Višina:</b> (?P<visina>\d*)&nbsp;m.+?'
    r'<b>Vrsta:</b>(?P<vrsta>.*?)</td>.+?'
    r'<b>Ogledov:</b>(?P<ogledi>.\d+?)</td>.+?'
    r'<b>Priljubljenost:</b>.*?\((?P<priljubljenost>\d+?)\. mesto\)</td>.+?'
    r'<b>Število poti:</b> <a class="moder".*?>(?P<stevilo_poti>\d*?)</a>',
    flags=re.DOTALL
)

#da pridobim ime in višino bližnjih točk
vzorec_tock_v_okolici = re.compile(
    r"<a class=moder href='/gora/.*?>(?P<bliznja_planinska_tocka>.*?)\s\((?P<visina_bliznje_planinske_tocke>\d+)m\)</a>",
    flags=re.DOTALL
)

vzorec_poti = re.compile(
    r"<tr bgcolor=\W#.{6}\W><td><a href='/izlet/.*?'>(?P<pot>.*?)"
    r"</a></td><td><a href='/izlet/.*?'>.*?</a></td><td><a href='/izlet/.*?'>(?P<zahtevnost>.*?)</a>",
    flags=re.DOTALL
)

#.*?<td class="naslov1"><b>&nbsp;&nbsp;<h1>(?P<ime>.*?)</h1></b></td>.+?<b>Gorovje:</b> <a\s.*?>(?P<gorovje>.*?)</a>.+?<b>Višina:</b> (?P<visina>\d*)&nbsp;m.+?<b>Vrsta:</b>(?P<vrsta>.*?)</td>.+?<b>Ogledov:</b>(?P<ogledi>.\d+?)</td>.+?<b>Priljubljenost:</b>.*?\((?P<priljubljenost>\d+?)\. mesto\)</td>.+?<b>Število poti:</b> <a class="moder".*?>(?P<stevilo_poti>\d*?)</a>

#vzorec, ki se pojavi med nekaterimi imeni planinskih točk, ki pa ga ne smem prenesti
vzorec_med_oklepaji_v_imenu = re.compile(
    r'&nbsp;',
    flags=re.DOTALL
)



def izloci_bliznje_tocke(niz):
    okolica = []
    for tocka in vzorec_tock_v_okolici.finditer(niz):
        okolica.append({
            'bližnja planinska točka': tocka.groupdict()['bliznja_planinska_tocka'].strip(),
            'višina bližnje točke (m)': int(tocka.groupdict()['visina_bliznje_planinske_tocke']),
        })
    return okolica

def izloci_poti(niz):
    poti = []
    for pot in vzorec_poti.finditer(niz):
        ime_poti = vzorec_med_oklepaji_v_imenu.sub(" ", pot.groupdict()['pot'])
        poti.append({
            'pot': ime_poti.strip(),
            'zahtevnost': pot.groupdict()['zahtevnost'].strip(),
        })
    return poti

def izloci_tocko(vsebina):
    for t in vzorec_tocke.finditer(vsebina):
        #je tako ali tako samo ena noter
        #print(tocka['ime'])
        tocka = {}

        tocka['ime'] = t.groupdict()['ime']
        tocka['gorovje'] = t.groupdict()['gorovje']
        tocka['višina (m)'] = int(t.groupdict()['visina'])
        if t.groupdict()['vrsta'].strip().split(", ") is [""]:
            tocka['vrsta'] = None 
        else:
            tocka['vrsta'] = t.groupdict()['vrsta'].strip().split(", ")
        tocka['število ogledov'] = int(t.groupdict()['ogledi'])
        tocka['priljubljenost (mesto)'] = int(t.groupdict()['priljubljenost'])
        tocka["število planinskih točk v okolici"] = len(izloci_bliznje_tocke(vsebina))
        tocka['število poti'] = int(t.groupdict()['stevilo_poti'])
    
        tocka['planinske točke v okolici'] = izloci_bliznje_tocke(vsebina)
        tocka['poti'] = izloci_poti(vsebina)

    #print(tocka)
    return tocka

def izloci_gnezdene_podatke(tocke):
    bliznje_tocke, poti, vrste = [], [], []

    for tocka in tocke:

        for bliznja_tocka in tocka.pop('planinske točke v okolici'): #seznam slovarjev, torej je bliznja_tocka en slovar
            bliznje_tocke.append({
                'ime bližnje točke': bliznja_tocka["bližnja planinska točka"],
                'višina bližnje točke (m)': bliznja_tocka['višina bližnje točke (m)'],
                'ime planinske točke': tocka["ime"],
            })
        for pot in tocka.pop('poti'): #seznam poti -> pot je slovar
            poti.append({
                'pot': pot["pot"],
                'zahtevnost': pot['zahtevnost'],
                'ime planinske točke': tocka["ime"],
            })

        if tocka['vrsta'] is None :
            vrste.append({
                'točka': tocka['ime'], 
                'vrsta': None,
            })
            tocka.pop('vrsta')
        else:
            for vrsta in tocka.pop('vrsta'):
                vrste.append({
                    'točka': tocka['ime'], 
                    'vrsta': vrsta,
                })

    vrste.sort(key=lambda vrsta: vrsta['točka'])
    bliznje_tocke.sort(key=lambda tocka: (tocka['ime planinske točke'], - (tocka['višina bližnje točke (m)']), tocka['ime bližnje točke']))
    poti.sort(key=lambda pot: (pot['ime planinske točke'], pot['pot']))

    return bliznje_tocke, poti, vrste

 
    
    

def koda_za_gorovje(url, st):
    ime_datoteke = 'gorovje-{}'.format(st)
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka_za_url.findall(vsebina):
        for naslov in vzorec_url.findall(blok):
            #print(naslov)
            print("https://www.hribi.net/" + naslov)
            yield "https://www.hribi.net/" + naslov


def koda_za_posamezno_tocko(url, st):
    
    datoteka = 'planinska-tocka-{}'.format(st)
    ime_datoteke = os.path.join(MAPA1, datoteka)
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    return izloci_tocko(vsebina)




planinske_tocke = []
y = 0
for x, splosen_url in enumerate(splosni_url):
    for url in koda_za_gorovje(splosen_url, x):
        tocka = koda_za_posamezno_tocko(url, y)
        planinske_tocke.append(tocka)
        y += 1
        

#print(planinske_tocke)
planinske_tocke.sort(key=lambda tocka: (tocka['gorovje'], - (tocka['višina (m)']), tocka['ime']))

ime_dat = os.path.join(MAPA2, "planinske-tocke.json")
orodja.zapisi_json(planinske_tocke, ime_dat)

bliznje_tocke, poti, vrste = izloci_gnezdene_podatke(planinske_tocke)
#print(bliznje_tocke)
#print(poti)
#print(vrste)
#imamo vse v jsonu, samo še csv

orodja.zapisi_csv(
    planinske_tocke,
    ['ime', 'gorovje', 'višina (m)', 'število ogledov', 'priljubljenost (mesto)', "število planinskih točk v okolici", 'število poti'],
    os.path.join(MAPA2, "planinske-tocke.csv" )
)
#os.path.join(MAPA2, "planinske-tocke.csv")
orodja.zapisi_csv(bliznje_tocke, ['ime planinske točke', 'ime bližnje točke', 'višina bližnje točke (m)'], os.path.join(MAPA2, "bliznje-tocke.csv"))
orodja.zapisi_csv(poti, ['ime planinske točke', 'pot', 'zahtevnost'], os.path.join(MAPA2, "poti.csv" ))
orodja.zapisi_csv(vrste, ['točka', 'vrsta'], os.path.join(MAPA2, "vrste.csv"))

#Kar dolgo tole dela, je to prav?