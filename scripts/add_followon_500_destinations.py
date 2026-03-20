from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'find' / 'destinations.json'
FALLBACK_PHOTO = 'https://img.tabiji.ai/owl-logo.png'

TSV = '''
Tromsø	Norway	Europe	city
Senja	Norway	Europe	island
Alesund	Norway	Europe	city
Jotunheimen National Park	Norway	Europe	park
Geirangerfjord	Norway	Europe	coast
Sognefjord	Norway	Europe	coast
Hardangerfjord	Norway	Europe	coast
Trondheim	Norway	Europe	city
Røros	Norway	Europe	cultural
Preikestolen	Norway	Europe	mountain
Tampere	Finland	Europe	city
Turku	Finland	Europe	city
Rovaniemi	Finland	Europe	city
Lakeland Finland	Finland	Europe	lake
Nuuksio National Park	Finland	Europe	park
Porvoo	Finland	Europe	cultural
Åland Islands	Finland	Europe	island
Saariselkä	Finland	Europe	mountain
Levi	Finland	Europe	mountain
Koli National Park	Finland	Europe	park
Uppsala	Sweden	Europe	city
Malmö	Sweden	Europe	city
Visby	Sweden	Europe	cultural
Swedish Lapland	Sweden	Europe	mountain
Abisko	Sweden	Europe	mountain
Österlen	Sweden	Europe	coast
Kiruna	Sweden	Europe	city
Luleå	Sweden	Europe	city
Marstrand	Sweden	Europe	coast
Sarek National Park	Sweden	Europe	park
Odense	Denmark	Europe	city
Skagen	Denmark	Europe	coast
Ribe	Denmark	Europe	cultural
Møn	Denmark	Europe	coast
Samsø	Denmark	Europe	island
Roskilde	Denmark	Europe	city
Sønderborg	Denmark	Europe	city
Faroe Islands	Faroe Islands	Europe	island
Tórshavn	Faroe Islands	Europe	city
Klaksvík	Faroe Islands	Europe	city
Seyðisfjörður	Iceland	Europe	coast
Akureyri	Iceland	Europe	city
Westfjords	Iceland	Europe	coast
Snæfellsnes Peninsula	Iceland	Europe	coast
Mývatn	Iceland	Europe	lake
Vík	Iceland	Europe	coast
Húsavík	Iceland	Europe	coast
Höfn	Iceland	Europe	coast
Landmannalaugar	Iceland	Europe	mountain
Thingvellir National Park	Iceland	Europe	park
Wicklow Mountains	Ireland	Europe	mountain
Killarney	Ireland	Europe	city
Dingle	Ireland	Europe	coast
Westport	Ireland	Europe	city
Kilkenny	Ireland	Europe	city
Kinsale	Ireland	Europe	coast
Sligo	Ireland	Europe	city
Armagh	Northern Ireland	Europe	city
Derry	Northern Ireland	Europe	city
Causeway Coast	Northern Ireland	Europe	coast
Yorkshire Dales	England	Europe	mountain
Lake District	England	Europe	lake
Peak District	England	Europe	mountain
Northumberland	England	Europe	coast
Canterbury	England	Europe	city
York	England	Europe	city
Edinburgh Old Town	Scotland	Europe	cultural
Isle of Skye	Scotland	Europe	island
Outer Hebrides	Scotland	Europe	island
Cairngorms National Park	Scotland	Europe	park
Loch Lomond	Scotland	Europe	lake
St Andrews	Scotland	Europe	city
Lerwick	Shetland	Europe	city
Orkney	Scotland	Europe	island
Cardiff	Wales	Europe	city
Pembrokeshire	Wales	Europe	coast
Snowdonia	Wales	Europe	mountain
Portmeirion	Wales	Europe	cultural
Llandudno	Wales	Europe	coast
Guernsey	Channel Islands	Europe	island
Jersey	Channel Islands	Europe	island
Luxembourg City	Luxembourg	Europe	city
Mullerthal	Luxembourg	Europe	mountain
Dinant	Belgium	Europe	city
Leuven	Belgium	Europe	city
Ypres	Belgium	Europe	city
Namur	Belgium	Europe	city
Mons	Belgium	Europe	city
Bruges Old Town	Belgium	Europe	cultural
Delft	Netherlands	Europe	city
Leiden	Netherlands	Europe	city
Utrecht	Netherlands	Europe	city
Maastricht	Netherlands	Europe	city
The Hague	Netherlands	Europe	city
Rotterdam	Netherlands	Europe	city
Kinderdijk	Netherlands	Europe	cultural
Texel	Netherlands	Europe	island
Haarlem	Netherlands	Europe	city
Groningen	Netherlands	Europe	city
Colmar Wine Route	France	Europe	roadtrip
Normandy Coast	France	Europe	coast
Mont Saint-Michel	France	Europe	cultural
Loire Valley	France	Europe	cultural
Nantes	France	Europe	city
Toulouse	France	Europe	city
Arles	France	Europe	city
Cassis	France	Europe	coast
Chamonix	France	Europe	mountain
Menton	France	Europe	city
Lille	France	Europe	city
Strasbourg	France	Europe	city
Reims	France	Europe	city
Provence	France	Europe	roadtrip
Annecy	France	Europe	city
Biarritz	France	Europe	coast
Carcassonne	France	Europe	cultural
Dordogne	France	Europe	cultural
Aix-en-Provence	France	Europe	city
Aosta Valley	Italy	Europe	mountain
Turin Hills	Italy	Europe	roadtrip
Lake Garda	Italy	Europe	lake
Bologna Hills	Italy	Europe	roadtrip
Ravenna	Italy	Europe	city
Trieste	Italy	Europe	city
Perugia	Italy	Europe	city
Orvieto	Italy	Europe	city
Lucca	Italy	Europe	city
Siena	Italy	Europe	city
Cinque Terre	Italy	Europe	coast
Liguria	Italy	Europe	coast
Parma	Italy	Europe	city
Modena	Italy	Europe	city
Bergamo	Italy	Europe	city
Verona Hills	Italy	Europe	roadtrip
Ischia	Italy	Europe	island
Procida	Italy	Europe	island
Capri	Italy	Europe	island
Taormina	Italy	Europe	city
Catania	Italy	Europe	city
Aeolian Islands	Italy	Europe	island
Val d'Orcia	Italy	Europe	roadtrip
Dolomites	Italy	Europe	mountain
Bled	Slovenia	Europe	lake
Ljubljana	Slovenia	Europe	city
Piran	Slovenia	Europe	coast
Soča Valley	Slovenia	Europe	mountain
Maribor	Slovenia	Europe	city
Postojna	Slovenia	Europe	cultural
Plitvice Lakes	Croatia	Europe	park
Rovinj	Croatia	Europe	city
Hvar	Croatia	Europe	island
Korčula	Croatia	Europe	island
Zadar	Croatia	Europe	city
Šibenik	Croatia	Europe	city
Istria	Croatia	Europe	roadtrip
Mljet	Croatia	Europe	island
Pag	Croatia	Europe	island
Pelješac	Croatia	Europe	coast
Budva	Montenegro	Europe	coast
Durmitor National Park	Montenegro	Europe	park
Perast	Montenegro	Europe	city
Ulcinj	Montenegro	Europe	coast
Lovćen	Montenegro	Europe	mountain
Sarajevo	Bosnia and Herzegovina	Europe	city
Jajce	Bosnia and Herzegovina	Europe	cultural
Blagaj	Bosnia and Herzegovina	Europe	cultural
Trebinje	Bosnia and Herzegovina	Europe	city
Una National Park	Bosnia and Herzegovina	Europe	park
Ohrid	North Macedonia	Europe	lake
Bitola	North Macedonia	Europe	city
Mavrovo National Park	North Macedonia	Europe	park
Matka Canyon	North Macedonia	Europe	mountain
Pristina	Kosovo	Europe	city
Prizren	Kosovo	Europe	city
Peja	Kosovo	Europe	city
Shkodër	Albania	Europe	city
Berat	Albania	Europe	city
Gjirokastër	Albania	Europe	city
Albanian Riviera	Albania	Europe	coast
Theth	Albania	Europe	mountain
Ksamil	Albania	Europe	coast
Valbona	Albania	Europe	mountain
Sofia	Bulgaria	Europe	city
Plovdiv	Bulgaria	Europe	city
Veliko Tarnovo	Bulgaria	Europe	city
Bansko	Bulgaria	Europe	mountain
Rila Monastery	Bulgaria	Europe	cultural
Sunny Beach	Bulgaria	Europe	coast
Varna	Bulgaria	Europe	city
Brașov	Romania	Europe	city
Sibiu	Romania	Europe	city
Cluj-Napoca	Romania	Europe	city
Sighișoara	Romania	Europe	city
Maramureș	Romania	Europe	cultural
Bucegi Mountains	Romania	Europe	mountain
Viscri	Romania	Europe	cultural
Timișoara	Romania	Europe	city
Sinaia	Romania	Europe	mountain
Iași	Romania	Europe	city
Brno	Czech Republic	Europe	city
Olomouc	Czech Republic	Europe	city
Český Krumlov	Czech Republic	Europe	city
Kutná Hora	Czech Republic	Europe	cultural
Bohemian Switzerland	Czech Republic	Europe	park
Karlovy Vary	Czech Republic	Europe	city
Pilsen	Czech Republic	Europe	city
Telč	Czech Republic	Europe	city
Mikulov	Czech Republic	Europe	city
Bratislava Wine Region	Slovakia	Europe	roadtrip
Košice	Slovakia	Europe	city
High Tatras	Slovakia	Europe	mountain
Banská Štiavnica	Slovakia	Europe	city
Slovak Paradise	Slovakia	Europe	park
Esztergom	Hungary	Europe	city
Pécs	Hungary	Europe	city
Eger	Hungary	Europe	city
Balatonfüred	Hungary	Europe	lake
Szentendre	Hungary	Europe	city
Debrecen	Hungary	Europe	city
Gdańsk Old Town	Poland	Europe	cultural
Wrocław	Poland	Europe	city
Poznań	Poland	Europe	city
Zakopane	Poland	Europe	mountain
Białowieża Forest	Poland	Europe	park
Lublin	Poland	Europe	city
Toruń	Poland	Europe	city
Łódź	Poland	Europe	city
Masurian Lakes	Poland	Europe	lake
Hel Peninsula	Poland	Europe	coast
Tallinn	Estonia	Europe	city
Tartu	Estonia	Europe	city
Saaremaa	Estonia	Europe	island
Pärnu	Estonia	Europe	coast
Lahemaa National Park	Estonia	Europe	park
Riga	Latvia	Europe	city
Jūrmala	Latvia	Europe	coast
Cēsis	Latvia	Europe	city
Gauja National Park	Latvia	Europe	park
Liepāja	Latvia	Europe	coast
Kaunas	Lithuania	Europe	city
Klaipėda	Lithuania	Europe	city
Curonian Spit	Lithuania	Europe	coast
Trakai	Lithuania	Europe	cultural
Aukštaitija National Park	Lithuania	Europe	park
Minsk	Belarus	Europe	city
Hrodna	Belarus	Europe	city
Brest	Belarus	Europe	city
Lviv	Ukraine	Europe	city
Kyiv	Ukraine	Europe	city
Odesa	Ukraine	Europe	city
Chernivtsi	Ukraine	Europe	city
Kamianets-Podilskyi	Ukraine	Europe	city
Chișinău	Moldova	Europe	city
Orheiul Vechi	Moldova	Europe	cultural
Tbilisi Old Town	Georgia	Asia	cultural
Kazbegi	Georgia	Asia	mountain
Svaneti	Georgia	Asia	mountain
Batumi	Georgia	Asia	coast
Kakheti	Georgia	Asia	roadtrip
Mtskheta	Georgia	Asia	cultural
Kutaisi	Georgia	Asia	city
Yerevan Highlands	Armenia	Asia	roadtrip
Dilijan	Armenia	Asia	mountain
Gyumri	Armenia	Asia	city
Tatev	Armenia	Asia	cultural
Sevan	Armenia	Asia	lake
Baku	Azerbaijan	Asia	city
Sheki	Azerbaijan	Asia	city
Ganja	Azerbaijan	Asia	city
Gobustan	Azerbaijan	Asia	cultural
Lankaran	Azerbaijan	Asia	coast
Istanbul Asian Side	Turkey	Asia	city
Antalya	Turkey	Asia	coast
Fethiye	Turkey	Asia	coast
Marmaris	Turkey	Asia	coast
Alaçatı	Turkey	Asia	coast
Çeşme	Turkey	Asia	coast
Pamukkale	Turkey	Asia	cultural
Ephesus	Turkey	Asia	cultural
Bursa	Turkey	Asia	city
Mardin	Turkey	Asia	city
Kaş	Turkey	Asia	coast
Trabzon	Turkey	Asia	city
Mount Nemrut	Turkey	Asia	mountain
Ani	Turkey	Asia	cultural
Gaziantep	Turkey	Asia	city
Aqaba	Jordan	Asia	coast
Wadi Mujib	Jordan	Asia	mountain
Madaba	Jordan	Asia	city
Jerash	Jordan	Asia	cultural
Dead Sea Jordan	Jordan	Asia	lake
Amman Hills	Jordan	Asia	city
Jerusalem	Israel	Asia	city
Haifa	Israel	Asia	city
Nazareth	Israel	Asia	city
Eilat	Israel	Asia	coast
Masada	Israel	Asia	cultural
Galilee	Israel	Asia	lake
Bethlehem	Palestine	Asia	city
Ramallah	Palestine	Asia	city
Beirut	Lebanon	Asia	city
Byblos	Lebanon	Asia	cultural
Baalbek	Lebanon	Asia	cultural
Batroun	Lebanon	Asia	coast
Faraya	Lebanon	Asia	mountain
Jbeil Coast	Lebanon	Asia	coast
Jebel Akhdar	Oman	Asia	mountain
Nizwa	Oman	Asia	city
Sur	Oman	Asia	coast
Salalah	Oman	Asia	coast
Wahiba Sands	Oman	Asia	desert
Khasab	Oman	Asia	coast
Al Ain	United Arab Emirates	Asia	city
Ras Al Khaimah	United Arab Emirates	Asia	coast
Fujairah	United Arab Emirates	Asia	coast
Hatta	United Arab Emirates	Asia	mountain
Sharjah	United Arab Emirates	Asia	city
AlUla	Saudi Arabia	Asia	cultural
Jeddah	Saudi Arabia	Asia	city
Riyadh	Saudi Arabia	Asia	city
Abha	Saudi Arabia	Asia	mountain
Taif	Saudi Arabia	Asia	mountain
Umluj	Saudi Arabia	Asia	coast
Manama	Bahrain	Asia	city
Muharraq	Bahrain	Asia	city
Doha Corniche	Qatar	Asia	city
Al Zubarah	Qatar	Asia	cultural
Kuwait City	Kuwait	Asia	city
Failaka Island	Kuwait	Asia	island
Baghdad	Iraq	Asia	city
Erbil	Iraq	Asia	city
Sulaymaniyah	Iraq	Asia	city
Najaf	Iraq	Asia	city
Tehran	Iran	Asia	city
Shiraz	Iran	Asia	city
Yazd	Iran	Asia	city
Tabriz	Iran	Asia	city
Kashan	Iran	Asia	city
Qeshm	Iran	Asia	island
Hormuz Island	Iran	Asia	island
Masuleh	Iran	Asia	mountain
Sana'a	Yemen	Asia	city
Aden	Yemen	Asia	city
Socotra	Yemen	Asia	island
Lhasa	Tibet	Asia	city
Shigatse	Tibet	Asia	city
Namtso	Tibet	Asia	lake
Kathmandu Valley	Nepal	Asia	cultural
Bhaktapur	Nepal	Asia	city
Patan	Nepal	Asia	city
Nagarkot	Nepal	Asia	mountain
Mustang	Nepal	Asia	mountain
Lumbini	Nepal	Asia	cultural
Bandipur	Nepal	Asia	city
Chitwan	Nepal	Asia	park
Annapurna Circuit	Nepal	Asia	mountain
Everest Base Camp	Nepal	Asia	mountain
Ladakh	India	Asia	mountain
Shimla	India	Asia	mountain
Manali	India	Asia	mountain
Spiti Valley	India	Asia	mountain
Kasol	India	Asia	mountain
Mysore	India	Asia	city
Alleppey	India	Asia	lake
Pondicherry	India	Asia	city
Chennai	India	Asia	city
Bengaluru	India	Asia	city
Hyderabad	India	Asia	city
Kolkata	India	Asia	city
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
Ahmedabad	India	Asia	city
Kutch	India	Asia	desert
Islamabad	Pakistan	Asia	city
Lahore	Pakistan	Asia	city
Hunza Valley	Pakistan	Asia	mountain
Skardu	Pakistan	Asia	mountain
Fairy Meadows	Pakistan	Asia	mountain
Karachi	Pakistan	Asia	city
Swat Valley	Pakistan	Asia	mountain
Multan	Pakistan	Asia	city
Tashkent	Uzbekistan	Asia	city
Nukus	Uzbekistan	Asia	city
Fergana Valley	Uzbekistan	Asia	mountain
Bishkek	Kyrgyzstan	Asia	city
Issyk-Kul	Kyrgyzstan	Asia	lake
Karakol	Kyrgyzstan	Asia	mountain
Song-Kul	Kyrgyzstan	Asia	lake
Osh	Kyrgyzstan	Asia	city
Jeti-Oguz	Kyrgyzstan	Asia	mountain
Pamir Highway	Tajikistan	Asia	roadtrip
Khojand	Tajikistan	Asia	city
Murghab	Tajikistan	Asia	mountain
Astana	Kazakhstan	Asia	city
Turkistan	Kazakhstan	Asia	cultural
Charyn Canyon	Kazakhstan	Asia	desert
Kolsai Lakes	Kazakhstan	Asia	lake
Shymkent	Kazakhstan	Asia	city
Ulaanbaatar Steppe	Mongolia	Asia	roadtrip
Gobi Desert	Mongolia	Asia	desert
Khuvsgul Lake	Mongolia	Asia	lake
Orkhon Valley	Mongolia	Asia	cultural
Terelj	Mongolia	Asia	park
Karakorum	Mongolia	Asia	cultural
Macau Peninsula	Macau	Asia	city
Chengdu Alleys	China	Asia	city
Kunming	China	Asia	city
Dali	China	Asia	cultural
Shangri-La	China	Asia	mountain
Xiamen	China	Asia	coast
Sanya	China	Asia	coast
Huangshan	China	Asia	mountain
Jiuzhaigou	China	Asia	park
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
Suzhou Canals	China	Asia	city
Hangzhou Tea Country	China	Asia	roadtrip
Lijiang Old Town	China	Asia	cultural
Zhangjiajie Forest Park	China	Asia	park
Shenzhen Bay	China	Asia	city
Jiufen	Taiwan	Asia	city
Taitung	Taiwan	Asia	coast
Hualien	Taiwan	Asia	city
Sun Moon Lake	Taiwan	Asia	lake
Alishan	Taiwan	Asia	mountain
Kenting	Taiwan	Asia	coast
Taichung	Taiwan	Asia	city
Tamsui	Taiwan	Asia	city
Ishigaki	Japan	Asia	island
Kerama Islands	Japan	Asia	island
Izu Peninsula	Japan	Asia	coast
Kawaguchiko	Japan	Asia	lake
Aso	Japan	Asia	mountain
Hiroshima	Japan	Asia	city
Kamakura Coast	Japan	Asia	coast
Otaru Canal	Japan	Asia	city
Hakodate Bay	Japan	Asia	city
Aomori Bay	Japan	Asia	city
Jeonju Hanok Village	South Korea	Asia	cultural
Andong Hahoe	South Korea	Asia	cultural
Suncheon Bay	South Korea	Asia	coast
Gangneung Coast	South Korea	Asia	coast
Tongyeong	South Korea	Asia	city
Yeosu	South Korea	Asia	city
Geoje	South Korea	Asia	island
Jeju Olle	South Korea	Asia	roadtrip
Vang Vieng Karsts	Laos	Asia	mountain
Pakse Loop	Laos	Asia	roadtrip
Si Phan Don	Laos	Asia	island
Plain of Jars	Laos	Asia	cultural
Nong Khiaw	Laos	Asia	mountain
Phonsavan	Laos	Asia	cultural
Savannakhet	Laos	Asia	city
Kep Coast	Cambodia	Asia	coast
Koh Rong	Cambodia	Asia	island
Kampong Thom	Cambodia	Asia	cultural
Kratie	Cambodia	Asia	city
Mondulkiri	Cambodia	Asia	mountain
Preah Vihear	Cambodia	Asia	cultural
Koh Rong Samloem	Cambodia	Asia	island
Tonle Sap Villages	Cambodia	Asia	lake
Batanes Islands	Philippines	Asia	island
Puerto Princesa	Philippines	Asia	city
Dumaguete	Philippines	Asia	city
Bantayan Island	Philippines	Asia	island
Samar	Philippines	Asia	island
Sorsogon	Philippines	Asia	coast
Vigan	Philippines	Asia	city
Sagada	Philippines	Asia	mountain
Banaue	Philippines	Asia	mountain
Panglao	Philippines	Asia	island
Gili Trawangan Nights	Indonesia	Asia	island
Gili Air Days	Indonesia	Asia	island
Nusa Lembongan	Indonesia	Asia	island
Raja Ampat Islands	Indonesia	Asia	island
Flores Overland	Indonesia	Asia	roadtrip
Mount Bromo Sunrise	Indonesia	Asia	mountain
Ijen Crater	Indonesia	Asia	mountain
Bandung Highlands	Indonesia	Asia	city
Surabaya	Indonesia	Asia	city
Semarang	Indonesia	Asia	city
Makassar	Indonesia	Asia	city
Lake Toba	Indonesia	Asia	lake
Bukit Lawang	Indonesia	Asia	park
Tana Toraja	Indonesia	Asia	cultural
Borobudur Sunrise	Indonesia	Asia	cultural
Prambanan	Indonesia	Asia	cultural
Belitung	Indonesia	Asia	island
Malang	Indonesia	Asia	city
Medan	Indonesia	Asia	city
Padang	Indonesia	Asia	city
Sumba	Indonesia	Asia	island
Sumatra Highlands	Indonesia	Asia	mountain
Sulawesi Coast	Indonesia	Asia	coast
Sumbawa Surf	Indonesia	Asia	coast
Rinca Island	Indonesia	Asia	island
Cameron Highlands	Malaysia	Asia	mountain
Tioman Island	Malaysia	Asia	island
Redang Island	Malaysia	Asia	island
Kuching	Malaysia	Asia	city
Miri	Malaysia	Asia	city
Johor Bahru	Malaysia	Asia	city
Taiping	Malaysia	Asia	city
Kuala Terengganu	Malaysia	Asia	city
Taman Negara	Malaysia	Asia	park
Bako National Park	Malaysia	Asia	park
Sipadan	Malaysia	Asia	island
Sandakan	Malaysia	Asia	city
Male	Maldives	Asia	city
Ari Atoll	Maldives	Asia	island
Vaadhoo Island	Maldives	Asia	island
Dhigurah	Maldives	Asia	island
Galle Fort	Sri Lanka	Asia	cultural
Mirissa	Sri Lanka	Asia	coast
Arugam Bay	Sri Lanka	Asia	coast
Trincomalee	Sri Lanka	Asia	coast
Sigiriya	Sri Lanka	Asia	cultural
Polonnaruwa	Sri Lanka	Asia	cultural
Nuwara Eliya	Sri Lanka	Asia	mountain
Yala National Park	Sri Lanka	Asia	park
Udawalawe	Sri Lanka	Asia	park
Tangalle	Sri Lanka	Asia	coast
Jaffna Peninsula	Sri Lanka	Asia	coast
Unawatuna	Sri Lanka	Asia	coast
Paro Valley	Bhutan	Asia	mountain
Punakha	Bhutan	Asia	cultural
Bumthang Valley	Bhutan	Asia	mountain
Phobjikha Valley	Bhutan	Asia	mountain
Marrakesh Medina	Morocco	Africa	cultural
Chefchaouen Hills	Morocco	Africa	mountain
Fez Medina	Morocco	Africa	cultural
Tangier	Morocco	Africa	city
Essaouira	Morocco	Africa	coast
Taghazout	Morocco	Africa	coast
Merzouga	Morocco	Africa	desert
Atlas Mountains	Morocco	Africa	mountain
Asilah	Morocco	Africa	coast
Tetouan	Morocco	Africa	city
Tunis	Tunisia	Africa	city
Sidi Bou Said	Tunisia	Africa	coast
Djerba	Tunisia	Africa	island
Kairouan	Tunisia	Africa	cultural
Tozeur	Tunisia	Africa	desert
Carthage	Tunisia	Africa	cultural
Siwa Oasis	Egypt	Africa	desert
Luxor West Bank	Egypt	Africa	cultural
Aswan	Egypt	Africa	city
Dahab	Egypt	Africa	coast
Sharm el-Sheikh	Egypt	Africa	coast
White Desert	Egypt	Africa	desert
Nile Valley Egypt	Egypt	Africa	roadtrip
Giza	Egypt	Africa	cultural
Cape Town Winelands	South Africa	Africa	roadtrip
Garden Route	South Africa	Africa	roadtrip
Drakensberg	South Africa	Africa	mountain
Hluhluwe-Imfolozi	South Africa	Africa	park
Hermanus	South Africa	Africa	coast
Knysna	South Africa	Africa	coast
Franschhoek	South Africa	Africa	city
Stellenbosch	South Africa	Africa	city
Durban	South Africa	Africa	city
Soweto	South Africa	Africa	city
Maputo	Mozambique	Africa	city
Bazaruto Archipelago	Mozambique	Africa	island
Tofo	Mozambique	Africa	coast
Vilanculos	Mozambique	Africa	coast
Stone Town	Tanzania	Africa	city
Paje	Tanzania	Africa	coast
Nungwi	Tanzania	Africa	coast
Ngorongoro	Tanzania	Africa	park
Tarangire	Tanzania	Africa	park
Ruaha National Park	Tanzania	Africa	park
Arusha	Tanzania	Africa	city
Moshi	Tanzania	Africa	city
Mafia Island	Tanzania	Africa	island
Lamu	Kenya	Africa	island
Diani Beach	Kenya	Africa	coast
Watamu	Kenya	Africa	coast
Naivasha	Kenya	Africa	lake
Maasai Mara	Kenya	Africa	park
Amboseli	Kenya	Africa	park
Nairobi National Park	Kenya	Africa	park
Kisumu	Kenya	Africa	city
Entebbe	Uganda	Africa	city
Jinja	Uganda	Africa	city
Bwindi	Uganda	Africa	park
Murchison Falls	Uganda	Africa	park
Lake Bunyonyi	Uganda	Africa	lake
Kigali Hills	Rwanda	Africa	roadtrip
Volcanoes National Park	Rwanda	Africa	park
Lake Kivu	Rwanda	Africa	lake
Butare	Rwanda	Africa	city
Nyungwe Forest	Rwanda	Africa	park
Lalibela	Ethiopia	Africa	cultural
Gondar	Ethiopia	Africa	city
Bahir Dar	Ethiopia	Africa	city
Simien Mountains	Ethiopia	Africa	mountain
Danakil Depression	Ethiopia	Africa	desert
Harar	Ethiopia	Africa	city
Accra Coast	Ghana	Africa	coast
Cape Coast	Ghana	Africa	city
Kumasi	Ghana	Africa	city
Mole National Park	Ghana	Africa	park
Ada Foah	Ghana	Africa	coast
Dakar	Senegal	Africa	city
Saint-Louis	Senegal	Africa	city
Saly	Senegal	Africa	coast
Casamance	Senegal	Africa	coast
Lagos	Nigeria	Africa	city
Abuja	Nigeria	Africa	city
Calabar	Nigeria	Africa	city
Ibadan	Nigeria	Africa	city
Abidjan Lagoons	Côte d'Ivoire	Africa	coast
Grand-Bassam	Côte d'Ivoire	Africa	city
Cotonou	Benin	Africa	city
Ouidah	Benin	Africa	cultural
Porto-Novo	Benin	Africa	city
Lomé	Togo	Africa	city
Banjul	Gambia	Africa	city
Bissau	Guinea-Bissau	Africa	city
Praia	Cape Verde	Africa	city
Sal	Cape Verde	Africa	island
Boa Vista	Cape Verde	Africa	island
Mindelo	Cape Verde	Africa	city
São Tomé	São Tomé and Príncipe	Africa	island
Príncipe	São Tomé and Príncipe	Africa	island
Windhoek	Namibia	Africa	city
Sossusvlei	Namibia	Africa	desert
Swakopmund	Namibia	Africa	coast
Etosha	Namibia	Africa	park
Skeleton Coast	Namibia	Africa	coast
Walvis Bay	Namibia	Africa	coast
Gaborone	Botswana	Africa	city
Okavango Delta	Botswana	Africa	park
Chobe National Park	Botswana	Africa	park
Makgadikgadi	Botswana	Africa	desert
Maun	Botswana	Africa	city
Kasane	Botswana	Africa	city
Victoria Falls	Zimbabwe	Africa	cultural
Hwange	Zimbabwe	Africa	park
Mana Pools	Zimbabwe	Africa	park
Harare	Zimbabwe	Africa	city
Livingstone	Zambia	Africa	city
South Luangwa	Zambia	Africa	park
Lusaka	Zambia	Africa	city
Lake Malawi	Malawi	Africa	lake
Liwonde	Malawi	Africa	park
Lilongwe	Malawi	Africa	city
Antananarivo	Madagascar	Africa	city
Nosy Be	Madagascar	Africa	island
Île Sainte-Marie	Madagascar	Africa	island
Avenue of the Baobabs	Madagascar	Africa	cultural
Andasibe	Madagascar	Africa	park
Mahajanga	Madagascar	Africa	coast
Port Louis	Mauritius	Africa	city
Le Morne	Mauritius	Africa	coast
Black River Gorges	Mauritius	Africa	park
Rodrigues	Mauritius	Africa	island
Mahé	Seychelles	Africa	island
Praslin	Seychelles	Africa	island
La Digue	Seychelles	Africa	island
Réunion	Réunion	Africa	island
Mafate	Réunion	Africa	mountain
Saint-Denis	Réunion	Africa	city
Salvador	Brazil	South America	city
Florianópolis	Brazil	South America	coast
Paraty	Brazil	South America	city
Jericoacoara	Brazil	South America	coast
Lençóis Maranhenses	Brazil	South America	park
Iguaçu Falls	Brazil	South America	park
Ouro Preto	Brazil	South America	city
Belo Horizonte	Brazil	South America	city
Recife	Brazil	South America	city
Olinda	Brazil	South America	city
Fernando de Noronha	Brazil	South America	island
Pantanal	Brazil	South America	park
Ilhabela	Brazil	South America	island
São Paulo	Brazil	South America	city
Jericoacoara Dunes	Brazil	South America	desert
Mendoza Wine Country	Argentina	South America	roadtrip
Bariloche	Argentina	South America	city
Salta	Argentina	South America	city
Ushuaia	Argentina	South America	city
El Chaltén	Argentina	South America	mountain
Iguazú Argentina	Argentina	South America	park
Córdoba Argentina	Argentina	South America	city
Mar del Plata	Argentina	South America	coast
El Calafate	Argentina	South America	city
Valparaíso	Chile	South America	city
San Pedro de Atacama	Chile	South America	desert
Puerto Varas	Chile	South America	city
Chiloé	Chile	South America	island
Torres del Paine	Chile	South America	park
Valle de Elqui	Chile	South America	mountain
Pucón	Chile	South America	mountain
Vina del Mar	Chile	South America	coast
La Paz	Bolivia	South America	city
Salar de Uyuni	Bolivia	South America	desert
Sucre	Bolivia	South America	city
Cochabamba	Bolivia	South America	city
Madidi	Bolivia	South America	park
Copacabana Bolivia	Bolivia	South America	lake
Arequipa	Peru	South America	city
Sacred Valley	Peru	South America	mountain
Paracas	Peru	South America	coast
Huacachina	Peru	South America	desert
Colca Canyon	Peru	South America	mountain
Huaraz	Peru	South America	mountain
Lake Titicaca Peru	Peru	South America	lake
Trujillo Peru	Peru	South America	city
Iquitos	Peru	South America	city
Uyuni Route Peru	Peru	South America	roadtrip
Cuenca	Ecuador	South America	city
Baños	Ecuador	South America	city
Otavalo	Ecuador	South America	city
Quito Highlands	Ecuador	South America	roadtrip
Mindo	Ecuador	South America	park
Guayaquil	Ecuador	South America	city
Galápagos	Ecuador	South America	island
Medellín Hills	Colombia	South America	roadtrip
Cartagena Walled City	Colombia	South America	cultural
Salento	Colombia	South America	city
Tayrona	Colombia	South America	park
San Andrés	Colombia	South America	island
Villa de Leyva	Colombia	South America	city
Barichara	Colombia	South America	city
Cali	Colombia	South America	city
Guatapé	Colombia	South America	city
Providencia	Colombia	South America	island
Montevideo Rambla	Uruguay	South America	city
Punta del Este	Uruguay	South America	coast
Colonia del Sacramento	Uruguay	South America	city
José Ignacio	Uruguay	South America	coast
Asunción	Paraguay	South America	city
Encarnación	Paraguay	South America	city
Gran Chaco	Paraguay	South America	park
Georgetown Guyana	Guyana	South America	city
Kaieteur Falls	Guyana	South America	park
Paramaribo	Suriname	South America	city
Brokopondo	Suriname	South America	lake
Canaima	Venezuela	South America	park
Mérida Venezuela	Venezuela	South America	city
Los Roques	Venezuela	South America	island
Curacao	Caribbean	North America	island
Aruba	Caribbean	North America	island
Bonaire	Caribbean	North America	island
Curaçao Willemstad	Caribbean	North America	city
San Juan	Puerto Rico	North America	city
Vieques	Puerto Rico	North America	island
Culebra	Puerto Rico	North America	island
Rincón	Puerto Rico	North America	coast
Samaná	Dominican Republic	North America	coast
Jarabacoa	Dominican Republic	North America	mountain
Santo Domingo	Dominican Republic	North America	city
Punta Cana	Dominican Republic	North America	coast
Cabarete	Dominican Republic	North America	coast
Negril	Jamaica	North America	coast
Treasure Beach	Jamaica	North America	coast
Port Antonio	Jamaica	North America	coast
Blue Mountains Jamaica	Jamaica	North America	mountain
Nassau	Bahamas	North America	city
Exumas	Bahamas	North America	island
Harbour Island	Bahamas	North America	island
George Town Exuma	Bahamas	North America	city
Bridgetown	Barbados	North America	city
Bathsheba	Barbados	North America	coast
Saint Lucia	Caribbean	North America	island
Soufrière	Saint Lucia	North America	coast
Antigua	Caribbean	North America	island
Barbuda	Caribbean	North America	island
Grenada	Caribbean	North America	island
Bequia	Saint Vincent and the Grenadines	North America	island
Canouan	Saint Vincent and the Grenadines	North America	island
Tobago	Trinidad and Tobago	North America	island
Trinidad Port of Spain	Trinidad and Tobago	North America	city
Caye Caulker	Belize	North America	island
Placencia	Belize	North America	coast
Hopkins	Belize	North America	coast
San Ignacio Belize	Belize	North America	city
Ambergris Caye	Belize	North America	island
Lake Atitlán	Guatemala	North America	lake
Antigua Guatemala	Guatemala	North America	city
Semuc Champey	Guatemala	North America	park
Flores Guatemala	Guatemala	North America	city
Tikal	Guatemala	North America	cultural
León	Nicaragua	North America	city
Granada Nicaragua	Nicaragua	North America	city
Ometepe	Nicaragua	North America	island
San Juan del Sur	Nicaragua	North America	coast
Corn Islands	Nicaragua	North America	island
Monteverde	Costa Rica	North America	park
Nosara	Costa Rica	North America	coast
Puerto Viejo	Costa Rica	North America	coast
Corcovado	Costa Rica	North America	park
Tamarindo	Costa Rica	North America	coast
La Fortuna	Costa Rica	North America	mountain
Santa Teresa Costa Rica	Costa Rica	North America	coast
Manuel Antonio	Costa Rica	North America	park
Boquete	Panama	North America	mountain
Bocas del Toro	Panama	North America	island
San Blas Islands	Panama	North America	island
El Valle de Antón	Panama	North America	mountain
Panama City Casco Viejo	Panama	North America	cultural
Isla Holbox	Mexico	North America	island
Bacalar	Mexico	North America	lake
San Miguel de Allende	Mexico	North America	city
Guanajuato	Mexico	North America	city
Puebla	Mexico	North America	city
Mérida Mexico	Mexico	North America	city
Valladolid Mexico	Mexico	North America	city
Sayulita	Mexico	North America	coast
Mazatlán	Mexico	North America	coast
La Paz Mexico	Mexico	North America	coast
Todos Santos	Mexico	North America	coast
Copper Canyon	Mexico	North America	mountain
Chiapas Highlands	Mexico	North America	mountain
Tulum Coast	Mexico	North America	coast
Ensenada	Mexico	North America	coast
Loreto	Mexico	North America	coast
Havana Vieja	Cuba	North America	cultural
Trinidad Cuba	Cuba	North America	city
Viñales	Cuba	North America	mountain
Cienfuegos	Cuba	North America	city
Varadero	Cuba	North America	coast
New Orleans French Quarter	United States	North America	cultural
Charleston	United States	North America	city
Savannah	United States	North America	city
Asheville	United States	North America	city
Sedona	United States	North America	mountain
Santa Fe	United States	North America	city
Maui Road to Hana	United States	North America	roadtrip
Big Island Hawaii	United States	North America	island
Kauai	United States	North America	island
Maui	United States	North America	island
Big Sur	United States	North America	coast
Monterey	United States	North America	city
Napa Valley	United States	North America	roadtrip
Seattle	United States	North America	city
Portland Oregon	United States	North America	city
San Diego	United States	North America	city
Palm Springs	United States	North America	city
Moab	United States	North America	mountain
Zion National Park	United States	North America	park
Bryce Canyon	United States	North America	park
Grand Canyon	United States	North America	park
Jackson Hole	United States	North America	mountain
Glacier National Park	United States	North America	park
Olympic National Park	United States	North America	park
Acadia	United States	North America	park
Cape Cod	United States	North America	coast
Aspen	United States	North America	mountain
Telluride	United States	North America	mountain
Austin Hill Country	United States	North America	roadtrip
Newport Rhode Island	United States	North America	coast
Vancouver Island	Canada	North America	island
Whistler	Canada	North America	mountain
Tofino	Canada	North America	coast
Quebec City	Canada	North America	city
Montreal	Canada	North America	city
Nova Scotia South Shore	Canada	North America	coast
Prince Edward Island	Canada	North America	island
Churchill	Canada	North America	city
Jasper	Canada	North America	mountain
Haida Gwaii	Canada	North America	island
Okanagan Valley	Canada	North America	roadtrip
St. John's	Canada	North America	city
Auckland	New Zealand	Oceania	city
Wellington	New Zealand	Oceania	city
Wanaka	New Zealand	Oceania	mountain
Marlborough Sounds	New Zealand	Oceania	coast
Abel Tasman	New Zealand	Oceania	park
Milford Sound	New Zealand	Oceania	coast
Rotorua	New Zealand	Oceania	city
Coromandel	New Zealand	Oceania	coast
Kaikōura	New Zealand	Oceania	coast
Bay of Islands	New Zealand	Oceania	coast
Tasmania East Coast	Australia	Oceania	coast
Melbourne	Australia	Oceania	city
Brisbane	Australia	Oceania	city
Perth	Australia	Oceania	city
Adelaide	Australia	Oceania	city
Margaret River	Australia	Oceania	roadtrip
Great Ocean Road	Australia	Oceania	roadtrip
Blue Mountains Australia	Australia	Oceania	mountain
Byron Bay	Australia	Oceania	coast
Noosa	Australia	Oceania	coast
Whitsundays	Australia	Oceania	island
Kangaroo Island	Australia	Oceania	island
Broome	Australia	Oceania	coast
Fremantle	Australia	Oceania	city
Hobart	Australia	Oceania	city
Darwin	Australia	Oceania	city
Cairns	Australia	Oceania	city
Great Barrier Reef	Australia	Oceania	park
Fiji Coral Coast	Fiji	Oceania	coast
Yasawa Islands	Fiji	Oceania	island
Mamanuca Islands	Fiji	Oceania	island
Vanua Levu	Fiji	Oceania	island
Samoa Upolu	Samoa	Oceania	island
Savai'i	Samoa	Oceania	island
American Samoa	American Samoa	Oceania	island
Rarotonga	Cook Islands	Oceania	island
Aitutaki Lagoon	Cook Islands	Oceania	island
Tahiti	French Polynesia	Oceania	island
Moorea	French Polynesia	Oceania	island
Rangiroa	French Polynesia	Oceania	island
Tikehau	French Polynesia	Oceania	island
Huahine	French Polynesia	Oceania	island
Lifou	New Caledonia	Oceania	island
Nouméa	New Caledonia	Oceania	city
Vanuatu Efate	Vanuatu	Oceania	island
Espiritu Santo	Vanuatu	Oceania	island
Tanna	Vanuatu	Oceania	island
Apia	Samoa	Oceania	city
Port Vila	Vanuatu	Oceania	city
Palau Rock Islands	Palau	Oceania	island
Koror	Palau	Oceania	city
Yap	Micronesia	Oceania	island
Pohnpei	Micronesia	Oceania	island
Kosrae	Micronesia	Oceania	island
Chuuk Lagoon	Micronesia	Oceania	island
Majuro	Marshall Islands	Oceania	island
Funafuti	Tuvalu	Oceania	island
Niue	Niue	Oceania	island
Norfolk Island	Norfolk Island	Oceania	island
Lord Howe Island	Australia	Oceania	island
''' 

VIBE_MAP = {
    'island': ['Beach', 'Relaxation', 'Nature'],
    'coast': ['Beach', 'Relaxation', 'Food'],
    'city': ['City', 'Cultural', 'Food'],
    'mountain': ['Nature', 'Adventure', 'Hiking'],
    'park': ['Nature', 'Adventure', 'Wildlife'],
    'cultural': ['Cultural', 'Romantic', 'History'],
    'lake': ['Nature', 'Relaxation', 'Romantic'],
    'desert': ['Adventure', 'Nature', 'Unfrequented'],
    'roadtrip': ['Nature', 'Adventure', 'Relaxation'],
}

TRAVEL_MAP = {
    'island': ['beach', 'couples', 'island-hopping'],
    'coast': ['beach', 'food', 'couples'],
    'city': ['solo', 'food', 'weekend'],
    'mountain': ['adventure', 'hiking', 'photography'],
    'park': ['adventure', 'wildlife', 'road-trip'],
    'cultural': ['history', 'couples', 'solo'],
    'lake': ['couples', 'photography', 'relaxation'],
    'desert': ['adventure', 'photography', 'offbeat'],
    'roadtrip': ['road-trip', 'photography', 'adventure'],
}

SEASON_MAP = {
    'Europe': 'Apr–Oct',
    'Asia': 'Oct–May',
    'Africa': 'Nov–Apr',
    'North America': 'Nov–Apr',
    'South America': 'Sep–May',
    'Oceania': 'May–Oct',
}

BUDGET_MAP = {
    'Europe': '$$$',
    'Asia': '$$',
    'Africa': '$$',
    'North America': '$$$',
    'South America': '$$',
    'Oceania': '$$$',
}

PITCH_TEMPLATES = {
    'island': '{name} is a high-payoff island escape for beach days, slower pacing, and the sort of water that tends to sell the trip by itself.',
    'coast': '{name} works as an easy coast-first trip with sea views, seafood upside, and enough atmosphere to justify staying longer than planned.',
    'city': '{name} is a strong city break for travelers who want food, walkable neighborhoods, and enough cultural weight to keep the trip from feeling generic.',
    'mountain': '{name} is a mountain-heavy destination built for big views, active days, and the kind of scenery that usually justifies the transit effort.',
    'park': '{name} is a national-park style payoff destination with strong nature access, memorable landscapes, and clear trip-building value.',
    'cultural': '{name} earns its keep with deep history, strong sense of place, and the kind of cultural density that anchors an itinerary easily.',
    'lake': '{name} is a calmer lake-and-landscape destination that suits couples, scenic downtime, and slower travel days.',
    'desert': '{name} offers stark landscapes, offbeat energy, and a much stronger visual payoff than its infrastructure usually suggests.',
    'roadtrip': '{name} is best approached as a route rather than a stop, with scenic variety and strong road-trip logic built into the destination itself.',
}


def parse_rows():
    rows = []
    for line in TSV.strip().splitlines():
        name, region, continent, kind = [part.strip() for part in line.split('\t')]
        rows.append((name, region, continent, kind))
    return rows


def main():
    data = json.loads(SOURCE.read_text())
    by_name = {row.get('name') for row in data if isinstance(row, dict)}
    added = 0
    limit = 500
    for name, region, continent, kind in parse_rows():
        if added >= limit:
            break
        if name in by_name:
            continue
        row = {
            'name': name,
            'region': region,
            'continent': continent,
            'photo': FALLBACK_PHOTO,
            'pitch': PITCH_TEMPLATES[kind].format(name=name),
            'budget': BUDGET_MAP.get(continent, '$$'),
            'season': SEASON_MAP.get(continent, 'Year-round'),
            'vibes': VIBE_MAP[kind],
            'travel': TRAVEL_MAP[kind],
        }
        data.append(row)
        by_name.add(name)
        added += 1
    data.sort(key=lambda r: r.get('name', '').casefold())
    SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(f'added={added} total={len(data)}')

if __name__ == '__main__':
    main()
