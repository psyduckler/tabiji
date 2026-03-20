from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'find' / 'destinations.json'
FALLBACK_PHOTO = 'https://img.tabiji.ai/owl-logo.png'

TSV = '''
Koh Phangan	Thailand	Asia	island
Koh Tao	Thailand	Asia	island
Koh Lanta	Thailand	Asia	island
Khao Sok National Park	Thailand	Asia	park
Ayutthaya	Thailand	Asia	cultural
Kanchanaburi	Thailand	Asia	city
Pai	Thailand	Asia	mountain
Chiang Rai	Thailand	Asia	city
Mae Hong Son	Thailand	Asia	mountain
Khao Yai National Park	Thailand	Asia	park
Phang Nga Bay	Thailand	Asia	coast
Railay	Thailand	Asia	coast
Hua Hin	Thailand	Asia	coast
Koh Chang	Thailand	Asia	island
Koh Lipe	Thailand	Asia	island
Koh Phi Phi	Thailand	Asia	island
Trang Islands	Thailand	Asia	island
Sukhothai	Thailand	Asia	cultural
Isaan	Thailand	Asia	cultural
Surat Thani	Thailand	Asia	city
Luang Prabang	Laos	Asia	city
Vang Vieng	Laos	Asia	mountain
Vientiane	Laos	Asia	city
Pakse	Laos	Asia	city
Si Phan Don	Laos	Asia	island
Plain of Jars	Laos	Asia	cultural
Nong Khiaw	Laos	Asia	mountain
Phonsavan	Laos	Asia	cultural
Bolaven Plateau	Laos	Asia	mountain
Savannakhet	Laos	Asia	city
Kampot	Cambodia	Asia	city
Kep	Cambodia	Asia	coast
Koh Rong	Cambodia	Asia	island
Battambang	Cambodia	Asia	city
Kampong Thom	Cambodia	Asia	cultural
Kratie	Cambodia	Asia	city
Mondulkiri	Cambodia	Asia	mountain
Preah Vihear	Cambodia	Asia	cultural
Koh Rong Samloem	Cambodia	Asia	island
Tonle Sap	Cambodia	Asia	lake
Baguio	Philippines	Asia	mountain
Siquijor	Philippines	Asia	island
Siargao	Philippines	Asia	island
Batanes	Philippines	Asia	island
Puerto Princesa	Philippines	Asia	city
Camiguin	Philippines	Asia	island
Dumaguete	Philippines	Asia	city
Bantayan Island	Philippines	Asia	island
Samar	Philippines	Asia	island
Sorsogon	Philippines	Asia	coast
Vigan	Philippines	Asia	cultural
Sagada	Philippines	Asia	mountain
Banaue	Philippines	Asia	mountain
Siquijor Island	Philippines	Asia	island
Panglao	Philippines	Asia	island
Palawan	Philippines	Asia	island
Gili Trawangan	Indonesia	Asia	island
Gili Air	Indonesia	Asia	island
Ubud	Indonesia	Asia	city
Nusa Penida	Indonesia	Asia	island
Nusa Lembongan	Indonesia	Asia	island
Raja Ampat	Indonesia	Asia	island
Flores	Indonesia	Asia	island
Labuan Bajo	Indonesia	Asia	city
Mount Bromo	Indonesia	Asia	mountain
Ijen	Indonesia	Asia	mountain
Bandung	Indonesia	Asia	city
Surabaya	Indonesia	Asia	city
Semarang	Indonesia	Asia	city
Makassar	Indonesia	Asia	city
Lake Toba	Indonesia	Asia	lake
Bukit Lawang	Indonesia	Asia	park
Tana Toraja	Indonesia	Asia	cultural
Borobudur	Indonesia	Asia	cultural
Prambanan	Indonesia	Asia	cultural
Belitung	Indonesia	Asia	island
Malang	Indonesia	Asia	city
Medan	Indonesia	Asia	city
Padang	Indonesia	Asia	city
Banda Islands	Indonesia	Asia	island
Sumba	Indonesia	Asia	island
Sumatra	Indonesia	Asia	island
Java	Indonesia	Asia	island
Sulawesi	Indonesia	Asia	island
Sumbawa	Indonesia	Asia	island
Rinca Island	Indonesia	Asia	island
Bromo Tengger Semeru	Indonesia	Asia	park
Kinabalu Park	Malaysia	Asia	park
Kota Kinabalu	Malaysia	Asia	city
Penang	Malaysia	Asia	city
Malacca	Malaysia	Asia	cultural
Ipoh	Malaysia	Asia	city
Cameron Highlands	Malaysia	Asia	mountain
Langkawi	Malaysia	Asia	island
Perhentian Islands	Malaysia	Asia	island
Tioman Island	Malaysia	Asia	island
Redang Island	Malaysia	Asia	island
Kuching	Malaysia	Asia	city
Miri	Malaysia	Asia	city
George Town	Malaysia	Asia	city
Johor Bahru	Malaysia	Asia	city
Taiping	Malaysia	Asia	city
Kuala Terengganu	Malaysia	Asia	city
Taman Negara	Malaysia	Asia	park
Bako National Park	Malaysia	Asia	park
Sipadan	Malaysia	Asia	island
Sandakan	Malaysia	Asia	city
Singapore	Singapore	Asia	city
Maldives	Indian Ocean	Asia	island
Male	Maldives	Asia	city
Ari Atoll	Maldives	Asia	island
Vaadhoo Island	Maldives	Asia	island
Baa Atoll	Maldives	Asia	island
Dhigurah	Maldives	Asia	island
Sri Lanka Highlands	Sri Lanka	Asia	mountain
Kandy	Sri Lanka	Asia	city
Galle	Sri Lanka	Asia	city
Mirissa	Sri Lanka	Asia	coast
Arugam Bay	Sri Lanka	Asia	coast
Trincomalee	Sri Lanka	Asia	coast
Sigiriya	Sri Lanka	Asia	cultural
Polonnaruwa	Sri Lanka	Asia	cultural
Nuwara Eliya	Sri Lanka	Asia	mountain
Yala National Park	Sri Lanka	Asia	park
Udawalawe	Sri Lanka	Asia	park
Tangalle	Sri Lanka	Asia	coast
Jaffna	Sri Lanka	Asia	city
Unawatuna	Sri Lanka	Asia	coast
Adam's Peak	Sri Lanka	Asia	mountain
Ella Rock	Sri Lanka	Asia	mountain
Bhutan Himalaya	Bhutan	Asia	mountain
Paro	Bhutan	Asia	city
Thimphu	Bhutan	Asia	city
Punakha	Bhutan	Asia	cultural
Bumthang	Bhutan	Asia	mountain
Phobjikha Valley	Bhutan	Asia	mountain
Kathmandu	Nepal	Asia	city
Pokhara	Nepal	Asia	lake
Chitwan National Park	Nepal	Asia	park
Annapurna	Nepal	Asia	mountain
Everest Region	Nepal	Asia	mountain
Lumbini	Nepal	Asia	cultural
Bandipur	Nepal	Asia	cultural
Nagarkot	Nepal	Asia	mountain
Mustang	Nepal	Asia	mountain
Bhaktapur	Nepal	Asia	cultural
Lhasa	Tibet	Asia	cultural
Leh	India	Asia	mountain
Ladakh	India	Asia	mountain
Amritsar	India	Asia	cultural
Jaipur	India	Asia	city
Jodhpur	India	Asia	city
Jaisalmer	India	Asia	desert
Pushkar	India	Asia	cultural
Rishikesh	India	Asia	mountain
Goa North	India	Asia	coast
Goa South	India	Asia	coast
Hampi	India	Asia	cultural
Mysore	India	Asia	city
Kochi	India	Asia	city
Munnar	India	Asia	mountain
Alleppey	India	Asia	lake
Andaman Islands	India	Asia	island
Pondicherry	India	Asia	city
Chennai	India	Asia	city
Bengaluru	India	Asia	city
Hyderabad	India	Asia	city
Kolkata	India	Asia	city
Darjeeling	India	Asia	mountain
Shimla	India	Asia	mountain
Manali	India	Asia	mountain
Spiti Valley	India	Asia	mountain
Kasol	India	Asia	mountain
Auroville	India	Asia	cultural
Khajuraho	India	Asia	cultural
Orchha	India	Asia	cultural
Ranthambore	India	Asia	park
Jim Corbett National Park	India	Asia	park
Kaziranga	India	Asia	park
Sundarbans	India	Asia	park
Mahabalipuram	India	Asia	cultural
Havelock Island	India	Asia	island
Dharamshala	India	Asia	mountain
Bhopal	India	Asia	city
Ahmedabad	India	Asia	city
Kutch	India	Asia	desert
Islamabad	Pakistan	Asia	city
Lahore	Pakistan	Asia	city
Hunza Valley	Pakistan	Asia	mountain
Skardu	Pakistan	Asia	mountain
Fairy Meadows	Pakistan	Asia	mountain
Karachi	Pakistan	Asia	city
Swat Valley	Pakistan	Asia	mountain
Multan	Pakistan	Asia	cultural
Samarkand	Uzbekistan	Asia	cultural
Bukhara	Uzbekistan	Asia	cultural
Khiva	Uzbekistan	Asia	cultural
Tashkent	Uzbekistan	Asia	city
Nukus	Uzbekistan	Asia	city
Fergana Valley	Uzbekistan	Asia	mountain
Bishkek	Kyrgyzstan	Asia	city
Issyk-Kul	Kyrgyzstan	Asia	lake
Karakol	Kyrgyzstan	Asia	mountain
Song-Kul	Kyrgyzstan	Asia	lake
Osh	Kyrgyzstan	Asia	city
Jeti-Oguz	Kyrgyzstan	Asia	mountain
Dushanbe	Tajikistan	Asia	city
Fann Mountains	Tajikistan	Asia	mountain
Pamir Highway	Tajikistan	Asia	mountain
Khojand	Tajikistan	Asia	city
Murghab	Tajikistan	Asia	mountain
Almaty	Kazakhstan	Asia	city
Astana	Kazakhstan	Asia	city
Turkistan	Kazakhstan	Asia	cultural
Charyn Canyon	Kazakhstan	Asia	desert
Kolsai Lakes	Kazakhstan	Asia	lake
Shymkent	Kazakhstan	Asia	city
Aktau	Kazakhstan	Asia	coast
Ulaanbaatar	Mongolia	Asia	city
Gobi Desert	Mongolia	Asia	desert
Khuvsgul Lake	Mongolia	Asia	lake
Orkhon Valley	Mongolia	Asia	cultural
Terelj	Mongolia	Asia	park
Karakorum	Mongolia	Asia	cultural
Hong Kong	Hong Kong	Asia	city
Macau	Macau	Asia	city
Guangzhou	China	Asia	city
Guilin	China	Asia	mountain
Yangshuo	China	Asia	mountain
Chengdu	China	Asia	city
Chongqing	China	Asia	city
Kunming	China	Asia	city
Dali	China	Asia	cultural
Shangri-La	China	Asia	mountain
Harbin	China	Asia	city
Qingdao	China	Asia	coast
Xiamen	China	Asia	coast
Sanya	China	Asia	coast
Huangshan	China	Asia	mountain
Jiuzhaigou	China	Asia	park
Gansu Corridor	China	Asia	cultural
Dunhuang	China	Asia	desert
Datong	China	Asia	cultural
Pingyao	China	Asia	cultural
Nanjing	China	Asia	city
Wuhan	China	Asia	city
Leshan	China	Asia	cultural
Tiger Leaping Gorge	China	Asia	mountain
Mount Emei	China	Asia	mountain
Beihai	China	Asia	coast
Zhuhai	China	Asia	coast
Lantau Island	Hong Kong	Asia	island
Sun Moon Lake	Taiwan	Asia	lake
Alishan	Taiwan	Asia	mountain
Hualien	Taiwan	Asia	city
Taroko Gorge	Taiwan	Asia	park
Taitung	Taiwan	Asia	coast
Kenting	Taiwan	Asia	coast
Jiufen	Taiwan	Asia	cultural
Tainan Old Town	Taiwan	Asia	cultural
Seoul	South Korea	Asia	city
Busan	South Korea	Asia	city
Gyeongju	South Korea	Asia	cultural
Sokcho	South Korea	Asia	coast
Seoraksan	South Korea	Asia	mountain
Jeonju	South Korea	Asia	cultural
Andong	South Korea	Asia	cultural
Gangneung	South Korea	Asia	coast
Tongyeong	South Korea	Asia	coast
Geoje	South Korea	Asia	coast
Osaka	Japan	Asia	city
Kyoto	Japan	Asia	city
Nara	Japan	Asia	cultural
Hiroshima	Japan	Asia	city
Miyajima	Japan	Asia	cultural
Nagoya	Japan	Asia	city
Sapporo	Japan	Asia	city
Otaru	Japan	Asia	coast
Aomori	Japan	Asia	city
Sendai	Japan	Asia	city
Kamakura	Japan	Asia	cultural
Yokohama	Japan	Asia	city
Kawaguchiko	Japan	Asia	lake
Kiso Valley	Japan	Asia	mountain
Takayama	Japan	Asia	cultural
Kanazawa	Japan	Asia	city
Toyama	Japan	Asia	city
Matsumoto	Japan	Asia	city
Naoshima	Japan	Asia	island
Shikoku	Japan	Asia	island
Yakushima	Japan	Asia	island
Nagasaki	Japan	Asia	city
Beppu	Japan	Asia	city
Kagoshima	Japan	Asia	city
Kumamoto	Japan	Asia	city
Aso	Japan	Asia	mountain
Izu Peninsula	Japan	Asia	coast
Furano	Japan	Asia	mountain
Niseko	Japan	Asia	mountain
Koyasan	Japan	Asia	cultural
Shirakawa-go	Japan	Asia	cultural
Matsue	Japan	Asia	city
Kurashiki	Japan	Asia	cultural
Naha	Japan	Asia	city
Ishigaki	Japan	Asia	island
Kerama Islands	Japan	Asia	island
Tbilisi	Georgia	Asia	city
Kazbegi	Georgia	Asia	mountain
Svaneti	Georgia	Asia	mountain
Kutaisi	Georgia	Asia	city
Batumi	Georgia	Asia	coast
Kakheti	Georgia	Asia	wine
Yerevan	Armenia	Asia	city
Dilijan	Armenia	Asia	mountain
Lake Sevan	Armenia	Asia	lake
Tatev	Armenia	Asia	cultural
Gyumri	Armenia	Asia	city
Baku	Azerbaijan	Asia	city
Sheki	Azerbaijan	Asia	cultural
Gobustan	Azerbaijan	Asia	desert
Ganja	Azerbaijan	Asia	city
Lankaran	Azerbaijan	Asia	coast
Musandam	Oman	Asia	coast
Salalah	Oman	Asia	coast
Nizwa	Oman	Asia	cultural
Wahiba Sands	Oman	Asia	desert
Jebel Akhdar	Oman	Asia	mountain
Khasab	Oman	Asia	coast
Wadi Shab	Oman	Asia	coast
Wadi Bani Khalid	Oman	Asia	lake
Ras Al Khaimah	United Arab Emirates	Asia	mountain
Sharjah	United Arab Emirates	Asia	city
Al Ain	United Arab Emirates	Asia	city
Fujairah	United Arab Emirates	Asia	coast
Hatta	United Arab Emirates	Asia	mountain
Jerusalem	Israel	Asia	cultural
Tel Aviv	Israel	Asia	city
Haifa	Israel	Asia	city
Dead Sea	Jordan	Asia	lake
Wadi Rum	Jordan	Asia	desert
Aqaba	Jordan	Asia	coast
Madaba	Jordan	Asia	cultural
Jerash	Jordan	Asia	cultural
Beirut	Lebanon	Asia	city
Byblos	Lebanon	Asia	cultural
Baalbek	Lebanon	Asia	cultural
Tyre	Lebanon	Asia	coast
Faraya	Lebanon	Asia	mountain
Cappadocia	Turkey	Asia	cultural
Antalya	Turkey	Asia	coast
Bodrum	Turkey	Asia	coast
Fethiye	Turkey	Asia	coast
Kas	Turkey	Asia	coast
Marmaris	Turkey	Asia	coast
Izmir	Turkey	Asia	city
Alaçatı	Turkey	Asia	coast
Trabzon	Turkey	Asia	coast
Mardin	Turkey	Asia	cultural
Mount Nemrut	Turkey	Asia	cultural
Safranbolu	Turkey	Asia	cultural
Pamukkale	Turkey	Asia	cultural
Ani	Turkey	Asia	cultural
Van	Turkey	Asia	lake
Cappadocia Valleys	Turkey	Asia	mountain
Tenerife	Spain	Europe	island
Gran Canaria	Spain	Europe	island
Lanzarote	Spain	Europe	island
Fuerteventura	Spain	Europe	island
Menorca	Spain	Europe	island
Bilbao	Spain	Europe	city
San Sebastián	Spain	Europe	city
Granada	Spain	Europe	city
Cordoba	Spain	Europe	city
Malaga	Spain	Europe	city
Ronda	Spain	Europe	cultural
Cadiz	Spain	Europe	coast
Costa Brava	Spain	Europe	coast
La Palma	Spain	Europe	island
La Gomera	Spain	Europe	island
Asturias	Spain	Europe	coast
Picos de Europa	Spain	Europe	mountain
Santiago de Compostela	Spain	Europe	cultural
Toledo	Spain	Europe	cultural
Zaragoza	Spain	Europe	city
Girona	Spain	Europe	city
Cadaqués	Spain	Europe	coast
Formentera	Spain	Europe	island
Costa del Sol	Spain	Europe	coast
La Rioja	Spain	Europe	wine
Ribera del Duero	Spain	Europe	wine
Bordeaux	France	Europe	city
Lyon	France	Europe	city
Marseille	France	Europe	city
Annecy	France	Europe	lake
Chamonix	France	Europe	mountain
Brittany	France	Europe	coast
Normandy	France	Europe	coast
Strasbourg	France	Europe	city
Colmar	France	Europe	city
Avignon	France	Europe	cultural
Aix-en-Provence	France	Europe	city
Loire Valley	France	Europe	wine
Dordogne	France	Europe	cultural
Mont Saint-Michel	France	Europe	cultural
Biarritz	France	Europe	coast
Corsica	France	Europe	island
Alsace	France	Europe	wine
Burgundy	France	Europe	wine
Provence	France	Europe	wine
Nice Hinterland	France	Europe	mountain
Lille	France	Europe	city
Toulouse	France	Europe	city
Carcassonne	France	Europe	cultural
Sicily East	Italy	Europe	coast
Puglia	Italy	Europe	coast
Lake Como	Italy	Europe	lake
Lake Garda	Italy	Europe	lake
Bologna	Italy	Europe	city
Turin	Italy	Europe	city
Verona	Italy	Europe	city
Genoa	Italy	Europe	city
Cinque Terre Villages	Italy	Europe	coast
Amalfi Coast Villages	Italy	Europe	coast
Dolomites East	Italy	Europe	mountain
South Tyrol	Italy	Europe	mountain
Matera	Italy	Europe	cultural
Bari	Italy	Europe	city
Trieste	Italy	Europe	city
Ravenna	Italy	Europe	cultural
Orvieto	Italy	Europe	cultural
Umbria	Italy	Europe	wine
Etna	Italy	Europe	mountain
Taormina	Italy	Europe	coast
Lecce	Italy	Europe	city
Parma	Italy	Europe	city
Lucca	Italy	Europe	city
Ischia	Italy	Europe	island
Procida	Italy	Europe	island
Elba	Italy	Europe	island
Sorrento	Italy	Europe	coast
Capri	Italy	Europe	island
Bergamo	Italy	Europe	city
Portofino	Italy	Europe	coast
Palermo	Italy	Europe	city
Catania	Italy	Europe	city
Malta	Mediterranean	Europe	island
Valletta	Malta	Europe	city
Gozo	Malta	Europe	island
Comino	Malta	Europe	island
Lisbon	Portugal	Europe	city
Douro Valley	Portugal	Europe	wine
Sintra	Portugal	Europe	cultural
Cascais	Portugal	Europe	coast
Óbidos	Portugal	Europe	cultural
Évora	Portugal	Europe	cultural
Coimbra	Portugal	Europe	city
Braga	Portugal	Europe	city
Aveiro	Portugal	Europe	coast
Azores East	Portugal	Europe	island
São Miguel	Portugal	Europe	island
Pico	Portugal	Europe	island
Alentejo Coast	Portugal	Europe	coast
Nazaré	Portugal	Europe	coast
Douro International	Portugal	Europe	mountain
Madeira North Coast	Portugal	Europe	coast
German Alps	Germany	Europe	mountain
Hamburg	Germany	Europe	city
Cologne	Germany	Europe	city
Heidelberg	Germany	Europe	city
Dresden	Germany	Europe	city
Leipzig	Germany	Europe	city
Nuremberg	Germany	Europe	city
Bamberg	Germany	Europe	cultural
Black Forest	Germany	Europe	mountain
Mosel Valley	Germany	Europe	wine
Rothenburg ob der Tauber	Germany	Europe	cultural
Sylt	Germany	Europe	island
Baden-Baden	Germany	Europe	city
Lübeck	Germany	Europe	cultural
Trier	Germany	Europe	cultural
Saxon Switzerland	Germany	Europe	mountain
Berchtesgaden	Germany	Europe	mountain
Rügen	Germany	Europe	island
Prague	Czech Republic	Europe	city
Cesky Krumlov	Czech Republic	Europe	cultural
Brno	Czech Republic	Europe	city
Kutná Hora	Czech Republic	Europe	cultural
Karlovy Vary	Czech Republic	Europe	city
Bohemian Switzerland	Czech Republic	Europe	mountain
Moravia Wine Region	Czech Republic	Europe	wine
Olomouc	Czech Republic	Europe	city
Brno Lakes	Czech Republic	Europe	lake
Tatra Mountains	Slovakia	Europe	mountain
Kosice	Slovakia	Europe	city
Banska Stiavnica	Slovakia	Europe	cultural
Slovak Paradise	Slovakia	Europe	park
Bratislava Old Town	Slovakia	Europe	cultural
Budapest Danube Bend	Hungary	Europe	cultural
Eger	Hungary	Europe	wine
Lake Balaton	Hungary	Europe	lake
Pécs	Hungary	Europe	city
Szentendre	Hungary	Europe	cultural
Debrecen	Hungary	Europe	city
Transylvania	Romania	Europe	mountain
Sibiu	Romania	Europe	city
Cluj-Napoca	Romania	Europe	city
Brasov Old Town	Romania	Europe	cultural
Sighișoara	Romania	Europe	cultural
Maramureș	Romania	Europe	cultural
Danube Delta	Romania	Europe	park
Constanța	Romania	Europe	coast
Timișoara	Romania	Europe	city
Cliffs of Moher	Ireland	Europe	coast
Galway	Ireland	Europe	city
Cork	Ireland	Europe	city
Killarney	Ireland	Europe	park
Dingle Peninsula	Ireland	Europe	coast
Ring of Kerry	Ireland	Europe	coast
Donegal	Ireland	Europe	coast
Aran Islands	Ireland	Europe	island
Belfast	United Kingdom	Europe	city
Lake District	United Kingdom	Europe	park
Cotswolds	United Kingdom	Europe	cultural
Bath	United Kingdom	Europe	cultural
York	United Kingdom	Europe	cultural
Oxford	United Kingdom	Europe	city
Cambridge	United Kingdom	Europe	city
Cornwall	United Kingdom	Europe	coast
Isle of Skye	United Kingdom	Europe	island
Scottish Highlands	United Kingdom	Europe	mountain
Inverness	United Kingdom	Europe	city
Isle of Mull	United Kingdom	Europe	island
Snowdonia	United Kingdom	Europe	mountain
Pembrokeshire	United Kingdom	Europe	coast
Brighton	United Kingdom	Europe	coast
Bristol	United Kingdom	Europe	city
Manchester	United Kingdom	Europe	city
Liverpool	United Kingdom	Europe	city
Glasgow	United Kingdom	Europe	city
Loch Lomond	United Kingdom	Europe	lake
Orkney	United Kingdom	Europe	island
Shetland	United Kingdom	Europe	island
Faroe Islands	North Atlantic	Europe	island
Torshavn	Faroe Islands	Europe	city
Copenhagen North Zealand	Denmark	Europe	cultural
Aarhus	Denmark	Europe	city
Bornholm	Denmark	Europe	island
Skagen	Denmark	Europe	coast
Odense	Denmark	Europe	city
Samsø	Denmark	Europe	island
Stockholm Archipelago	Sweden	Europe	island
Gothenburg	Sweden	Europe	city
Gotland	Sweden	Europe	island
Visby	Sweden	Europe	cultural
Malmö	Sweden	Europe	city
Åre	Sweden	Europe	mountain
Abisko	Sweden	Europe	mountain
Kiruna	Sweden	Europe	mountain
Lofoten	Norway	Europe	island
Tromsø	Norway	Europe	city
Bergen Fjords	Norway	Europe	coast
Alesund	Norway	Europe	city
Geirangerfjord	Norway	Europe	coast
Trondheim	Norway	Europe	city
Svalbard	Norway	Europe	island
Stavanger	Norway	Europe	city
Preikestolen	Norway	Europe	mountain
Senja	Norway	Europe	island
Finnish Lakeland	Finland	Europe	lake
Helsinki	Finland	Europe	city
Turku	Finland	Europe	city
Rovaniemi	Finland	Europe	city
Lapland	Finland	Europe	mountain
Åland	Finland	Europe	island
Porvoo	Finland	Europe	cultural
Tallinn	Estonia	Europe	city
Tartu	Estonia	Europe	city
Saaremaa	Estonia	Europe	island
Pärnu	Estonia	Europe	coast
Riga	Latvia	Europe	city
Cesis	Latvia	Europe	cultural
Jurmala	Latvia	Europe	coast
Liepāja	Latvia	Europe	coast
Curonian Spit	Lithuania	Europe	coast
Kaunas	Lithuania	Europe	city
Klaipėda	Lithuania	Europe	coast
Nida	Lithuania	Europe	coast
Warsaw Old Town	Poland	Europe	cultural
Krakow	Poland	Europe	city
Gdansk	Poland	Europe	city
Wroclaw	Poland	Europe	city
Poznan	Poland	Europe	city
Zakopane	Poland	Europe	mountain
Masuria	Poland	Europe	lake
Lublin	Poland	Europe	city
Bialowieza	Poland	Europe	park
Zakynthos	Greece	Europe	island
Naxos	Greece	Europe	island
Paros	Greece	Europe	island
Milos	Greece	Europe	island
Crete West	Greece	Europe	coast
Rhodes	Greece	Europe	island
Thessaloniki	Greece	Europe	city
Peloponnese	Greece	Europe	coast
Nafplio	Greece	Europe	cultural
Hydra	Greece	Europe	island
Meteora	Greece	Europe	cultural
Tinos	Greece	Europe	island
Syros	Greece	Europe	island
Sifnos	Greece	Europe	island
Patmos	Greece	Europe	island
Kefalonia	Greece	Europe	island
Lefkada	Greece	Europe	island
Paxos	Greece	Europe	island
Skiathos	Greece	Europe	island
Santorini Villages	Greece	Europe	cultural
Cyprus	Eastern Mediterranean	Europe	island
Paphos	Cyprus	Europe	coast
Limassol	Cyprus	Europe	city
Troodos Mountains	Cyprus	Europe	mountain
Nicosia	Cyprus	Europe	city
Dubrovnik Hinterland	Croatia	Europe	coast
Hvar	Croatia	Europe	island
Korčula	Croatia	Europe	island
Rovinj	Croatia	Europe	coast
Istria	Croatia	Europe	wine
Zadar	Croatia	Europe	city
Šibenik	Croatia	Europe	coast
Plitvice Lakes	Croatia	Europe	park
Mljet	Croatia	Europe	island
Vis	Croatia	Europe	island
Brac	Croatia	Europe	island
Pag	Croatia	Europe	island
Bay of Kotor	Montenegro	Europe	coast
Budva	Montenegro	Europe	coast
Durmitor	Montenegro	Europe	mountain
Lake Skadar	Montenegro	Europe	lake
Perast	Montenegro	Europe	cultural
Lovćen	Montenegro	Europe	mountain
Sarajevo	Bosnia and Herzegovina	Europe	city
Jajce	Bosnia and Herzegovina	Europe	cultural
Blagaj	Bosnia and Herzegovina	Europe	cultural
Trebinje	Bosnia and Herzegovina	Europe	city
Ljubljana	Slovenia	Europe	city
Lake Bled	Slovenia	Europe	lake
Piran	Slovenia	Europe	coast
Soča Valley	Slovenia	Europe	mountain
Maribor	Slovenia	Europe	wine
Triglav National Park	Slovenia	Europe	park
Lake Bohinj	Slovenia	Europe	lake
Belgrade	Serbia	Europe	city
Novi Sad	Serbia	Europe	city
Tara National Park	Serbia	Europe	park
Niš	Serbia	Europe	city
Kopaonik	Serbia	Europe	mountain
Skopje	North Macedonia	Europe	city
Ohrid	North Macedonia	Europe	lake
Mavrovo	North Macedonia	Europe	mountain
Bitola	North Macedonia	Europe	city
Pristina	Kosovo	Europe	city
Prizren	Kosovo	Europe	cultural
Rugova	Kosovo	Europe	mountain
Sofia	Bulgaria	Europe	city
Plovdiv	Bulgaria	Europe	city
Rila Monastery	Bulgaria	Europe	cultural
Bansko	Bulgaria	Europe	mountain
Veliko Tarnovo	Bulgaria	Europe	cultural
Black Sea Coast Bulgaria	Bulgaria	Europe	coast
Koprivshtitsa	Bulgaria	Europe	cultural
Swiss Alps	Switzerland	Europe	mountain
Bern	Switzerland	Europe	city
Lausanne	Switzerland	Europe	city
Montreux	Switzerland	Europe	coast
Jungfrau Region	Switzerland	Europe	mountain
Grindelwald	Switzerland	Europe	mountain
Lugano	Switzerland	Europe	lake
Appenzell	Switzerland	Europe	mountain
Aosta Valley	Italy	Europe	mountain
Hallstatt	Austria	Europe	lake
Graz	Austria	Europe	city
Wachau Valley	Austria	Europe	wine
Zell am See	Austria	Europe	lake
Bad Gastein	Austria	Europe	mountain
Linz	Austria	Europe	city
Tyrol	Austria	Europe	mountain
Iceland South Coast	Iceland	Europe	coast
Akureyri	Iceland	Europe	city
Snæfellsnes	Iceland	Europe	coast
Westfjords	Iceland	Europe	coast
Golden Circle	Iceland	Europe	cultural
East Iceland	Iceland	Europe	coast
Marrakesh Atlas	Morocco	Africa	mountain
Casablanca	Morocco	Africa	city
Rabat	Morocco	Africa	city
Tangier	Morocco	Africa	city
Ouarzazate	Morocco	Africa	desert
Merzouga	Morocco	Africa	desert
Atlas Mountains	Morocco	Africa	mountain
Imlil	Morocco	Africa	mountain
Asilah	Morocco	Africa	coast
Taghazout	Morocco	Africa	coast
Meknes	Morocco	Africa	city
Rwanda	East Africa	Africa	safari
Kigali	Rwanda	Africa	city
Volcanoes National Park	Rwanda	Africa	safari
Lake Kivu	Rwanda	Africa	lake
Akagera	Rwanda	Africa	safari
Musanze	Rwanda	Africa	mountain
Nairobi	Kenya	Africa	city
Lamu	Kenya	Africa	coast
Diani Beach	Kenya	Africa	coast
Watamu	Kenya	Africa	coast
Masai Mara	Kenya	Africa	safari
Naivasha	Kenya	Africa	lake
Samburu	Kenya	Africa	safari
Amboseli	Kenya	Africa	safari
Tsavo	Kenya	Africa	safari
Lake Nakuru	Kenya	Africa	lake
Zanzibar	Tanzania	Africa	island
Stone Town	Tanzania	Africa	cultural
Nungwi	Tanzania	Africa	coast
Pemba Island	Tanzania	Africa	island
Mafia Island	Tanzania	Africa	island
Ngorongoro	Tanzania	Africa	safari
Tarangire	Tanzania	Africa	safari
Arusha	Tanzania	Africa	city
Mikumi	Tanzania	Africa	safari
Ruaha	Tanzania	Africa	safari
Moshi	Tanzania	Africa	city
Kilimanjaro	Tanzania	Africa	mountain
Uganda	East Africa	Africa	safari
Kampala	Uganda	Africa	city
Bwindi	Uganda	Africa	safari
Queen Elizabeth National Park	Uganda	Africa	safari
Jinja	Uganda	Africa	city
Murchison Falls	Uganda	Africa	safari
Entebbe	Uganda	Africa	city
Botswana Delta	Botswana	Africa	safari
Maun	Botswana	Africa	city
Okavango Delta	Botswana	Africa	safari
Chobe	Botswana	Africa	safari
Makgadikgadi	Botswana	Africa	desert
Moremi	Botswana	Africa	safari
Kalahari	Botswana	Africa	desert
Cape Winelands	South Africa	Africa	wine
Stellenbosch	South Africa	Africa	wine
Franschhoek	South Africa	Africa	wine
Hermanus	South Africa	Africa	coast
Garden Route	South Africa	Africa	coast
Plettenberg Bay	South Africa	Africa	coast
Knysna	South Africa	Africa	coast
Drakensberg	South Africa	Africa	mountain
Kruger	South Africa	Africa	safari
Johannesburg North	South Africa	Africa	city
Durban	South Africa	Africa	city
Wild Coast	South Africa	Africa	coast
Cederberg	South Africa	Africa	mountain
Sossusvlei	Namibia	Africa	desert
Namib Desert	Namibia	Africa	desert
Swakopmund	Namibia	Africa	coast
Etosha	Namibia	Africa	safari
Damaraland	Namibia	Africa	desert
Skeleton Coast	Namibia	Africa	coast
Fish River Canyon	Namibia	Africa	desert
Windhoek	Namibia	Africa	city
Victoria Falls	Zimbabwe	Africa	cultural
Hwange	Zimbabwe	Africa	safari
Mana Pools	Zimbabwe	Africa	safari
Harare	Zimbabwe	Africa	city
Bazaruto	Mozambique	Africa	island
Tofo	Mozambique	Africa	coast
Maputo	Mozambique	Africa	city
Vilanculos	Mozambique	Africa	coast
Inhambane	Mozambique	Africa	coast
Nosy Be	Madagascar	Africa	island
Avenue of the Baobabs	Madagascar	Africa	cultural
Isalo	Madagascar	Africa	park
Tsingy de Bemaraha	Madagascar	Africa	park
Île Sainte-Marie	Madagascar	Africa	island
Antsirabe	Madagascar	Africa	city
Dakar	Senegal	Africa	city
Saint-Louis	Senegal	Africa	cultural
Saly	Senegal	Africa	coast
Gorée Island	Senegal	Africa	island
Saloum Delta	Senegal	Africa	park
Praia	Cape Verde	Africa	city
Sal	Cape Verde	Africa	island
Boa Vista	Cape Verde	Africa	island
São Vicente	Cape Verde	Africa	island
Mindelo	Cape Verde	Africa	city
Accra	Ghana	Africa	city
Cape Coast	Ghana	Africa	coast
Elmina	Ghana	Africa	cultural
Kumasi	Ghana	Africa	city
Busua	Ghana	Africa	coast
Abidjan	Côte d'Ivoire	Africa	city
Grand-Bassam	Côte d'Ivoire	Africa	coast
Lagos	Nigeria	Africa	city
Ibadan	Nigeria	Africa	city
Calabar	Nigeria	Africa	coast
Addis Ababa	Ethiopia	Africa	city
Lalibela	Ethiopia	Africa	cultural
Simien Mountains	Ethiopia	Africa	mountain
Bahir Dar	Ethiopia	Africa	lake
Gondar	Ethiopia	Africa	cultural
Mauritius	Indian Ocean	Africa	island
Le Morne	Mauritius	Africa	coast
Black River Gorges	Mauritius	Africa	park
Port Louis	Mauritius	Africa	city
Rodrigues	Mauritius	Africa	island
Seychelles	Indian Ocean	Africa	island
Mahé	Seychelles	Africa	island
Praslin	Seychelles	Africa	island
La Digue	Seychelles	Africa	island
Reunion	Indian Ocean	Africa	island
Mafate	Reunion	Africa	mountain
Cirque de Cilaos	Reunion	Africa	mountain
Mexico City	Mexico	North America	city
Oaxaca	Mexico	North America	city
San Miguel de Allende	Mexico	North America	city
Guanajuato	Mexico	North America	city
Merida	Mexico	North America	city
Bacalar	Mexico	North America	lake
Isla Holbox	Mexico	North America	island
Tulum	Mexico	North America	coast
Isla Mujeres	Mexico	North America	island
Sayulita	Mexico	North America	coast
Puerto Escondido	Mexico	North America	coast
San Cristóbal de las Casas	Mexico	North America	city
Copper Canyon	Mexico	North America	mountain
La Paz	Mexico	North America	coast
Todos Santos	Mexico	North America	coast
Loreto	Mexico	North America	coast
Holbox	Mexico	North America	island
Mérida Yucatán	Mexico	North America	city
Campeche	Mexico	North America	city
Puebla	Mexico	North America	city
Isla Espíritu Santo	Mexico	North America	island
Riviera Nayarit	Mexico	North America	coast
Canada Rockies	Canada	North America	mountain
Vancouver	Canada	North America	city
Montreal	Canada	North America	city
Quebec City	Canada	North America	city
Toronto	Canada	North America	city
Whistler	Canada	North America	mountain
Tofino	Canada	North America	coast
Vancouver Island	Canada	North America	island
Nova Scotia	Canada	North America	coast
Prince Edward Island	Canada	North America	island
Newfoundland	Canada	North America	island
Yukon	Canada	North America	mountain
Jasper	Canada	North America	mountain
Niagara-on-the-Lake	Canada	North America	wine
Ottawa	Canada	North America	city
Haida Gwaii	Canada	North America	island
Kelowna	Canada	North America	wine
Churchill	Canada	North America	safari
Charlevoix	Canada	North America	coast
Calgary	Canada	North America	city
Chicago	United States	North America	city
San Francisco	United States	North America	city
Los Angeles	United States	North America	city
San Diego	United States	North America	city
New Orleans	United States	North America	city
Charleston	United States	North America	city
Savannah	United States	North America	city
Washington DC	United States	North America	city
Boston	United States	North America	city
Seattle	United States	North America	city
Portland	United States	North America	city
Santa Fe	United States	North America	city
Sedona	United States	North America	mountain
Grand Canyon	United States	North America	park
Zion	United States	North America	park
Bryce Canyon	United States	North America	park
Arches	United States	North America	park
Olympic National Park	United States	North America	park
Glacier National Park	United States	North America	park
Acadia	United States	North America	park
Maui	United States	North America	island
Big Island	United States	North America	island
Kauai	United States	North America	island
Martha's Vineyard	United States	North America	island
Nantucket	United States	North America	island
Asheville	United States	North America	mountain
Jackson Hole	United States	North America	mountain
Palm Springs	United States	North America	desert
Monterey	United States	North America	coast
Big Sur	United States	North America	coast
Lake Tahoe	United States	North America	lake
Jacksonville Beaches	United States	North America	coast
Outer Banks	United States	North America	coast
Key West	United States	North America	island
Puerto Rico	Caribbean	North America	island
San Juan	Puerto Rico	North America	city
Vieques	Puerto Rico	North America	island
Culebra	Puerto Rico	North America	island
Dominican Republic	Caribbean	North America	island
Santo Domingo	Dominican Republic	North America	city
Punta Cana	Dominican Republic	North America	coast
Samaná	Dominican Republic	North America	coast
Jamaica	Caribbean	North America	island
Kingston	Jamaica	North America	city
Montego Bay	Jamaica	North America	coast
Port Antonio	Jamaica	North America	coast
Negril	Jamaica	North America	coast
Ocho Rios	Jamaica	North America	coast
Cuba West	Cuba	North America	coast
Trinidad Cuba	Cuba	North America	cultural
Viñales	Cuba	North America	cultural
Varadero	Cuba	North America	coast
Baracoa	Cuba	North America	coast
Cayman Islands	Caribbean	North America	island
Grand Cayman	Cayman Islands	North America	island
Belize City	Belize	North America	city
San Ignacio	Belize	North America	cultural
Placencia	Belize	North America	coast
Ambergris Caye	Belize	North America	island
Caye Caulker	Belize	North America	island
Guatemala Highlands	Guatemala	North America	mountain
Antigua Guatemala	Guatemala	North America	city
Lake Atitlán	Guatemala	North America	lake
Flores	Guatemala	North America	city
Semuc Champey	Guatemala	North America	park
Tikal	Guatemala	North America	cultural
Panama City	Panama	North America	city
Bocas del Toro	Panama	North America	island
Boquete	Panama	North America	mountain
San Blas Islands	Panama	North America	island
Santa Catalina	Panama	North America	coast
Costa Rica Highlands	Costa Rica	North America	mountain
Arenal	Costa Rica	North America	mountain
Monteverde	Costa Rica	North America	mountain
Manuel Antonio	Costa Rica	North America	park
Nosara	Costa Rica	North America	coast
Santa Teresa	Costa Rica	North America	coast
Puerto Viejo de Talamanca	Costa Rica	North America	coast
Tortuguero	Costa Rica	North America	park
Corcovado	Costa Rica	North America	park
Uvita	Costa Rica	North America	coast
Nicaragua	Central America	North America	coast
Granada Nicaragua	Nicaragua	North America	city
León Nicaragua	Nicaragua	North America	city
Ometepe	Nicaragua	North America	island
San Juan del Sur	Nicaragua	North America	coast
Honduras Bay Islands	Honduras	North America	island
Roatán	Honduras	North America	island
Utila	Honduras	North America	island
Copán	Honduras	North America	cultural
El Salvador Coast	El Salvador	North America	coast
Suchitoto	El Salvador	North America	cultural
Ruta de las Flores	El Salvador	North America	mountain
Bogotá	Colombia	South America	city
Medellín	Colombia	South America	city
Cartagena Old Town	Colombia	South America	cultural
Tayrona	Colombia	South America	park
Minca	Colombia	South America	mountain
Salento	Colombia	South America	mountain
Coffee Triangle	Colombia	South America	wine
Guatapé	Colombia	South America	lake
Cali	Colombia	South America	city
Barichara	Colombia	South America	cultural
San Andrés	Colombia	South America	island
Providencia	Colombia	South America	island
Rosario Islands	Colombia	South America	island
Popayán	Colombia	South America	city
Villa de Leyva	Colombia	South America	cultural
Quito	Ecuador	South America	city
Galápagos	Ecuador	South America	island
Cuenca Ecuador	Ecuador	South America	city
Baños	Ecuador	South America	mountain
Cotopaxi	Ecuador	South America	mountain
Otavalo	Ecuador	South America	cultural
Mindo	Ecuador	South America	mountain
Montañita	Ecuador	South America	coast
Guayaquil	Ecuador	South America	city
Lima Coast	Peru	South America	coast
Sacred Valley	Peru	South America	mountain
Arequipa	Peru	South America	city
Colca Canyon	Peru	South America	mountain
Lake Titicaca	Peru	South America	lake
Iquitos	Peru	South America	city
Paracas	Peru	South America	coast
Huacachina	Peru	South America	desert
Huaraz	Peru	South America	mountain
Nazca	Peru	South America	desert
Mancora	Peru	South America	coast
La Paz Bolivia	Bolivia	South America	city
Uyuni	Bolivia	South America	desert
Sucre	Bolivia	South America	city
Copacabana Bolivia	Bolivia	South America	lake
Samaipata	Bolivia	South America	cultural
Potosí	Bolivia	South America	city
Santiago Wine Country	Chile	South America	wine
Valparaíso	Chile	South America	city
Atacama Salt Flats	Chile	South America	desert
Puerto Varas	Chile	South America	lake
Carretera Austral	Chile	South America	coast
Torres del Paine	Chile	South America	mountain
Chiloé	Chile	South America	island
Easter Island	Chile	South America	island
Elqui Valley	Chile	South America	wine
Pucón	Chile	South America	mountain
Valle de Colchagua	Chile	South America	wine
Buenos Aires	Argentina	South America	city
Mendoza	Argentina	South America	wine
El Calafate	Argentina	South America	mountain
El Chaltén	Argentina	South America	mountain
Ushuaia	Argentina	South America	mountain
Iguazú Falls	Argentina	South America	park
Salta	Argentina	South America	city
Jujuy	Argentina	South America	mountain
Bariloche	Argentina	South America	lake
Córdoba Argentina	Argentina	South America	city
Patagonia Atlantic Coast	Argentina	South America	coast
Rosario	Argentina	South America	city
Punta del Este	Uruguay	South America	coast
Montevideo	Uruguay	South America	city
José Ignacio	Uruguay	South America	coast
Colonia del Sacramento	Uruguay	South America	cultural
Florianópolis	Brazil	South America	island
São Paulo	Brazil	South America	city
Salvador	Brazil	South America	city
Paraty	Brazil	South America	coast
Ilha Grande	Brazil	South America	island
Lençóis Maranhenses	Brazil	South America	park
Jericoacoara	Brazil	South America	coast
Iguaçu Falls	Brazil	South America	park
Pantanal	Brazil	South America	safari
Chapada Diamantina	Brazil	South America	park
Fernando de Noronha	Brazil	South America	island
Recife	Brazil	South America	city
Olinda	Brazil	South America	cultural
Búzios	Brazil	South America	coast
Bonito	Brazil	South America	park
Amazon Brazil	Brazil	South America	park
Canoa Quebrada	Brazil	South America	coast
Curitiba	Brazil	South America	city
Brasília	Brazil	South America	city
Amazônia Peruana	Peru	South America	park
Cusco Valley	Peru	South America	mountain
''' 

KIND_META = {
    'city': ('$$', 'Mar–May, Sep–Nov', ['City', 'Cultural', 'Food'], ['solo', 'food'], 'A strong urban base with enough culture, food, and day-trip value to justify a proper stay.'),
    'island': ('$$$', 'Nov–Apr', ['Beach', 'Nature', 'Relaxation'], ['couples', 'beach'], 'An easy high-payoff island pick for beach time, scenery, and switching fully into vacation mode.'),
    'coast': ('$$', 'May–Oct', ['Beach', 'Relaxation', 'Nature'], ['couples', 'road-trip'], 'A scenic coastal stretch or town that works for slow days, good views, and easy trip-building.'),
    'park': ('$$$', 'May–Sep', ['Nature', 'Adventure', 'Hiking'], ['adventure', 'photography'], 'A high-value nature destination built around scenery, wildlife, or hikes worth traveling for.'),
    'mountain': ('$$', 'Jun–Sep', ['Nature', 'Adventure', 'Hiking'], ['adventure', 'photography'], 'A mountain destination with real scenery payoff, active days, and cooler-air reset value.'),
    'lake': ('$$', 'May–Sep', ['Nature', 'Relaxation', 'Romantic'], ['couples', 'photography'], 'A lake-centered destination that earns its place on calm water, views, and an easy slower pace.'),
    'desert': ('$$', 'Oct–Apr', ['Adventure', 'Nature', 'Unfrequented'], ['adventure', 'offbeat'], 'A desert landscape destination with stark scenery, huge skies, and a more remote trip profile.'),
    'cultural': ('$$', 'Apr–Jun, Sep–Oct', ['Cultural', 'Romantic', 'City'], ['history', 'solo'], 'A culture-first destination with strong history, atmosphere, and clear landmark value.'),
    'safari': ('$$$$', 'Jun–Oct', ['Nature', 'Adventure', 'Luxury'], ['safari', 'photography'], 'A safari destination that makes the wildlife payoff the center of the trip.'),
    'wine': ('$$$', 'May–Oct', ['Food', 'Romantic', 'Relaxation'], ['couples', 'food'], 'A wine-region destination that works best when the trip is built around scenery, food, and slow afternoons.'),
}


def slugify(name: str) -> str:
    s = name.casefold().replace('’', "'")
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r"\s+", '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def main() -> None:
    data = json.loads(SOURCE.read_text())
    existing_names = {row.get('name') for row in data if isinstance(row, dict)}
    existing_slugs = {slugify(row.get('name', '')) for row in data if isinstance(row, dict)}
    additions = []
    seen = set()
    for raw in TSV.strip().splitlines():
        name, region, continent, kind = [part.strip() for part in raw.split('\t')]
        slug = slugify(name)
        if name in existing_names or slug in existing_slugs or slug in seen:
            continue
        budget, season, vibes, travel, pitch = KIND_META[kind]
        additions.append({
            'name': name,
            'region': region,
            'continent': continent,
            'photo': FALLBACK_PHOTO,
            'pitch': pitch,
            'budget': budget,
            'season': season,
            'vibes': vibes,
            'travel': travel,
        })
        seen.add(slug)
    if len(additions) < 500:
        raise SystemExit(f'Only {len(additions)} unique additions after filtering; need at least 500')
    additions = additions[:500]
    data.extend(additions)
    data.sort(key=lambda r: r.get('name', '').casefold())
    SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(f'added={len(additions)} total={len(data)}')
    print('sample=', [row['name'] for row in additions[:10]])


if __name__ == '__main__':
    main()
