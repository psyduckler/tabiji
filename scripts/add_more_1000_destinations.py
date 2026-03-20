from __future__ import annotations
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'find' / 'destinations.json'
FALLBACK_PHOTO = 'https://img.tabiji.ai/owl-logo.png'
TARGET_ADD = 1000

TSV = '''
Lillehammer	Norway	Europe	mountain
Bodø	Norway	Europe	city
Narvik	Norway	Europe	mountain
Alta	Norway	Europe	city
Andøya	Norway	Europe	island
Kjerag	Norway	Europe	mountain
Flåm	Norway	Europe	coast
Loen	Norway	Europe	mountain
Åndalsnes	Norway	Europe	mountain
Helgeland Coast	Norway	Europe	coast
Jyväskylä	Finland	Europe	city
Savonlinna	Finland	Europe	city
Kuusamo	Finland	Europe	mountain
Oulu	Finland	Europe	city
Inari	Finland	Europe	lake
Hanko	Finland	Europe	coast
Rauma	Finland	Europe	cultural
Ylläs	Finland	Europe	mountain
Pallas-Yllästunturi	Finland	Europe	park
Kuopio	Finland	Europe	city
Umeå	Sweden	Europe	city
Kalmar	Sweden	Europe	city
Ystad	Sweden	Europe	coast
Småland	Sweden	Europe	roadtrip
Höga Kusten	Sweden	Europe	coast
Vadstena	Sweden	Europe	cultural
Öland	Sweden	Europe	island
Falun	Sweden	Europe	city
Västerås	Sweden	Europe	city
Sundsvall	Sweden	Europe	city
Sønderjylland	Denmark	Europe	roadtrip
Aalborg	Denmark	Europe	city
Ebeltoft	Denmark	Europe	coast
North Jutland Coast	Denmark	Europe	coast
Fanø	Denmark	Europe	island
Mols Bjerge	Denmark	Europe	park
Elsinore	Denmark	Europe	city
Kolding	Denmark	Europe	city
Silkeborg	Denmark	Europe	lake
Frederiksø	Denmark	Europe	island
Belfast Coast	Northern Ireland	Europe	coast
Fermanagh Lakelands	Northern Ireland	Europe	lake
Newcastle Mournes	Northern Ireland	Europe	mountain
Donegal Coast	Ireland	Europe	coast
Kerry Cliffs	Ireland	Europe	coast
Connemara	Ireland	Europe	mountain
Achill Island	Ireland	Europe	island
Waterford	Ireland	Europe	city
Clonakilty	Ireland	Europe	coast
Glendalough	Ireland	Europe	cultural
West Cork	Ireland	Europe	coast
Limerick	Ireland	Europe	city
Mayo Coast	Ireland	Europe	coast
Burren	Ireland	Europe	park
Kilkee	Ireland	Europe	coast
Norfolk Broads	England	Europe	lake
Whitby	England	Europe	coast
Norwich	England	Europe	city
Durham	England	Europe	city
Jurassic Coast	England	Europe	coast
Brighton and Hove	England	Europe	coast
Bristol Harbourside	England	Europe	city
Isle of Wight	England	Europe	island
South Downs	England	Europe	park
Exmoor	England	Europe	park
Salisbury	England	Europe	city
Canal Bath	England	Europe	cultural
North York Moors	England	Europe	park
Southwold	England	Europe	coast
Winchester	England	Europe	city
Falmouth	England	Europe	coast
Newquay	England	Europe	coast
Padstow	England	Europe	coast
Lincoln	England	Europe	city
Cambridgeshire Fens	England	Europe	roadtrip
Stirling	Scotland	Europe	city
Glencoe	Scotland	Europe	mountain
Fort William	Scotland	Europe	city
Oban	Scotland	Europe	coast
Dundee	Scotland	Europe	city
Perthshire	Scotland	Europe	roadtrip
Culross	Scotland	Europe	cultural
Arran	Scotland	Europe	island
Mull	Scotland	Europe	island
North Coast 500	Scotland	Europe	roadtrip
Tobermory	Scotland	Europe	coast
Aviemore	Scotland	Europe	mountain
Isle of Harris	Scotland	Europe	island
Galloway Forest Park	Scotland	Europe	park
Pitlochry	Scotland	Europe	city
Brecon Beacons	Wales	Europe	mountain
Tenby	Wales	Europe	coast
Anglesey	Wales	Europe	island
Gower Peninsula	Wales	Europe	coast
Conwy	Wales	Europe	city
Hay-on-Wye	Wales	Europe	cultural
Llyn Peninsula	Wales	Europe	coast
Wye Valley	Wales	Europe	roadtrip
Monmouthshire	Wales	Europe	roadtrip
Ceredigion Coast	Wales	Europe	coast
Sark	Channel Islands	Europe	island
Alderney	Channel Islands	Europe	island
Dinan	France	Europe	city
Saint-Malo	France	Europe	coast
Honfleur	France	Europe	coast
Étretat	France	Europe	coast
Rouen	France	Europe	city
Le Havre	France	Europe	city
Deauville	France	Europe	coast
Vannes	France	Europe	city
Quimper	France	Europe	city
Concarneau	France	Europe	coast
Belle-Île-en-Mer	France	Europe	island
La Rochelle	France	Europe	coast
Île de Ré	France	Europe	island
Périgueux	France	Europe	city
Sarlat-la-Canéda	France	Europe	city
Albi	France	Europe	city
Gorges du Verdon	France	Europe	park
Menton	France	Europe	coast
Èze	France	Europe	cultural
Saint-Paul-de-Vence	France	Europe	cultural
Morzine	France	Europe	mountain
Megève	France	Europe	mountain
Grenoble	France	Europe	city
Clermont-Ferrand	France	Europe	city
Auvergne Volcanoes	France	Europe	park
Nîmes	France	Europe	city
Uzès	France	Europe	city
Saint-Rémy-de-Provence	France	Europe	city
Luberon	France	Europe	roadtrip
Bandol	France	Europe	coast
La Ciotat	France	Europe	coast
Hyères	France	Europe	coast
Porquerolles	France	Europe	island
Toulon	France	Europe	city
Mulhouse	France	Europe	city
Eguisheim	France	Europe	cultural
Riquewihr	France	Europe	cultural
Beaune	France	Europe	city
Dijon Hinterland	France	Europe	roadtrip
Jura Mountains France	France	Europe	mountain
Cantal	France	Europe	mountain
Chartres	France	Europe	city
Le Mans	France	Europe	city
Amboise	France	Europe	city
Saumur	France	Europe	city
Blois	France	Europe	city
Cahors	France	Europe	city
Lourdes	France	Europe	city
Pau	France	Europe	city
Perpignan	France	Europe	city
Collioure	France	Europe	coast
Sete	France	Europe	coast
Ardèche Gorges	France	Europe	park
Bastia	France	Europe	city
Bonifacio	France	Europe	coast
Ajaccio	France	Europe	city
Perugia Hills	Italy	Europe	roadtrip
Mantua	Italy	Europe	city
Ferrara	Italy	Europe	city
Padua	Italy	Europe	city
Treviso	Italy	Europe	city
Vicenza	Italy	Europe	city
Bassano del Grappa	Italy	Europe	city
Monferrato	Italy	Europe	roadtrip
Langhe	Italy	Europe	roadtrip
Asti	Italy	Europe	city
Arezzo	Italy	Europe	city
Volterra	Italy	Europe	city
Montepulciano	Italy	Europe	city
Pienza	Italy	Europe	city
Maremma	Italy	Europe	coast
Argentario	Italy	Europe	coast
Civita di Bagnoregio	Italy	Europe	cultural
Assisi	Italy	Europe	city
Gubbio	Italy	Europe	city
Spoleto	Italy	Europe	city
Trento	Italy	Europe	city
Merano	Italy	Europe	mountain
Alpe di Siusi	Italy	Europe	mountain
Val Gardena	Italy	Europe	mountain
Cortina d'Ampezzo	Italy	Europe	mountain
Belluno	Italy	Europe	city
Mantello Lakes	Italy	Europe	lake
Lago Maggiore	Italy	Europe	lake
Orta San Giulio	Italy	Europe	lake
Lecce Old Town	Italy	Europe	cultural
Polignano a Mare	Italy	Europe	coast
Monopoli	Italy	Europe	coast
Alberobello	Italy	Europe	cultural
Ostuni	Italy	Europe	city
Vieste	Italy	Europe	coast
Gargano	Italy	Europe	park
Tropea	Italy	Europe	coast
Scilla	Italy	Europe	coast
Cefalù	Italy	Europe	coast
Noto	Italy	Europe	city
Siracusa	Italy	Europe	city
Ragusa	Italy	Europe	city
Agrigento	Italy	Europe	cultural
San Vito Lo Capo	Italy	Europe	coast
Favignana	Italy	Europe	island
Pantelleria	Italy	Europe	island
Ponza	Italy	Europe	island
Elba Coast	Italy	Europe	coast
Ascoli Piceno	Italy	Europe	city
Ancona Riviera	Italy	Europe	coast
Rimini Hinterland	Italy	Europe	roadtrip
Brescia	Italy	Europe	city
Cremona	Italy	Europe	city
Varenna	Italy	Europe	coast
Como Hills	Italy	Europe	roadtrip
Sopot	Poland	Europe	coast
Szczecin	Poland	Europe	city
Bieszczady	Poland	Europe	mountain
Kłodzko Valley	Poland	Europe	roadtrip
Kazimierz Dolny	Poland	Europe	city
Gdynia	Poland	Europe	coast
Sandomierz	Poland	Europe	city
Kaszuby	Poland	Europe	lake
Słowiński National Park	Poland	Europe	park
Karpacz	Poland	Europe	mountain
Bydgoszcz	Poland	Europe	city
Beskidy	Poland	Europe	mountain
Bielsko-Biała	Poland	Europe	city
Opole	Poland	Europe	city
Biebrza National Park	Poland	Europe	park
Rzeszów	Poland	Europe	city
Poznań Lakes	Poland	Europe	lake
Masovia Countryside	Poland	Europe	roadtrip
Nałęczów	Poland	Europe	city
Hel Coast	Poland	Europe	coast
Bruges Canals	Belgium	Europe	cultural
Ghent Canals	Belgium	Europe	cultural
Mechelen	Belgium	Europe	city
Tournai	Belgium	Europe	city
Durbuy	Belgium	Europe	city
Spa	Belgium	Europe	city
Ardennes Belgium	Belgium	Europe	mountain
Ostend	Belgium	Europe	coast
Knokke-Heist	Belgium	Europe	coast
Liège	Belgium	Europe	city
Brabant Countryside	Belgium	Europe	roadtrip
Bouillon	Belgium	Europe	cultural
Middelburg	Netherlands	Europe	city
Giethoorn	Netherlands	Europe	lake
Zaanse Schans	Netherlands	Europe	cultural
Breda	Netherlands	Europe	city
Den Bosch	Netherlands	Europe	city
Zwolle	Netherlands	Europe	city
Amersfoort	Netherlands	Europe	city
Arnhem	Netherlands	Europe	city
Nijmegen	Netherlands	Europe	city
Frisian Islands	Netherlands	Europe	island
Terschelling	Netherlands	Europe	island
Vlieland	Netherlands	Europe	island
Domburg	Netherlands	Europe	coast
South Limburg	Netherlands	Europe	roadtrip
Zeeland Coast	Netherlands	Europe	coast
Dordrecht	Netherlands	Europe	city
Alkmaar	Netherlands	Europe	city
Ameland	Netherlands	Europe	island
Schiermonnikoog	Netherlands	Europe	island
Bourtange	Netherlands	Europe	cultural
Porto Santo	Portugal	Europe	island
São Jorge	Portugal	Europe	island
Faial	Portugal	Europe	island
Terceira	Portugal	Europe	island
Ponta Delgada	Portugal	Europe	city
Setúbal	Portugal	Europe	coast
Comporta	Portugal	Europe	coast
Peniche	Portugal	Europe	coast
Ericeira	Portugal	Europe	coast
Viana do Castelo	Portugal	Europe	coast
Guimarães	Portugal	Europe	city
Monsaraz	Portugal	Europe	cultural
Tavira	Portugal	Europe	coast
Sagres	Portugal	Europe	coast
Lagos Portugal	Portugal	Europe	coast
Vilamoura	Portugal	Europe	coast
Aljezur	Portugal	Europe	coast
Gerês	Portugal	Europe	park
Tomar	Portugal	Europe	city
Portalegre	Portugal	Europe	city
Aveleda Wine Country	Portugal	Europe	roadtrip
Funchal	Portugal	Europe	city
Santana Madeira	Portugal	Europe	cultural
Bilbao Coast	Spain	Europe	coast
Zamora	Spain	Europe	city
León Spain	Spain	Europe	city
Burgos	Spain	Europe	city
Salamanca	Spain	Europe	city
Segovia	Spain	Europe	city
Ávila	Spain	Europe	city
Cuenca Spain	Spain	Europe	city
Almería	Spain	Europe	coast
Cabo de Gata	Spain	Europe	park
Tarifa	Spain	Europe	coast
Jerez de la Frontera	Spain	Europe	city
Córdoba Patios	Spain	Europe	cultural
Jaén	Spain	Europe	city
Úbeda	Spain	Europe	cultural
Baeza	Spain	Europe	cultural
Sanlúcar de Barrameda	Spain	Europe	coast
Rías Baixas	Spain	Europe	coast
A Coruña	Spain	Europe	city
Vigo	Spain	Europe	city
Ourense	Spain	Europe	city
Costa da Morte	Spain	Europe	coast
Cíes Islands	Spain	Europe	island
Pontevedra	Spain	Europe	city
Lugo	Spain	Europe	city
Cantabria Coast	Spain	Europe	coast
Santander	Spain	Europe	city
Comillas	Spain	Europe	city
Oviedo	Spain	Europe	city
Gijón	Spain	Europe	coast
La Palma Ridge	Spain	Europe	mountain
El Hierro	Spain	Europe	island
La Graciosa	Spain	Europe	island
Huesca Pyrenees	Spain	Europe	mountain
Jaca	Spain	Europe	city
Cadaqués Coast	Spain	Europe	coast
Besalú	Spain	Europe	cultural
Mallorca Tramuntana	Spain	Europe	mountain
Mahón	Spain	Europe	city
Ciutadella	Spain	Europe	city
Las Palmas	Spain	Europe	city
Puerto de la Cruz	Spain	Europe	coast
Costa Blanca North	Spain	Europe	coast
Alicante	Spain	Europe	city
Val d'Aran	Spain	Europe	mountain
La Gomera Trails	Spain	Europe	mountain
Pamplona	Spain	Europe	city
Logroño	Spain	Europe	city
Vitoria-Gasteiz	Spain	Europe	city
Soria	Spain	Europe	city
Sierra de Grazalema	Spain	Europe	park
Sierra Nevada Spain	Spain	Europe	mountain
Ribeira Sacra	Spain	Europe	roadtrip
Cáceres	Spain	Europe	city
Mérida Spain	Spain	Europe	city
Peñíscola	Spain	Europe	coast
Murcia	Spain	Europe	city
Cartagena Spain	Spain	Europe	city
Andorra la Vella	Andorra	Europe	city
Madriu Valley	Andorra	Europe	mountain
Port de Sóller	Spain	Europe	coast
Huelva Coast	Spain	Europe	coast
Bamberg Rivers	Germany	Europe	cultural
Freiburg im Breisgau	Germany	Europe	city
Garmisch-Partenkirchen	Germany	Europe	mountain
Lake Constance Germany	Germany	Europe	lake
Tübingen	Germany	Europe	city
Ulm	Germany	Europe	city
Regensburg	Germany	Europe	city
Passau	Germany	Europe	city
Würzburg	Germany	Europe	city
Erfurt	Germany	Europe	city
Jena	Germany	Europe	city
Quedlinburg	Germany	Europe	city
Harz Mountains	Germany	Europe	mountain
Usedom	Germany	Europe	island
Warnemünde	Germany	Europe	coast
Schwerin	Germany	Europe	city
Müritz	Germany	Europe	lake
Monschau	Germany	Europe	city
Cochem	Germany	Europe	city
Koblenz	Germany	Europe	city
Berchtesgaden Lakes	Germany	Europe	lake
Allgäu	Germany	Europe	mountain
Füssen	Germany	Europe	city
Mainz	Germany	Europe	city
Speyer	Germany	Europe	city
Rostock	Germany	Europe	city
Ahr Valley	Germany	Europe	roadtrip
Lüneburg	Germany	Europe	city
Bodensee Alps Edge	Germany	Europe	roadtrip
Weimar	Germany	Europe	city
Goslar	Germany	Europe	city
Rügen Coast	Germany	Europe	coast
Saarbrücken	Germany	Europe	city
Heidelberg Hills	Germany	Europe	roadtrip
Marburg	Germany	Europe	city
Potsdam Lakes	Germany	Europe	lake
Dresden Elbland	Germany	Europe	roadtrip
Münster	Germany	Europe	city
Bonn	Germany	Europe	city
Pilsen Beer Trails	Czech Republic	Europe	roadtrip
Liberec	Czech Republic	Europe	city
Bohemian Paradise	Czech Republic	Europe	park
Třebíč	Czech Republic	Europe	city
Znojmo	Czech Republic	Europe	city
Jeseníky	Czech Republic	Europe	mountain
Pardubice	Czech Republic	Europe	city
Hradec Králové	Czech Republic	Europe	city
Kroměříž	Czech Republic	Europe	city
South Bohemia	Czech Republic	Europe	roadtrip
Moravian Karst	Czech Republic	Europe	park
Jihlava	Czech Republic	Europe	city
Broumov	Czech Republic	Europe	city
Třeboň	Czech Republic	Europe	lake
Františkovy Lázně	Czech Republic	Europe	city
Pálava	Czech Republic	Europe	mountain
Levoča	Slovakia	Europe	city
Bardejov	Slovakia	Europe	city
Liptov	Slovakia	Europe	roadtrip
Poprad	Slovakia	Europe	city
Vlkolínec	Slovakia	Europe	cultural
Nitra	Slovakia	Europe	city
Orava	Slovakia	Europe	roadtrip
Trenčín	Slovakia	Europe	city
Spiš Castle	Slovakia	Europe	cultural
Low Tatras	Slovakia	Europe	mountain
Sopron	Hungary	Europe	city
Tokaj	Hungary	Europe	roadtrip
Szeged	Hungary	Europe	city
Keszthely	Hungary	Europe	lake
Hollókő	Hungary	Europe	cultural
Győr	Hungary	Europe	city
Tihany	Hungary	Europe	lake
Kecskemét	Hungary	Europe	city
Aggtelek	Hungary	Europe	park
Villány	Hungary	Europe	roadtrip
Białystok	Poland	Europe	city
Maribor Wine Hills	Slovenia	Europe	roadtrip
Kranjska Gora	Slovenia	Europe	mountain
Ptuj	Slovenia	Europe	city
Velika Planina	Slovenia	Europe	mountain
Vipava Valley	Slovenia	Europe	roadtrip
Celje	Slovenia	Europe	city
Izola	Slovenia	Europe	coast
Kobarid	Slovenia	Europe	mountain
Logar Valley	Slovenia	Europe	mountain
Banja Luka	Bosnia and Herzegovina	Europe	city
Una River Bosnia	Bosnia and Herzegovina	Europe	park
Počitelj	Bosnia and Herzegovina	Europe	cultural
Travnik	Bosnia and Herzegovina	Europe	city
Konjic	Bosnia and Herzegovina	Europe	mountain
Jahorina	Bosnia and Herzegovina	Europe	mountain
Višegrad	Bosnia and Herzegovina	Europe	cultural
Neum	Bosnia and Herzegovina	Europe	coast
Bijambare	Bosnia and Herzegovina	Europe	park
Bjelašnica	Bosnia and Herzegovina	Europe	mountain
Kolašin	Montenegro	Europe	mountain
Tivat	Montenegro	Europe	coast
Herceg Novi	Montenegro	Europe	coast
Lake Skadar Montenegro	Montenegro	Europe	lake
Bar Montenegro	Montenegro	Europe	coast
Žabljak	Montenegro	Europe	mountain
Cetinje	Montenegro	Europe	city
Biogradska Gora	Montenegro	Europe	park
Virpazar	Montenegro	Europe	lake
Ada Bojana	Montenegro	Europe	coast
Subotica	Serbia	Europe	city
Zlatibor	Serbia	Europe	mountain
Drvengrad	Serbia	Europe	cultural
Uvac Canyon	Serbia	Europe	park
Vršac	Serbia	Europe	city
Fruška Gora	Serbia	Europe	park
Sremski Karlovci	Serbia	Europe	city
Kragujevac	Serbia	Europe	city
Golubac	Serbia	Europe	cultural
Tara Drina Valley	Serbia	Europe	roadtrip
Nišava Gorge	Serbia	Europe	mountain
Kruševac	Serbia	Europe	city
Šar Mountains	Kosovo	Europe	mountain
Rugova Gorge	Kosovo	Europe	mountain
Gjakova	Kosovo	Europe	city
Gračanica	Kosovo	Europe	cultural
Mitrovica	Kosovo	Europe	city
Tetovo	North Macedonia	Europe	city
Kruševo	North Macedonia	Europe	city
Prespa Lake	North Macedonia	Europe	lake
Kratovo	North Macedonia	Europe	city
Kokino	North Macedonia	Europe	cultural
Pelister National Park	North Macedonia	Europe	park
Dojran	North Macedonia	Europe	lake
Struga	North Macedonia	Europe	city
Prilep	North Macedonia	Europe	city
Kratka Valley	North Macedonia	Europe	roadtrip
Vlora	Albania	Europe	coast
Himarë	Albania	Europe	coast
Dhërmi	Albania	Europe	coast
Korçë	Albania	Europe	city
Pogradec	Albania	Europe	lake
Llogara Pass	Albania	Europe	mountain
Përmet	Albania	Europe	city
Apollonia Albania	Albania	Europe	cultural
Krujë	Albania	Europe	city
Lake Koman	Albania	Europe	lake
Vlorë Riviera	Albania	Europe	roadtrip
Sarandë	Albania	Europe	coast
Burgas	Bulgaria	Europe	city
Nessebar	Bulgaria	Europe	cultural
Sozopol	Bulgaria	Europe	coast
Melnik Bulgaria	Bulgaria	Europe	city
Rila Lakes	Bulgaria	Europe	mountain
Belogradchik	Bulgaria	Europe	cultural
Pirin Mountains	Bulgaria	Europe	mountain
Kazanlak	Bulgaria	Europe	city
Kavarna	Bulgaria	Europe	coast
Plovdiv Hills	Bulgaria	Europe	roadtrip
Suceava	Romania	Europe	city
Bucovina Monasteries	Romania	Europe	cultural
Oradea	Romania	Europe	city
Alba Iulia	Romania	Europe	city
Apuseni Mountains	Romania	Europe	mountain
Danube Delta Romania	Romania	Europe	park
Biertan	Romania	Europe	cultural
Piatra Neamț	Romania	Europe	city
Transfăgărășan	Romania	Europe	roadtrip
Mamaia	Romania	Europe	coast
Bistrița	Romania	Europe	city
Bran	Romania	Europe	cultural
Maramureș Valleys	Romania	Europe	roadtrip
Visby Walls	Sweden	Europe	cultural
Thun	Switzerland	Europe	lake
Fribourg Switzerland	Switzerland	Europe	city
Valais Vineyards	Switzerland	Europe	roadtrip
Engadin	Switzerland	Europe	mountain
Zug	Switzerland	Europe	city
Neuchâtel	Switzerland	Europe	city
Aletsch Arena	Switzerland	Europe	mountain
Verbier	Switzerland	Europe	mountain
Appenzell Trails	Switzerland	Europe	roadtrip
Lauterbrunnen	Switzerland	Europe	mountain
Brienz	Switzerland	Europe	lake
St. Moritz Lakes	Switzerland	Europe	lake
Sion	Switzerland	Europe	city
Ascona	Switzerland	Europe	lake
Bad Ragaz	Switzerland	Europe	city
Rhine Gorge Switzerland	Switzerland	Europe	mountain
Wengen	Switzerland	Europe	mountain
Gruyères	Switzerland	Europe	cultural
Murten	Switzerland	Europe	city
Klagenfurt	Austria	Europe	city
Hallstatt Hinterland	Austria	Europe	roadtrip
Bregenz	Austria	Europe	lake
Seefeld	Austria	Europe	mountain
Alpbach	Austria	Europe	mountain
Schladming	Austria	Europe	mountain
Mariazell	Austria	Europe	city
Krems an der Donau	Austria	Europe	city
Salzkammergut	Austria	Europe	lake
St. Anton	Austria	Europe	mountain
Mayrhofen	Austria	Europe	mountain
Dürnstein	Austria	Europe	cultural
Villach	Austria	Europe	city
Bad Ischl	Austria	Europe	city
Eisenstadt	Austria	Europe	city
Innsbruck Villages	Austria	Europe	roadtrip
Hafnarfjörður	Iceland	Europe	city
Egilsstaðir	Iceland	Europe	city
Skaftafell	Iceland	Europe	park
Reykjanes Peninsula	Iceland	Europe	coast
Hveragerði	Iceland	Europe	city
Vestmannaeyjar	Iceland	Europe	island
Blue Lagoon Iceland	Iceland	Europe	lake
Skagafjörður	Iceland	Europe	coast
Kirkjubæjarklaustur	Iceland	Europe	city
Hólmavík	Iceland	Europe	coast
Lago Maggiore Switzerland	Switzerland	Europe	lake
Göreme	Turkey	Asia	cultural
Şirince	Turkey	Asia	cultural
Bozcaada	Turkey	Asia	island
Datça	Turkey	Asia	coast
Didim	Turkey	Asia	coast
Amasra	Turkey	Asia	coast
Amasya	Turkey	Asia	city
Şanlıurfa	Turkey	Asia	city
Dalyan Turkey	Turkey	Asia	coast
Gökçeada	Turkey	Asia	island
Bergama	Turkey	Asia	cultural
Kaş Peninsula	Turkey	Asia	coast
Side	Turkey	Asia	coast
Alanya	Turkey	Asia	coast
Assos Turkey	Turkey	Asia	cultural
Selçuk	Turkey	Asia	city
Patara	Turkey	Asia	coast
Adana	Turkey	Asia	city
Kars	Turkey	Asia	city
Rize Highlands	Turkey	Asia	mountain
Erzurum	Turkey	Asia	city
Mersin	Turkey	Asia	coast
Göbekli Tepe	Turkey	Asia	cultural
Mudurnu	Turkey	Asia	city
Abant	Turkey	Asia	lake
Bursa Coast	Turkey	Asia	roadtrip
Kars Plateau	Turkey	Asia	roadtrip
Akyaka	Turkey	Asia	coast
Ayvalık	Turkey	Asia	coast
Foça	Turkey	Asia	coast
Bozburun	Turkey	Asia	coast
Azerbaijan Mountains	Azerbaijan	Asia	mountain
Quba	Azerbaijan	Asia	mountain
Khinalug	Azerbaijan	Asia	mountain
Naftalan	Azerbaijan	Asia	city
Nakhchivan	Azerbaijan	Asia	city
Mingachevir	Azerbaijan	Asia	lake
Gabala	Azerbaijan	Asia	mountain
Lahij	Azerbaijan	Asia	cultural
Absheron Peninsula	Azerbaijan	Asia	coast
Nabran	Azerbaijan	Asia	coast
Stepantsminda	Georgia	Asia	mountain
Borjomi	Georgia	Asia	mountain
Akhaltsikhe	Georgia	Asia	city
Telavi	Georgia	Asia	city
Ushguli	Georgia	Asia	mountain
Gudauri	Georgia	Asia	mountain
Mestia	Georgia	Asia	mountain
Signagi	Georgia	Asia	cultural
David Gareja	Georgia	Asia	cultural
Adjara Highlands	Georgia	Asia	mountain
Dilijan Forest	Armenia	Asia	park
Jermuk	Armenia	Asia	mountain
Goris	Armenia	Asia	city
Areni	Armenia	Asia	roadtrip
Garni	Armenia	Asia	cultural
Lori Province	Armenia	Asia	mountain
Aparan	Armenia	Asia	city
Vanadzor	Armenia	Asia	city
Tatev Highlands	Armenia	Asia	mountain
Aghveran	Armenia	Asia	mountain
Karakol Valley	Kyrgyzstan	Asia	roadtrip
Bokonbayevo	Kyrgyzstan	Asia	lake
Altyn Arashan	Kyrgyzstan	Asia	mountain
Arslanbob	Kyrgyzstan	Asia	mountain
Naryn	Kyrgyzstan	Asia	city
Tash Rabat	Kyrgyzstan	Asia	cultural
Sary-Chelek	Kyrgyzstan	Asia	lake
At-Bashy	Kyrgyzstan	Asia	mountain
Kyzyl-Oi	Kyrgyzstan	Asia	mountain
Cholpon-Ata	Kyrgyzstan	Asia	lake
Isfara	Tajikistan	Asia	city
Panjakent	Tajikistan	Asia	city
Iskanderkul	Tajikistan	Asia	lake
Wakhan Corridor	Tajikistan	Asia	roadtrip
Khorog	Tajikistan	Asia	mountain
Fann Lakes	Tajikistan	Asia	lake
Istaravshan	Tajikistan	Asia	city
Hisor	Tajikistan	Asia	cultural
Zarafshan Valley	Tajikistan	Asia	roadtrip
Bulunkul	Tajikistan	Asia	lake
Aktau Mountains	Kazakhstan	Asia	mountain
Alakol	Kazakhstan	Asia	lake
Burabay	Kazakhstan	Asia	park
Mangystau	Kazakhstan	Asia	desert
Turgen Gorge	Kazakhstan	Asia	mountain
Bayanaul	Kazakhstan	Asia	park
Taraz	Kazakhstan	Asia	city
Lake Kaindy	Kazakhstan	Asia	lake
Bozzhyra	Kazakhstan	Asia	desert
Altai Kazakhstan	Kazakhstan	Asia	mountain
Khiva Desert Edge	Uzbekistan	Asia	desert
Navoiy	Uzbekistan	Asia	city
Termez	Uzbekistan	Asia	city
Shahrisabz	Uzbekistan	Asia	cultural
Zaamin	Uzbekistan	Asia	park
Aydarkul	Uzbekistan	Asia	lake
Margilan	Uzbekistan	Asia	city
Rishtan	Uzbekistan	Asia	cultural
Kokand	Uzbekistan	Asia	city
Chimgan	Uzbekistan	Asia	mountain
Turkmenbashi	Turkmenistan	Asia	coast
Ashgabat	Turkmenistan	Asia	city
Konye-Urgench	Turkmenistan	Asia	cultural
Darvaza	Turkmenistan	Asia	desert
Mary Turkmenistan	Turkmenistan	Asia	city
Merv	Turkmenistan	Asia	cultural
Balkanabat	Turkmenistan	Asia	city
Kow Ata	Turkmenistan	Asia	lake
Yangykala	Turkmenistan	Asia	desert
Awaza	Turkmenistan	Asia	coast
Bandar Abbas	Iran	Asia	coast
Kerman	Iran	Asia	city
Isfahan	Iran	Asia	city
Persepolis	Iran	Asia	cultural
Qom	Iran	Asia	city
Rasht	Iran	Asia	city
Gorgan	Iran	Asia	city
Kish Island	Iran	Asia	island
Lut Desert	Iran	Asia	desert
Abyaneh	Iran	Asia	cultural
Tabas	Iran	Asia	desert
Anzali Lagoon	Iran	Asia	lake
Hamadan	Iran	Asia	city
Meybod	Iran	Asia	city
Urmia	Iran	Asia	lake
Kermanshah	Iran	Asia	city
Chabahar	Iran	Asia	coast
Ramsar	Iran	Asia	coast
Qazvin	Iran	Asia	city
Ardabil	Iran	Asia	city
Bam Iran	Iran	Asia	cultural
Kerman Desert Route	Iran	Asia	roadtrip
Qeshm Coast	Iran	Asia	coast
Bishapur	Iran	Asia	cultural
Babol	Iran	Asia	city
Masouleh Forest	Iran	Asia	mountain
Muscat Coast	Oman	Asia	coast
Jebel Shams	Oman	Asia	mountain
Misfat Al Abriyeen	Oman	Asia	cultural
Bahla	Oman	Asia	cultural
Daymaniyat Islands	Oman	Asia	island
Wadi Bani Awf	Oman	Asia	mountain
Masirah Island	Oman	Asia	island
Duqm	Oman	Asia	coast
Rustaq	Oman	Asia	city
Dhofar Mountains	Oman	Asia	mountain
Sohar	Oman	Asia	city
Quriyat	Oman	Asia	coast
Jabal Samhan	Oman	Asia	mountain
Yiti	Oman	Asia	coast
Bimmah Sinkhole	Oman	Asia	lake
Al Batinah Coast	Oman	Asia	roadtrip
Khasab Fjords	Oman	Asia	coast
Abha Highlands	Saudi Arabia	Asia	mountain
Al Baha	Saudi Arabia	Asia	mountain
Jazan	Saudi Arabia	Asia	coast
Tabuk	Saudi Arabia	Asia	city
Farasan Islands	Saudi Arabia	Asia	island
Taif Highlands	Saudi Arabia	Asia	mountain
Al Ahsa	Saudi Arabia	Asia	cultural
Yanbu	Saudi Arabia	Asia	coast
Hegra	Saudi Arabia	Asia	cultural
Jubail	Saudi Arabia	Asia	coast
Asir National Park	Saudi Arabia	Asia	park
Buraidah	Saudi Arabia	Asia	city
Al Khobar	Saudi Arabia	Asia	city
Wadi Disah	Saudi Arabia	Asia	mountain
Al Qassim Farms	Saudi Arabia	Asia	roadtrip
Muharraq Pearling Trail	Bahrain	Asia	cultural
Amwaj Islands	Bahrain	Asia	island
Sakhir Desert	Bahrain	Asia	desert
Bahrain Fort	Bahrain	Asia	cultural
Riffa	Bahrain	Asia	city
Zallaq	Bahrain	Asia	coast
Al Jasra	Bahrain	Asia	cultural
Hawar Islands	Bahrain	Asia	island
Budaiya	Bahrain	Asia	coast
A'ali	Bahrain	Asia	city
Al Wakrah	Qatar	Asia	coast
The Pearl Doha	Qatar	Asia	city
Khor Al Adaid	Qatar	Asia	desert
Al Khor	Qatar	Asia	coast
Lusail	Qatar	Asia	city
Mesaieed Dunes	Qatar	Asia	desert
Dukhan	Qatar	Asia	coast
Souq Waqif Quarter	Qatar	Asia	cultural
Zekreet	Qatar	Asia	desert
Katara Waterfront	Qatar	Asia	coast
Kuwait City Seafront	Kuwait	Asia	coast
Al Jahra	Kuwait	Asia	city
Kuwait Bay	Kuwait	Asia	coast
Al Khiran	Kuwait	Asia	coast
Kabd Desert	Kuwait	Asia	desert
Salmiya	Kuwait	Asia	city
Mubarak Al Kabeer	Kuwait	Asia	city
Bubiyan Island	Kuwait	Asia	island
Kuwait Desert Camp Belt	Kuwait	Asia	roadtrip
Fintas	Kuwait	Asia	coast
Aqaba Gulf	Jordan	Asia	coast
Wadi Dana	Jordan	Asia	mountain
Salt Jordan	Jordan	Asia	city
Ajloun	Jordan	Asia	mountain
Irbid	Jordan	Asia	city
Wadi Rum Trails	Jordan	Asia	desert
Karak Jordan	Jordan	Asia	cultural
Ma'in Hot Springs	Jordan	Asia	lake
Umm Qais	Jordan	Asia	cultural
Amman Citadel Quarter	Jordan	Asia	cultural
Haifa Bay	Israel	Asia	coast
Acre	Israel	Asia	cultural
Tiberias	Israel	Asia	lake
Golan Heights	Israel	Asia	mountain
Negev Desert	Israel	Asia	desert
Mitzpe Ramon	Israel	Asia	desert
Safed	Israel	Asia	city
Caesarea	Israel	Asia	cultural
Ein Gedi	Israel	Asia	park
Jaffa	Israel	Asia	cultural
Jericho Oasis	Palestine	Asia	desert
Nablus	Palestine	Asia	city
Hebron	Palestine	Asia	city
Birzeit	Palestine	Asia	city
Bethany Beyond	Palestine	Asia	cultural
Jerusalem Hills Palestine	Palestine	Asia	mountain
Aida Valley	Palestine	Asia	roadtrip
Gaza Coast	Palestine	Asia	coast
Sebastia	Palestine	Asia	cultural
Taybeh	Palestine	Asia	city
Tripoli Lebanon	Lebanon	Asia	city
Sidon	Lebanon	Asia	coast
Tyre Lebanon	Lebanon	Asia	coast
Qadisha Valley	Lebanon	Asia	mountain
Bcharre	Lebanon	Asia	mountain
Jeita	Lebanon	Asia	cultural
Chouf Mountains	Lebanon	Asia	mountain
Aley	Lebanon	Asia	mountain
Zahle	Lebanon	Asia	city
Akkar Coast	Lebanon	Asia	coast
Erbil Citadel	Iraq	Asia	cultural
Duhok	Iraq	Asia	mountain
Karbala	Iraq	Asia	city
Basra	Iraq	Asia	city
Mosul	Iraq	Asia	city
Hatra	Iraq	Asia	cultural
Marshes of Iraq	Iraq	Asia	park
Babylon	Iraq	Asia	cultural
Amadiya	Iraq	Asia	mountain
Kirkuk	Iraq	Asia	city
Socotra Coast	Yemen	Asia	coast
Hadramaut	Yemen	Asia	cultural
Al Mukalla	Yemen	Asia	coast
Shibam	Yemen	Asia	cultural
Taiz	Yemen	Asia	city
Ibb Highlands	Yemen	Asia	mountain
Mocha	Yemen	Asia	coast
Wadi Dawan	Yemen	Asia	roadtrip
Sana'a Old City	Yemen	Asia	cultural
Hajjah Mountains	Yemen	Asia	mountain
Paro	Bhutan	Asia	city
Trongsa	Bhutan	Asia	cultural
Haa Valley	Bhutan	Asia	mountain
Trongsa Highlands	Bhutan	Asia	mountain
Mongar	Bhutan	Asia	city
Trong Heritage Route	Bhutan	Asia	roadtrip
Trashigang	Bhutan	Asia	city
Trongsa Dzong Belt	Bhutan	Asia	cultural
Lhuntse	Bhutan	Asia	mountain
Gasa	Bhutan	Asia	mountain
Kathmandu Valley	Nepal	Asia	cultural
Nagarkot Ridge	Nepal	Asia	mountain
Janakpur	Nepal	Asia	city
Ilam	Nepal	Asia	mountain
Rara Lake	Nepal	Asia	lake
Ghandruk	Nepal	Asia	mountain
Tansen	Nepal	Asia	city
Bardia National Park	Nepal	Asia	park
Namche Bazaar	Nepal	Asia	mountain
Dhulikhel	Nepal	Asia	mountain
Bhairahawa	Nepal	Asia	city
Langtang Valley	Nepal	Asia	mountain
Gorkha	Nepal	Asia	city
Phewa Lakeside	Nepal	Asia	lake
Rupandehi Plains	Nepal	Asia	roadtrip
Shimla Hills	India	Asia	mountain
Tawang	India	Asia	mountain
Ziro Valley	India	Asia	mountain
Shillong	India	Asia	city
Cherrapunji	India	Asia	mountain
Majuli	India	Asia	island
Pelling	India	Asia	mountain
Gangtok	India	Asia	city
Kalimpong	India	Asia	mountain
Almora	India	Asia	mountain
Nainital	India	Asia	lake
Kausani	India	Asia	mountain
Haridwar	India	Asia	city
Mussoorie	India	Asia	mountain
Auli	India	Asia	mountain
Jibhi	India	Asia	mountain
McLeod Ganj	India	Asia	mountain
Palampur	India	Asia	mountain
Kullu Valley	India	Asia	mountain
Chandigarh	India	Asia	city
Jammu	India	Asia	city
Gulmarg	India	Asia	mountain
Pahalgam	India	Asia	mountain
Sonamarg	India	Asia	mountain
Amritsar Heritage Quarter	India	Asia	cultural
Bikaner	India	Asia	city
Mount Abu	India	Asia	mountain
Jaisalmer Dunes	India	Asia	desert
Bundi	India	Asia	city
Chittorgarh	India	Asia	cultural
Ranakpur	India	Asia	cultural
Kumbhalgarh	India	Asia	cultural
Jodhpur Desert Edge	India	Asia	roadtrip
Gwalior	India	Asia	city
Khajuraho Temples	India	Asia	cultural
Mandu	India	Asia	cultural
Pachmarhi	India	Asia	mountain
Maheshwar	India	Asia	city
Bhopal Lakes	India	Asia	lake
Aurangabad	India	Asia	city
Ajanta	India	Asia	cultural
Ellora	India	Asia	cultural
Nashik	India	Asia	city
Lonavala	India	Asia	mountain
Mahabaleshwar	India	Asia	mountain
Alibaug	India	Asia	coast
Ratnagiri	India	Asia	coast
Ganpatipule	India	Asia	coast
Gokarna	India	Asia	coast
Coorg	India	Asia	mountain
Kabini	India	Asia	park
Hampi Boulders	India	Asia	cultural
Badami	India	Asia	cultural
Mangalore	India	Asia	coast
Bekal	India	Asia	coast
Varkala	India	Asia	coast
Kumarakom	India	Asia	lake
Wayanad	India	Asia	park
Madurai	India	Asia	city
Kodaikanal	India	Asia	mountain
Ooty	India	Asia	mountain
Rameswaram	India	Asia	coast
Pondicherry Coast	India	Asia	coast
Visakhapatnam	India	Asia	coast
Araku Valley	India	Asia	mountain
Vijayawada	India	Asia	city
Warangal	India	Asia	city
Diu	India	Asia	island
Gir National Park	India	Asia	park
Dwarka	India	Asia	coast
Saputara	India	Asia	mountain
Mandvi	India	Asia	coast
Bhubaneswar	India	Asia	city
Puri	India	Asia	coast
Konark	India	Asia	cultural
Darjeeling Tea Hills	India	Asia	roadtrip
Sundarbans Delta	India	Asia	park
Murshidabad	India	Asia	city
Bishnupur	India	Asia	cultural
Jamshedpur	India	Asia	city
Netarhat	India	Asia	mountain
Patna	India	Asia	city
Rajgir	India	Asia	cultural
Bodh Gaya	India	Asia	cultural
Kanha National Park	India	Asia	park
Bandhavgarh	India	Asia	park
Tadoba	India	Asia	park
Dandeli	India	Asia	park
Rann of Kutch	India	Asia	desert
Sakleshpur	India	Asia	mountain
Ranthambore Fort Belt	India	Asia	roadtrip
Murree	Pakistan	Asia	mountain
Naran Kaghan	Pakistan	Asia	mountain
Neelum Valley	Pakistan	Asia	mountain
Gilgit	Pakistan	Asia	city
Khaplu	Pakistan	Asia	mountain
Passu	Pakistan	Asia	mountain
Attabad Lake	Pakistan	Asia	lake
Mohenjo-daro	Pakistan	Asia	cultural
Thatta	Pakistan	Asia	city
Peshawar	Pakistan	Asia	city
Chitral	Pakistan	Asia	mountain
Kalash Valleys	Pakistan	Asia	mountain
Malam Jabba	Pakistan	Asia	mountain
Karimabad	Pakistan	Asia	mountain
Deosai	Pakistan	Asia	park
Ormara	Pakistan	Asia	coast
Gwadar	Pakistan	Asia	coast
Karakoram Highway	Pakistan	Asia	roadtrip
Taxila	Pakistan	Asia	cultural
Larkana	Pakistan	Asia	city
Lahore Walled City	Pakistan	Asia	cultural
Cox's Bazar	Bangladesh	Asia	coast
Sundarbans Bangladesh	Bangladesh	Asia	park
Sylhet	Bangladesh	Asia	city
Srimangal	Bangladesh	Asia	mountain
Rangamati	Bangladesh	Asia	lake
Bandarban	Bangladesh	Asia	mountain
Rajshahi	Bangladesh	Asia	city
Khulna	Bangladesh	Asia	city
Bagerhat	Bangladesh	Asia	cultural
Saint Martin's Island	Bangladesh	Asia	island
Dhaka Old City	Bangladesh	Asia	cultural
Paharpur	Bangladesh	Asia	cultural
Comilla	Bangladesh	Asia	city
Kuakata	Bangladesh	Asia	coast
Moulvibazar	Bangladesh	Asia	mountain
Anuradhapura	Sri Lanka	Asia	cultural
Kandy Highlands	Sri Lanka	Asia	mountain
Ella	Sri Lanka	Asia	mountain
Horton Plains	Sri Lanka	Asia	park
Bentota	Sri Lanka	Asia	coast
Kalpitiya	Sri Lanka	Asia	coast
Haputale	Sri Lanka	Asia	mountain
Negombo	Sri Lanka	Asia	coast
Mannar	Sri Lanka	Asia	coast
Koggala	Sri Lanka	Asia	coast
Ratnapura	Sri Lanka	Asia	city
Dambulla	Sri Lanka	Asia	cultural
Batticaloa	Sri Lanka	Asia	coast
Kitulgala	Sri Lanka	Asia	mountain
Nilaveli	Sri Lanka	Asia	coast
Pai Canyon Belt	Thailand	Asia	mountain
Mae Sariang	Thailand	Asia	mountain
Sangkhlaburi	Thailand	Asia	cultural
Loei	Thailand	Asia	mountain
Nan	Thailand	Asia	city
Chiang Khan	Thailand	Asia	coast
Koh Mak	Thailand	Asia	island
Koh Kood	Thailand	Asia	island
Koh Yao Noi	Thailand	Asia	island
Khao Lak	Thailand	Asia	coast
Khanom	Thailand	Asia	coast
Trat	Thailand	Asia	coast
Phetchabun	Thailand	Asia	mountain
Sukhothai Plains	Thailand	Asia	roadtrip
Ubon Ratchathani	Thailand	Asia	city
Nakhon Phanom	Thailand	Asia	city
Songkhla	Thailand	Asia	coast
Satun	Thailand	Asia	coast
Isaan Plateau	Thailand	Asia	roadtrip
Khao Kho	Thailand	Asia	mountain
Chiang Saen	Thailand	Asia	city
Mae Salong	Thailand	Asia	mountain
Phitsanulok	Thailand	Asia	city
Koh Jum	Thailand	Asia	island
Trang Coast	Thailand	Asia	coast
Koh Mook	Thailand	Asia	island
Nan Loop	Thailand	Asia	roadtrip
Vientiane Riverside	Laos	Asia	coast
Luang Namtha	Laos	Asia	mountain
Muang Ngoi	Laos	Asia	mountain
Thakhek Loop	Laos	Asia	roadtrip
Champasak	Laos	Asia	cultural
Muang La	Laos	Asia	mountain
Ban Houayxay	Laos	Asia	city
Xieng Khouang	Laos	Asia	city
Nam Et-Phou Louey	Laos	Asia	park
Luang Prabang Hills	Laos	Asia	roadtrip
Kep Islands	Cambodia	Asia	island
Koh Sdach	Cambodia	Asia	island
Kampong Cham	Cambodia	Asia	city
Banlung	Cambodia	Asia	mountain
Sen Monorom	Cambodia	Asia	mountain
Koh Kong	Cambodia	Asia	coast
Bokor Highlands	Cambodia	Asia	mountain
Takeo	Cambodia	Asia	city
Banteay Chhmar	Cambodia	Asia	cultural
Kampong Chhnang	Cambodia	Asia	city
Siem Reap Temples Belt	Cambodia	Asia	roadtrip
Battambang Countryside	Cambodia	Asia	roadtrip
Hoi An Beaches	Vietnam	Asia	coast
Hue Imperial City	Vietnam	Asia	cultural
Phong Nha	Vietnam	Asia	park
Ha Giang Loop	Vietnam	Asia	roadtrip
Mai Chau	Vietnam	Asia	mountain
Moc Chau	Vietnam	Asia	mountain
Quy Nhon	Vietnam	Asia	coast
Nha Trang	Vietnam	Asia	coast
Dalat	Vietnam	Asia	mountain
Phan Rang	Vietnam	Asia	coast
Con Dao	Vietnam	Asia	island
Phu Yen	Vietnam	Asia	coast
Can Tho	Vietnam	Asia	city
Mekong Delta	Vietnam	Asia	roadtrip
Mui Ne	Vietnam	Asia	coast
Ba Be Lake	Vietnam	Asia	lake
Cao Bang	Vietnam	Asia	mountain
Tam Coc	Vietnam	Asia	cultural
Bac Ha	Vietnam	Asia	mountain
Ha Long Hinterland	Vietnam	Asia	roadtrip
Vung Tau	Vietnam	Asia	coast
Da Lat Highlands	Vietnam	Asia	roadtrip
Koh Rong Archipelago	Cambodia	Asia	roadtrip
Mrauk U	Myanmar	Asia	cultural
Ngapali	Myanmar	Asia	coast
Hsipaw	Myanmar	Asia	mountain
Mawlamyine	Myanmar	Asia	city
Dawei	Myanmar	Asia	coast
Pyin Oo Lwin	Myanmar	Asia	mountain
Putao	Myanmar	Asia	mountain
Kalaw	Myanmar	Asia	mountain
Loikaw	Myanmar	Asia	city
Sittwe	Myanmar	Asia	coast
Bagan Plains	Myanmar	Asia	roadtrip
Lake Inle Shore	Myanmar	Asia	lake
Baguio Highlands	Philippines	Asia	mountain
Batanes Coast	Philippines	Asia	coast
Moalboal	Philippines	Asia	coast
Apo Island	Philippines	Asia	island
Siquijor Waterfalls Belt	Philippines	Asia	roadtrip
Romblon	Philippines	Asia	island
Port Barton	Philippines	Asia	coast
El Nido Bacuit	Philippines	Asia	island
Bantayan Beaches	Philippines	Asia	coast
Catanduanes	Philippines	Asia	island
Dinagat Islands	Philippines	Asia	island
Camotes Islands	Philippines	Asia	island
Malapascua	Philippines	Asia	island
Donsol	Philippines	Asia	coast
Bicol Volcano Belt	Philippines	Asia	roadtrip
Sorsogon Coast	Philippines	Asia	coast
Baguio Pine Hills	Philippines	Asia	roadtrip
Iloilo	Philippines	Asia	city
Bacolod	Philippines	Asia	city
Sultan Kudarat Coast	Philippines	Asia	coast
Pagudpud	Philippines	Asia	coast
Siargao Surf Coast	Philippines	Asia	coast
Samal Island	Philippines	Asia	island
Tacloban	Philippines	Asia	city
Caramoan	Philippines	Asia	coast
El Yuco Loop	Philippines	Asia	roadtrip
Banda Neira	Indonesia	Asia	island
Ternate	Indonesia	Asia	city
Tidore	Indonesia	Asia	island
Banyuwangi	Indonesia	Asia	coast
Jember	Indonesia	Asia	city
Dieng Plateau	Indonesia	Asia	mountain
Karimunjawa	Indonesia	Asia	island
Yogyakarta Hinterland	Indonesia	Asia	roadtrip
Bogor	Indonesia	Asia	city
Pangandaran	Indonesia	Asia	coast
Cirebon	Indonesia	Asia	city
Batu	Indonesia	Asia	mountain
Baluran National Park	Indonesia	Asia	park
Bunaken	Indonesia	Asia	island
Tomohon	Indonesia	Asia	mountain
Likupang	Indonesia	Asia	coast
Wakatobi	Indonesia	Asia	island
Selayar	Indonesia	Asia	island
Toraja Highlands	Indonesia	Asia	mountain
Manado	Indonesia	Asia	city
Samosir	Indonesia	Asia	island
Berastagi	Indonesia	Asia	mountain
Bukittinggi	Indonesia	Asia	mountain
Padang Highlands	Indonesia	Asia	roadtrip
Mentawai	Indonesia	Asia	island
Nias	Indonesia	Asia	island
Tanjung Puting	Indonesia	Asia	park
Banjarmasin	Indonesia	Asia	city
Derawan Islands	Indonesia	Asia	island
Berau Coast	Indonesia	Asia	coast
Balikpapan	Indonesia	Asia	city
Samarinda	Indonesia	Asia	city
Komodo Coast	Indonesia	Asia	coast
Sape Route	Indonesia	Asia	roadtrip
Waerebo	Indonesia	Asia	cultural
Savu Sea Islands	Indonesia	Asia	island
Kupang	Indonesia	Asia	city
Alor	Indonesia	Asia	island
Timor Highlands	Indonesia	Asia	mountain
Rote	Indonesia	Asia	island
Mentawai Surf Belt	Indonesia	Asia	roadtrip
Sabang	Indonesia	Asia	island
Banda Aceh	Indonesia	Asia	city
Pekanbaru	Indonesia	Asia	city
Tanjung Selor	Indonesia	Asia	city
Togean Islands	Indonesia	Asia	island
Canggu Rice Belt	Indonesia	Asia	roadtrip
Amed	Indonesia	Asia	coast
Pemuteran	Indonesia	Asia	coast
Nusa Ceningan	Indonesia	Asia	island
West Bali National Park	Indonesia	Asia	park
Sengkang	Indonesia	Asia	city
Kuala Kangsar	Malaysia	Asia	city
Kuantan	Malaysia	Asia	coast
Mersing	Malaysia	Asia	coast
Perlis	Malaysia	Asia	coast
Genting Highlands	Malaysia	Asia	mountain
Fraser's Hill	Malaysia	Asia	mountain
Belum Rainforest	Malaysia	Asia	park
Semporna	Malaysia	Asia	coast
Kudat	Malaysia	Asia	coast
Kota Belud	Malaysia	Asia	coast
Keningau	Malaysia	Asia	mountain
Lahad Datu	Malaysia	Asia	park
Tawau	Malaysia	Asia	city
Sibu	Malaysia	Asia	city
Bintulu	Malaysia	Asia	coast
Kapit	Malaysia	Asia	mountain
Pulau Pangkor	Malaysia	Asia	island
Johor Coast	Malaysia	Asia	coast
Desaru	Malaysia	Asia	coast
Kuala Selangor	Malaysia	Asia	coast
Janda Baik	Malaysia	Asia	mountain
Perak River Towns	Malaysia	Asia	roadtrip
Tebrau Coast	Malaysia	Asia	roadtrip
Sembporna Islands	Malaysia	Asia	roadtrip
George Town Heritage Belt	Malaysia	Asia	roadtrip
Taichung Highlands	Taiwan	Asia	mountain
Lukang	Taiwan	Asia	cultural
Yilan	Taiwan	Asia	coast
Keelung	Taiwan	Asia	coast
Green Island Taiwan	Taiwan	Asia	island
Penghu	Taiwan	Asia	island
Chiayi	Taiwan	Asia	city
Aowanda	Taiwan	Asia	park
Wuling Farm	Taiwan	Asia	mountain
Tainan Temples Belt	Taiwan	Asia	roadtrip
Okinawa Main Island	Japan	Asia	island
Miyakojima	Japan	Asia	island
Iriomote	Japan	Asia	island
Amami Oshima	Japan	Asia	island
Kagurazaka Tokyo	Japan	Asia	city
Fukui	Japan	Asia	city
Toyooka	Japan	Asia	city
Iya Valley	Japan	Asia	mountain
Kii Peninsula	Japan	Asia	roadtrip
Matsuyama	Japan	Asia	city
Onomichi	Japan	Asia	coast
Shimanami Kaido	Japan	Asia	roadtrip
Akiyoshidai	Japan	Asia	park
Yufuin	Japan	Asia	mountain
Arita	Japan	Asia	cultural
Saga Plains	Japan	Asia	roadtrip
Dazaifu	Japan	Asia	cultural
Mito	Japan	Asia	city
Kawazu	Japan	Asia	coast
Shodoshima	Japan	Asia	island
Teshima	Japan	Asia	island
Nikko Mountains	Japan	Asia	roadtrip
Hiraizumi	Japan	Asia	cultural
Towada	Japan	Asia	lake
Biei	Japan	Asia	roadtrip
Shiretoko	Japan	Asia	park
Furano Valley	Japan	Asia	roadtrip
Noboribetsu	Japan	Asia	mountain
Lake Akan	Japan	Asia	lake
Ine	Japan	Asia	coast
Miyama	Japan	Asia	cultural
Hagi	Japan	Asia	city
Amanohashidate	Japan	Asia	coast
Izu Islands	Japan	Asia	island
Kusatsu Onsen	Japan	Asia	mountain
Karuizawa	Japan	Asia	mountain
Obuse	Japan	Asia	city
Yamagata Hot Springs Belt	Japan	Asia	roadtrip
Aso Highlands	Japan	Asia	roadtrip
Unzen	Japan	Asia	mountain
Yakushima Forest	Japan	Asia	park
Noto Peninsula	Japan	Asia	coast
Sado Island	Japan	Asia	island
Omi Hachiman	Japan	Asia	cultural
Hikone	Japan	Asia	city
Matsue Coast	Japan	Asia	coast
Tsuwano	Japan	Asia	city
Ureshino	Japan	Asia	mountain
Kagoshima Bay	Japan	Asia	coast
Jeju Olle Coast	South Korea	Asia	coast
Pohang	South Korea	Asia	coast
Suwon	South Korea	Asia	city
Mokpo	South Korea	Asia	coast
Boseong	South Korea	Asia	mountain
Damyang	South Korea	Asia	cultural
Chuncheon	South Korea	Asia	city
Jecheon	South Korea	Asia	lake
Seorak Coast	South Korea	Asia	roadtrip
Gyeongju Hills	South Korea	Asia	roadtrip
Koror Beaches	Palau	Oceania	coast
Peleliu	Palau	Oceania	island
Babeldaob	Palau	Oceania	island
Ngardmau	Palau	Oceania	mountain
Kayangel	Palau	Oceania	island
Airai	Palau	Oceania	city
Chuuk Islands	Micronesia	Oceania	island
Yap Lagoon	Micronesia	Oceania	coast
Kosrae Rainforest	Micronesia	Oceania	park
Pohnpei Highlands	Micronesia	Oceania	mountain
Majuro Atoll	Marshall Islands	Oceania	island
Arno Atoll	Marshall Islands	Oceania	island
Ebeye	Marshall Islands	Oceania	island
Ailinglaplap	Marshall Islands	Oceania	island
Mili Atoll	Marshall Islands	Oceania	island
Tuamotu Atolls	French Polynesia	Oceania	island
Fakarava	French Polynesia	Oceania	island
Taha'a	French Polynesia	Oceania	island
Maupiti	French Polynesia	Oceania	island
Nuku Hiva	French Polynesia	Oceania	island
Huahine Lagoon	French Polynesia	Oceania	coast
Bora Bora Motus	French Polynesia	Oceania	island
Ahe Atoll	French Polynesia	Oceania	island
Mangareva	French Polynesia	Oceania	island
Rurutu	French Polynesia	Oceania	island
Aitutaki Motus	Cook Islands	Oceania	island
Atiu	Cook Islands	Oceania	island
Mangaia	Cook Islands	Oceania	island
Mitiaro	Cook Islands	Oceania	island
Mauke	Cook Islands	Oceania	island
Savai'i Coast	Samoa	Oceania	coast
Lalomanu	Samoa	Oceania	coast
Manono	Samoa	Oceania	island
Tutuila	American Samoa	Oceania	island
Ofu	American Samoa	Oceania	island
Ta'u	American Samoa	Oceania	island
Upolu Highlands	Samoa	Oceania	mountain
Samoa South Coast	Samoa	Oceania	roadtrip
Niue Cliffs	Niue	Oceania	coast
Alofi	Niue	Oceania	city
Niue Coral Coast	Niue	Oceania	coast
Liku	Niue	Oceania	coast
Lakepa	Niue	Oceania	coast
Lifou Lagoons	New Caledonia	Oceania	coast
Maré	New Caledonia	Oceania	island
Île des Pins	New Caledonia	Oceania	island
Ouvéa	New Caledonia	Oceania	island
Poindimié	New Caledonia	Oceania	coast
Koné	New Caledonia	Oceania	city
Hienghène	New Caledonia	Oceania	coast
Aneityum	Vanuatu	Oceania	island
Port Olry	Vanuatu	Oceania	coast
Pentecost Island	Vanuatu	Oceania	island
Ambrym	Vanuatu	Oceania	island
Malekula	Vanuatu	Oceania	island
Epi	Vanuatu	Oceania	island
Erromango	Vanuatu	Oceania	island
Santo Blue Holes	Vanuatu	Oceania	lake
Futuna Coast	Vanuatu	Oceania	coast
Lelepa	Vanuatu	Oceania	island
Coral Coast Fiji	Fiji	Oceania	coast
Taveuni	Fiji	Oceania	island
Kadavu	Fiji	Oceania	island
Savusavu	Fiji	Oceania	coast
Pacific Harbour	Fiji	Oceania	coast
Ovalau	Fiji	Oceania	island
Beqa	Fiji	Oceania	island
Denarau Belt	Fiji	Oceania	roadtrip
Vanua Levu Coast	Fiji	Oceania	coast
Lomaiviti	Fiji	Oceania	island
Aoraki Mackenzie	New Zealand	Oceania	mountain
Catlins	New Zealand	Oceania	coast
Coromandel Peninsula	New Zealand	Oceania	coast
Marlborough	New Zealand	Oceania	roadtrip
Nelson	New Zealand	Oceania	city
Westport New Zealand	New Zealand	Oceania	coast
Franz Josef	New Zealand	Oceania	mountain
Fox Glacier	New Zealand	Oceania	mountain
Dunedin	New Zealand	Oceania	city
The Sounds NZ	New Zealand	Oceania	coast
Raglan	New Zealand	Oceania	coast
Napier	New Zealand	Oceania	city
Taupō	New Zealand	Oceania	lake
Tongariro	New Zealand	Oceania	park
Queen Charlotte Drive	New Zealand	Oceania	roadtrip
Lake Tekapo	New Zealand	Oceania	lake
Akaroa	New Zealand	Oceania	coast
Gisborne	New Zealand	Oceania	coast
Stewart Island	New Zealand	Oceania	island
Mount Maunganui	New Zealand	Oceania	coast
Port Stephens	Australia	Oceania	coast
Hunter Valley	Australia	Oceania	roadtrip
Lord Howe Lagoon	Australia	Oceania	coast
Jervis Bay	Australia	Oceania	coast
Blue Mountains Villages	Australia	Oceania	roadtrip
Canberra Highlands	Australia	Oceania	roadtrip
Bruny Island	Australia	Oceania	island
Launceston	Australia	Oceania	city
Bay of Fires	Australia	Oceania	coast
Cradle Mountain	Australia	Oceania	park
Tasman Peninsula	Australia	Oceania	coast
Mornington Peninsula	Australia	Oceania	coast
Yarra Valley	Australia	Oceania	roadtrip
Phillip Island	Australia	Oceania	island
Wilsons Promontory	Australia	Oceania	park
Grampians	Australia	Oceania	mountain
Kangaroo Island Coast	Australia	Oceania	coast
Clare Valley	Australia	Oceania	roadtrip
Barossa Valley	Australia	Oceania	roadtrip
Flinders Ranges	Australia	Oceania	mountain
Esperance	Australia	Oceania	coast
Albany Australia	Australia	Oceania	coast
Pemberton	Australia	Oceania	mountain
Karijini	Australia	Oceania	park
Exmouth	Australia	Oceania	coast
Coral Bay	Australia	Oceania	coast
Ningaloo Coast	Australia	Oceania	coast
Margaret River Coast	Australia	Oceania	coast
Kalbarri	Australia	Oceania	park
Rottnest Coast	Australia	Oceania	coast
Kununurra	Australia	Oceania	city
Kakadu	Australia	Oceania	park
Litchfield	Australia	Oceania	park
Arnhem Land Edge	Australia	Oceania	roadtrip
Airlie Beach	Australia	Oceania	coast
Magnetic Island	Australia	Oceania	island
Mission Beach	Australia	Oceania	coast
Cape Tribulation	Australia	Oceania	coast
Port Douglas Hinterland	Australia	Oceania	roadtrip
Sunshine Coast Hinterland	Australia	Oceania	mountain
K'gari	Australia	Oceania	island
Gold Coast Hinterland	Australia	Oceania	mountain
Southern Great Barrier Reef	Australia	Oceania	park
Noosa Everglades	Australia	Oceania	lake
Fitzroy Island	Australia	Oceania	island
Whitsunday Coast	Australia	Oceania	coast
Katoomba Escarpment	Australia	Oceania	mountain
Bora Bora East Motu	French Polynesia	Oceania	island
Essaouira	Morocco	Africa	coast
Oualidia	Morocco	Africa	coast
Essaouira Coast	Morocco	Africa	roadtrip
Meknes Medina	Morocco	Africa	cultural
Ifrane	Morocco	Africa	mountain
Azilal	Morocco	Africa	mountain
Tafraoute	Morocco	Africa	mountain
Dakhla	Morocco	Africa	coast
Taroudant	Morocco	Africa	city
Al Hoceima	Morocco	Africa	coast
Volubilis	Morocco	Africa	cultural
Berkane Coast	Morocco	Africa	roadtrip
Toubkal Valley	Morocco	Africa	mountain
Ouzoud Falls	Morocco	Africa	park
Taza	Morocco	Africa	city
Monastir	Tunisia	Africa	coast
Mahdia	Tunisia	Africa	coast
Hammamet	Tunisia	Africa	coast
Sfax	Tunisia	Africa	city
Douz	Tunisia	Africa	desert
Matmata	Tunisia	Africa	cultural
El Jem	Tunisia	Africa	cultural
Tabarka	Tunisia	Africa	coast
Bizerte	Tunisia	Africa	coast
Nefta	Tunisia	Africa	desert
El Kef	Tunisia	Africa	city
Ksar Ghilane	Tunisia	Africa	desert
Sousse Medina	Tunisia	Africa	cultural
Kerkennah	Tunisia	Africa	island
Tataouine	Tunisia	Africa	city
Alexandria Corniche	Egypt	Africa	coast
Marsa Alam	Egypt	Africa	coast
Hurghada	Egypt	Africa	coast
Marsa Matruh	Egypt	Africa	coast
Fayoum Oasis	Egypt	Africa	desert
Saint Catherine	Egypt	Africa	mountain
Abydos	Egypt	Africa	cultural
Nuweiba	Egypt	Africa	coast
Ras Mohammed	Egypt	Africa	park
El Gouna	Egypt	Africa	coast
El Quseir	Egypt	Africa	coast
Kharga Oasis	Egypt	Africa	desert
Bahariya Oasis	Egypt	Africa	desert
Aswan Nile Islands	Egypt	Africa	island
Ismailia	Egypt	Africa	city
Marsa Mubarak Coast	Egypt	Africa	roadtrip
Dahshur	Egypt	Africa	cultural
Marsa Shagra	Egypt	Africa	coast
Sidi Ifni	Morocco	Africa	coast
Aswan Desert Edge	Egypt	Africa	roadtrip
Saint Catherine Trail	Egypt	Africa	roadtrip
Siwa Desert Route	Egypt	Africa	roadtrip
Blue Nile Highlands	Ethiopia	Africa	mountain
Axum	Ethiopia	Africa	cultural
Lalibela Highlands	Ethiopia	Africa	mountain
Omo Valley	Ethiopia	Africa	roadtrip
Awasa	Ethiopia	Africa	lake
Debark	Ethiopia	Africa	mountain
Arba Minch	Ethiopia	Africa	city
Bale Mountains	Ethiopia	Africa	park
Mekele	Ethiopia	Africa	city
Wenchi Crater Lake	Ethiopia	Africa	lake
Dire Dawa	Ethiopia	Africa	city
Danakil Route	Ethiopia	Africa	roadtrip
Harar Walled City	Ethiopia	Africa	cultural
Lake Tana Islands	Ethiopia	Africa	island
Rift Valley Lakes Ethiopia	Ethiopia	Africa	roadtrip
Bahir Dar Blue Nile	Ethiopia	Africa	roadtrip
Arusha Corridor	Tanzania	Africa	roadtrip
Mikumi Plains	Tanzania	Africa	park
Pangani	Tanzania	Africa	coast
Bagamoyo	Tanzania	Africa	coast
Kilwa Kisiwani	Tanzania	Africa	cultural
Lake Natron	Tanzania	Africa	lake
Usambara Mountains	Tanzania	Africa	mountain
Iringa	Tanzania	Africa	city
Katavi	Tanzania	Africa	park
Mahale Mountains	Tanzania	Africa	park
Mwanza	Tanzania	Africa	city
Pemba Tanzania	Tanzania	Africa	island
Lindi Coast	Tanzania	Africa	coast
Mikindani	Tanzania	Africa	coast
Tarangire Valley	Tanzania	Africa	roadtrip
Jinja Nile	Uganda	Africa	coast
Fort Portal	Uganda	Africa	city
Kibale	Uganda	Africa	park
Queen Elizabeth Uganda	Uganda	Africa	park
Sipi Falls	Uganda	Africa	mountain
Kidepo Valley	Uganda	Africa	park
Lake Mburo	Uganda	Africa	lake
Kampala Hills	Uganda	Africa	roadtrip
Mbarara	Uganda	Africa	city
Rwenzori	Uganda	Africa	mountain
Soroti	Uganda	Africa	city
Entebbe Shores	Uganda	Africa	coast
Kampala Old City	Uganda	Africa	cultural
Lake Mutanda	Uganda	Africa	lake
Mgahinga	Uganda	Africa	park
Naivasha Shores	Kenya	Africa	coast
Samburu Plains	Kenya	Africa	park
Nakuru	Kenya	Africa	city
Malindi	Kenya	Africa	coast
Mount Kenya	Kenya	Africa	mountain
Hell's Gate	Kenya	Africa	park
Kakamega Forest	Kenya	Africa	park
Marsabit	Kenya	Africa	mountain
Kisite Marine Park	Kenya	Africa	park
Laikipia	Kenya	Africa	roadtrip
Nairobi Highlands	Kenya	Africa	roadtrip
Meru National Park Kenya	Kenya	Africa	park
Lake Turkana	Kenya	Africa	lake
Sagana	Kenya	Africa	mountain
Nyeri	Kenya	Africa	city
Kigali Green Hills	Rwanda	Africa	roadtrip
Akagera National Park	Rwanda	Africa	park
Musanze Highlands	Rwanda	Africa	mountain
Gisenyi	Rwanda	Africa	coast
Kibuye	Rwanda	Africa	lake
Butare Heritage Quarter	Rwanda	Africa	cultural
Kigali Old Quarter	Rwanda	Africa	cultural
Nyanza	Rwanda	Africa	city
Karongi	Rwanda	Africa	lake
Gisagara Hills	Rwanda	Africa	mountain
Bujumbura	Burundi	Africa	city
Gitega	Burundi	Africa	city
Lake Tanganyika Burundi	Burundi	Africa	lake
Kibira National Park	Burundi	Africa	park
Rumonge	Burundi	Africa	coast
Ngozi	Burundi	Africa	mountain
Bururi	Burundi	Africa	mountain
Ruvubu National Park	Burundi	Africa	park
Muyinga	Burundi	Africa	city
Saga Beach Burundi	Burundi	Africa	coast
Dakar Corniche	Senegal	Africa	coast
Île de Gorée	Senegal	Africa	island
Sine-Saloum	Senegal	Africa	park
Mbour	Senegal	Africa	coast
Joal-Fadiouth	Senegal	Africa	cultural
Tambacounda	Senegal	Africa	city
Kédougou	Senegal	Africa	mountain
Casamance River	Senegal	Africa	roadtrip
Ziguinchor	Senegal	Africa	city
Lac Rose	Senegal	Africa	lake
Kaolack	Senegal	Africa	city
Popenguine	Senegal	Africa	coast
Zinder	Niger	Africa	city
Agadez	Niger	Africa	city
Aïr Mountains	Niger	Africa	mountain
Niamey	Niger	Africa	city
W National Park Niger	Niger	Africa	park
Diffa	Niger	Africa	city
Dosso	Niger	Africa	city
Tahoua	Niger	Africa	city
Ayorou	Niger	Africa	coast
Termit Massif	Niger	Africa	desert
Cotonou Coast	Benin	Africa	coast
Ganvié	Benin	Africa	lake
Abomey	Benin	Africa	cultural
Grand-Popo	Benin	Africa	coast
Natitingou	Benin	Africa	city
Porto-Novo Heritage Quarter	Benin	Africa	cultural
Pendjari	Benin	Africa	park
Parakou	Benin	Africa	city
Dassa-Zoumé	Benin	Africa	mountain
Lokossa	Benin	Africa	city
Lomé Beaches	Togo	Africa	coast
Kpalimé	Togo	Africa	mountain
Koutammakou	Togo	Africa	cultural
Aneho	Togo	Africa	coast
Sokodé	Togo	Africa	city
Atakpamé	Togo	Africa	city
Dapaong	Togo	Africa	city
Fazao-Malfakassa	Togo	Africa	park
Togoville	Togo	Africa	cultural
Kara Togo	Togo	Africa	city
Accra Beaches	Ghana	Africa	coast
Kakum	Ghana	Africa	park
Axim	Ghana	Africa	coast
Takoradi	Ghana	Africa	city
Wli Falls	Ghana	Africa	park
Volta Lake	Ghana	Africa	lake
Tamale	Ghana	Africa	city
Ada Estuary	Ghana	Africa	coast
Paga	Ghana	Africa	cultural
Mole Savannah Belt	Ghana	Africa	roadtrip
Koforidua	Ghana	Africa	city
Bamenda Highlands	Cameroon	Africa	mountain
Kribi	Cameroon	Africa	coast
Limbe	Cameroon	Africa	coast
Mount Cameroon	Cameroon	Africa	mountain
Yaoundé	Cameroon	Africa	city
Douala	Cameroon	Africa	city
Ngaoundéré	Cameroon	Africa	city
Waza National Park	Cameroon	Africa	park
Dschang	Cameroon	Africa	mountain
Bafoussam	Cameroon	Africa	city
Libreville	Gabon	Africa	city
Loango National Park	Gabon	Africa	park
Pointe Denis	Gabon	Africa	coast
Lambaréné	Gabon	Africa	city
Port-Gentil	Gabon	Africa	coast
Franceville	Gabon	Africa	city
Ivindo	Gabon	Africa	park
Mayumba	Gabon	Africa	coast
Mouila	Gabon	Africa	city
Akanda	Gabon	Africa	park
São Tomé North Coast	São Tomé and Príncipe	Africa	coast
Santo António	São Tomé and Príncipe	Africa	city
Ilhéu das Rolas	São Tomé and Príncipe	Africa	island
Obo National Park	São Tomé and Príncipe	Africa	park
Neves	São Tomé and Príncipe	Africa	coast
Santana São Tomé	São Tomé and Príncipe	Africa	coast
Benguela	Angola	Africa	coast
Lubango	Angola	Africa	city
Kalandula Falls	Angola	Africa	park
Luanda	Angola	Africa	city
Namibe	Angola	Africa	desert
Lobito	Angola	Africa	coast
Malanje	Angola	Africa	city
M'banza-Kongo	Angola	Africa	cultural
Kissama	Angola	Africa	park
Tundavala Gap	Angola	Africa	mountain
Chobe River Zambia	Zambia	Africa	coast
Kasanka	Zambia	Africa	park
Kafue	Zambia	Africa	park
Lower Zambezi	Zambia	Africa	park
Chipata	Zambia	Africa	city
Lake Tanganyika Zambia	Zambia	Africa	lake
North Luangwa	Zambia	Africa	park
South Luangwa Valley	Zambia	Africa	roadtrip
Lusaka Green Belt	Zambia	Africa	roadtrip
Siavonga	Zambia	Africa	lake
Lake Kariba Zimbabwe	Zimbabwe	Africa	lake
Matobo	Zimbabwe	Africa	park
Nyanga	Zimbabwe	Africa	mountain
Mutare	Zimbabwe	Africa	city
Great Zimbabwe	Zimbabwe	Africa	cultural
Kariba	Zimbabwe	Africa	lake
Bulawayo	Zimbabwe	Africa	city
Gonarezhou	Zimbabwe	Africa	park
Chimanimani	Zimbabwe	Africa	mountain
Bvumba	Zimbabwe	Africa	mountain
Lilongwe Highlands	Malawi	Africa	mountain
Nkhotakota	Malawi	Africa	coast
Cape Maclear	Malawi	Africa	coast
Mzuzu	Malawi	Africa	city
Nyika Plateau	Malawi	Africa	mountain
Likoma Island	Malawi	Africa	island
Blantyre	Malawi	Africa	city
Zomba Plateau	Malawi	Africa	mountain
Monkey Bay	Malawi	Africa	coast
Lake Malawi South Shore	Malawi	Africa	roadtrip
Inhambane Coast	Mozambique	Africa	coast
Vilanculos Archipelago	Mozambique	Africa	coast
Pemba Mozambique	Mozambique	Africa	coast
Gorongosa	Mozambique	Africa	park
Ilha de Mozambique	Mozambique	Africa	island
Nampula	Mozambique	Africa	city
Quirimbas	Mozambique	Africa	island
Xai-Xai	Mozambique	Africa	coast
Chimoio	Mozambique	Africa	city
Maputo Bay	Mozambique	Africa	coast
Sodwana Bay	South Africa	Africa	coast
Coffee Bay	South Africa	Africa	coast
Port Elizabeth	South Africa	Africa	coast
Addo Elephant Park	South Africa	Africa	park
Blyde River Canyon	South Africa	Africa	mountain
Paternoster	South Africa	Africa	coast
Cederberg Valleys	South Africa	Africa	roadtrip
Hogsback	South Africa	Africa	mountain
Marloth Park	South Africa	Africa	park
Jeffreys Bay	South Africa	Africa	coast
Swellendam	South Africa	Africa	city
Kgalagadi	South Africa	Africa	park
St Lucia South Africa	South Africa	Africa	coast
Mthatha Coast	South Africa	Africa	roadtrip
Clarens	South Africa	Africa	mountain
Madikwe	South Africa	Africa	park
Hoedspruit	South Africa	Africa	city
Port Alfred	South Africa	Africa	coast
Sani Pass	South Africa	Africa	mountain
Kosi Bay	South Africa	Africa	coast
Skeleton Coast Namibia	Namibia	Africa	roadtrip
Lüderitz	Namibia	Africa	coast
Spitzkoppe	Namibia	Africa	mountain
Damaraland Valleys	Namibia	Africa	roadtrip
Caprivi Strip	Namibia	Africa	coast
Kolmanskop	Namibia	Africa	cultural
Twyfelfontein	Namibia	Africa	cultural
Waterberg Namibia	Namibia	Africa	mountain
Henties Bay	Namibia	Africa	coast
Keetmanshoop	Namibia	Africa	city
Savuti	Botswana	Africa	park
Nxai Pan	Botswana	Africa	park
Tuli Block	Botswana	Africa	roadtrip
Khwai	Botswana	Africa	park
Ghanzi	Botswana	Africa	city
Mokhotlong	Lesotho	Africa	mountain
Malealea	Lesotho	Africa	mountain
Semonkong	Lesotho	Africa	mountain
Butha-Buthe	Lesotho	Africa	city
Katse Dam	Lesotho	Africa	lake
Maseru	Lesotho	Africa	city
Bokong	Lesotho	Africa	park
Quthing	Lesotho	Africa	city
Ts'ehlanyane	Lesotho	Africa	park
Leribe Highlands	Lesotho	Africa	roadtrip
Maseru Plateau	Lesotho	Africa	roadtrip
Toamasina	Madagascar	Africa	coast
Ranomafana	Madagascar	Africa	park
Morondava	Madagascar	Africa	coast
Ifaty	Madagascar	Africa	coast
Antsiranana	Madagascar	Africa	coast
Andringitra	Madagascar	Africa	mountain
Nosy Komba	Madagascar	Africa	island
Anakao	Madagascar	Africa	coast
Masoala	Madagascar	Africa	park
Fianarantsoa	Madagascar	Africa	city
Ankarana	Madagascar	Africa	park
Tuléar	Madagascar	Africa	coast
Ankarafantsika	Madagascar	Africa	park
Andasibe Forest	Madagascar	Africa	roadtrip
Sainte-Marie Coast	Madagascar	Africa	roadtrip
Grand Baie	Mauritius	Africa	coast
Chamarel	Mauritius	Africa	mountain
Flic en Flac	Mauritius	Africa	coast
Le Morne Peninsula	Mauritius	Africa	coast
Trou aux Biches	Mauritius	Africa	coast
Mahebourg	Mauritius	Africa	coast
Belle Mare	Mauritius	Africa	coast
Chamarel Route	Mauritius	Africa	roadtrip
Praslin Beaches	Seychelles	Africa	coast
La Digue Coves	Seychelles	Africa	coast
Silhouette Island	Seychelles	Africa	island
Curieuse	Seychelles	Africa	island
Denis Island	Seychelles	Africa	island
Mahé Highlands	Seychelles	Africa	mountain
Mahé Coast	Seychelles	Africa	roadtrip
Piton de la Fournaise	Réunion	Africa	mountain
Cilaos	Réunion	Africa	mountain
Saint-Gilles	Réunion	Africa	coast
Hell-Bourg	Réunion	Africa	city
Réunion South Coast	Réunion	Africa	coast
Reunion Volcano Route	Réunion	Africa	roadtrip
''' 

KIND_META = {
    'city': ('$$', 'Mar–May, Sep–Nov', ['City', 'Cultural', 'Food'], ['solo', 'food', 'weekend'], 'A strong urban base with enough culture, food, and day-trip value to justify a proper stay.'),
    'island': ('$$$', 'Nov–Apr', ['Beach', 'Nature', 'Relaxation'], ['couples', 'beach', 'island-hopping'], 'An easy high-payoff island pick for beach time, scenery, and switching fully into vacation mode.'),
    'coast': ('$$', 'May–Oct', ['Beach', 'Relaxation', 'Nature'], ['couples', 'road-trip', 'food'], 'A scenic coastal stretch or town that works for slow days, good views, and easy trip-building.'),
    'park': ('$$$', 'May–Sep', ['Nature', 'Adventure', 'Hiking'], ['adventure', 'photography', 'wildlife'], 'A high-value nature destination built around scenery, wildlife, or hikes worth traveling for.'),
    'mountain': ('$$', 'Jun–Sep', ['Nature', 'Adventure', 'Hiking'], ['adventure', 'photography', 'hiking'], 'A mountain destination with real scenery payoff, active days, and cooler-air reset value.'),
    'lake': ('$$', 'May–Sep', ['Nature', 'Relaxation', 'Romantic'], ['couples', 'photography', 'relaxation'], 'A lake-centered destination that earns its place on calm water, views, and an easy slower pace.'),
    'desert': ('$$', 'Oct–Apr', ['Adventure', 'Nature', 'Unfrequented'], ['adventure', 'photography', 'offbeat'], 'A desert landscape destination with stark scenery, huge skies, and a more remote trip profile.'),
    'cultural': ('$$', 'Apr–Jun, Sep–Oct', ['Cultural', 'Romantic', 'History'], ['history', 'solo', 'couples'], 'A culture-first destination with strong history, atmosphere, and clear landmark value.'),
    'roadtrip': ('$$', 'May–Oct', ['Nature', 'Adventure', 'Relaxation'], ['road-trip', 'photography', 'adventure'], 'A route-style destination that works best as a scenic circuit rather than a single stop.'),
}

REGION_BUDGET = {
    'Europe': '$$$', 'Asia': '$$', 'Africa': '$$', 'North America': '$$$', 'South America': '$$', 'Oceania': '$$$'
}
REGION_SEASON = {
    'Europe': 'Apr–Oct', 'Asia': 'Oct–May', 'Africa': 'Nov–Apr', 'North America': 'Nov–Apr', 'South America': 'Sep–May', 'Oceania': 'May–Oct'
}

def slugify(name: str) -> str:
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.casefold().replace('’', "'")
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r"\s+", '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def parse_rows():
    rows = []
    for raw in TSV.strip().splitlines():
        name, region, continent, kind = [part.strip() for part in raw.split('\t')]
        rows.append((name, region, continent, kind))
    return rows


def generated_row(name: str, region: str, continent: str, kind: str) -> dict:
    budget, season, vibes, travel, pitch = KIND_META[kind]
    return {
        'name': name,
        'region': region,
        'continent': continent,
        'photo': FALLBACK_PHOTO,
        'pitch': pitch,
        'budget': REGION_BUDGET.get(continent, budget),
        'season': REGION_SEASON.get(continent, season),
        'vibes': vibes,
        'travel': travel,
    }


def main():
    data = json.loads(SOURCE.read_text())
    rows = parse_rows()
    generated_rows = [generated_row(name, region, continent, kind) for name, region, continent, kind in rows]
    generated_row_set = {json.dumps(row, sort_keys=True, ensure_ascii=False) for row in generated_rows}
    already_present = [row for row in data if json.dumps(row, sort_keys=True, ensure_ascii=False) in generated_row_set]
    if len(already_present) >= TARGET_ADD:
        print(f'added=0 total={len(data)} already_present={len(already_present)}')
        print('note=target batch already present; no changes written')
        return

    existing_names = {row.get('name') for row in data if isinstance(row, dict)}
    existing_slugs = {slugify(row.get('name', '')) for row in data if isinstance(row, dict)}
    additions = []
    seen = set()
    for name, region, continent, kind in rows:
        slug = slugify(name)
        if name in existing_names or slug in existing_slugs or slug in seen:
            continue
        row = generated_row(name, region, continent, kind)
        additions.append(row)
        seen.add(slug)
    if len(additions) < TARGET_ADD:
        raise SystemExit(f'Only {len(additions)} unique additions after filtering; need {TARGET_ADD}')
    additions = additions[:TARGET_ADD]
    data.extend(additions)
    data.sort(key=lambda r: r.get('name', '').casefold())
    SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(f'added={len(additions)} total={len(data)}')
    print('first10=', [row['name'] for row in additions[:10]])
    print('last10=', [row['name'] for row in additions[-10:]])

if __name__ == '__main__':
    main()
