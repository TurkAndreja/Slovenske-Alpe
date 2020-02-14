Slovenske Alpe
==============

Analizirala bom vsaj 300 točk na planinskih poteh po Sloveniji na območju Alp. Podatke bom pridobila na strani [Hribi.net] (https://www.hribi.net/gorovja).

Podatki o posamezni planinski točki:
- gorovje
- višina
- vrsta
- priljubljenost
- število poti in njihova zahtevnost
- število ogledov
- gore v okolici in njihova višina

Hipoteze:
1. Ali največ točk na planinski poti v Alpah predstavljajo vrhovi?
2. Ali je število poti in ogledov povezanih s priljubljenostjo planinske točke?
3. Ali je priljubljenost obiskov planinske točke povezana s številom gor v okolici?
4. Ali je priljubljenost povezana z višino točke?
5. Ali lahko preko višine predvidemo vrsto planinske točke?

Repozitorij vsebuje štiri CSV datoteke (in json slovar vseh podatkov skupaj):
1. planinske-tocke.csv vsebuje podatke o imenu in višini planinske točke, kateremu gorovju pripada, koliko poti vodi nanjo, koliko planinskih točk se nahaja okoli nje v radiju dveh kilometrov, na katerem mestu je glede priljubljenosti in število ogledov spletne strani, ki je namenjena eksplicitno tej planinski točki
2. vrste.csv za vsako planinsko točko pove, kakšne vrste je (posamezna je lahko več vrst)
3. poti.csv hrani podatke o različnih poteh, ki vodijo na posamezno točko in njihove zahtevnosti
4. bliznje-tocke.csv pa za vsako točko beleži bližje točke (v radiju dveh kilometrov) ter pove še višino posamezne bližnje točke

V mapi obdelani-podatki se nahaja tudi analiza podatkov.
