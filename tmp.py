#!/usr/bin/env python

from sh import ls

lda16_domains = [
'64rus.com',
'7system.ru',
'9trest-ekb.ru',
'achimgaz.ru',
'advas.ru',
'adventa.su',
'aem-avto.ru',
'agescorp.ru',
'agoracom.ru',
'agrocabel.ru',
'anderssen.ru',
'apabank.ru',
'askomkrk.ru',
'atonot.ru',
'avtoros.info',
'aybarus.ru',
'b-co.ru',
'banksbrr.ru',
'bike-centre.ru',
'bliz.ru',
'bosforkmv.ru',
'breez.ru',
'centrenergo.ru',
'cnlog.ru',
'dcli.ru',
'easystep.ru',
'entrade.ru',
'estima.ru',
'evromix.ru',
'fgup-ohrana.ru',
'gbu.asueirc.ru',
'gourji.com',
'grisbank.ru',
'holod-nsk.ru',
'iksid.ru',
'ingcoma.com',
'itscan.ru',
'katran72.com',
'kazkedr.ru',
'klimat.city',
'km-profil.ru',
'kolomnamoloko.ru',
'kolomzavod.ru',
'kr-o-wn.ru',
'kuzmiha.ru',
'loginof.ru',
'lrp-hotel.ru',
'mail.kimkor.ru',
'med-el.ru',
'mediana-filter.ru',
'mkskom.ru',
'mosproektstroy.com',
'msvkok.ru',
'niiekran.ru',
'novolrus47.ru',
'ntces.ru',
'nzslp.ru',
'ogorodov.org',
'omt-ohe.ru',
'osy.ru',
'oysters.ru',
'papa-carlo.ru',
'pos18.nichost.ru',
'posuda.ru',
'r-color.ru',
'rallinn.ru',
'rostender.info',
'sangrup.ru',
'scent.ru',
'scrh.ru',
'sibir-zitar.ru',
'snowworld.ru',
'sro77.ru',
'statum.com.ru',
'stroy-sg.ru',
'syntechrus.ru',
'tdkremlin.ru',
'test-systems.ru',
'tk-ptg.ru',
'tkvprok.ru',
'tornado24.ru',
'tpak.ru',
'trust-finance.com',
'tupperware.su',
'uds.ru',
'uez.ru',
'uo-minusinsk.ru',
'vci.ru',
'vector-kaluga.ru',
'velpharm.ru',
'ventar.ru',
'vlbb.ru',
'vw-alt.ru',
'wayg.ru',
'yakitoriya.ru',
'zaodss.ru',
'zhukadmin.ru'
]

real_domains = []

for letter in ls('/home/mail/').split():
	for domain in ls('/home/mail/'+letter+'/').split():
		#print domain
		real_domains.append(domain)
#print real_domains


missing=[]
for domain in lda16_domains:
	if domain in real_domains:
		real_domains.remove(domain)
	else:
		missing.append(domain)
