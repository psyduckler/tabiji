#!/usr/bin/env python3
"""Costa Rica book-readiness pass (2026-04-28):

1. Shorten ~30 worst scam-titles toward NYC's 3-7-word concrete-narrative form
2. Prune scam-location bloat (NYC <10 words; CR has many 25-45 word lists)
3. Sync api/v1/scams/<city>.json `name` field to the new HTML title

Strategy: explicit per-scam (city, scam_id, old_title, new_title,
old_loc, new_loc) tuples. Each old string is unique enough that a literal
str.replace catches every occurrence (scam-title div, TOC, comic alt text,
meta description, og:description, twitter:description, takeaways line,
JSON-LD Article description). For api/v1, update the matching scam by id.

Locations are simpler — only one canonical place: <div class="scam-location">.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


# (city, scam_id, old_title_or_None, new_title_or_None, old_loc_or_None, new_loc_or_None)
# `_or_None` means: leave it alone. Locations have the trailing 📍 stripped here;
# the script preserves the existing 📍 emoji prefix on the page.
CHANGES: list[tuple[str, int, str | None, str | None, str | None, str | None]] = [
    # ---- jaco-costa-rica ----
    ("jaco-costa-rica", 1,
     "Jacó Nightlife Drink-Spiking & 'Costa Rican Friend' Robbery Setup",
     "Jacó Nightlife Drink-Spike Robbery",
     "Avenida Pastor Díaz nightlife strip (Jacó main drag), Beatle Bar, Le Loft, Orange Pub, Tabacón-area clubs, Hotel Cocal & Casino pool bar, late-night beach approach west of Avenida Pastor Díaz",
     "Avenida Pastor Díaz nightlife strip; Hotel Cocal & Casino pool bar"),
    ("jaco-costa-rica", 2,
     "'Costa Joe' — Named WhatsApp/Facebook Fixer Deposit Fraud (Cars, Golf Carts, Airbnbs)",
     "'Costa Joe' WhatsApp Deposit Fraud",
     "Facebook groups targeting Jacó (What's On Jaco, Costa Rica Travel, Playas del Coco), WhatsApp private chats after FB introductions, claimed 'rental lots' in Jacó beach zone and Herradura",
     "Facebook groups targeting Jacó (What's On Jaco, Costa Rica Travel); WhatsApp deposits to claimed Jacó rentals"),
    ("jaco-costa-rica", 3,
     "Jacó Beach Parking Fake 'No-Park Zone' Reflective-Vest Extortion",
     "Jacó Beach Reflective-Vest Parking Extortion",
     "Parking strips along Avenida Pastor Díaz near Playa Jacó main beach access, side streets by Jaco Walk plaza, beach-front lots south of Hotel Cocal, parking near Playa Hermosa surf break",
     "Avenida Pastor Díaz parking strips; Jaco Walk plaza side streets; Hotel Cocal beach-front lots"),
    ("jaco-costa-rica", 4,
     None, None,
     "Search-engine-optimized copycat tour-booking websites (monteverdetourscr.com and similar domains targeting Jacó-area day-tours — Carara crocodile, Manuel Antonio, Catarata Bijagual, zipline combos), booked while planning from Jacó hotels",
     "Copycat domains like monteverdetourscr.com; booked from Jacó hotel WiFi"),
    ("jaco-costa-rica", 6,
     "Jacó ATV & Golf Cart Rental Damage-Inflation Deposit Trap",
     "Jacó ATV / Golf Cart Damage-Deposit Trap",
     None, None),
    ("jaco-costa-rica", 7,
     "Jacó Mirador & Beach Opportunistic Robbery / Belongings Theft",
     "Jacó Mirador Lookout Robbery",
     "Mirador Jacó lookout and approach trail (abandoned villa above south end of Jacó beach), Playa Jacó main beach sand, Playa Hermosa surf-break parking, beach approaches after sunset",
     "Mirador Jacó lookout trail (abandoned villa above south Jacó); Playa Jacó sand after sunset"),

    # ---- la-fortuna ----
    ("la-fortuna", 1,
     "Lava Land Tours 'Sloth Tour' Bait-and-Switch — Julio's Downtown Storefront",
     "Lava Land Tours 'Sloth Tour' Bait-and-Switch",
     "Storefront on Avenida Central (Calle 2) in central La Fortuna, specifically 'between Jungle Bowls and The Blue Spa' — a block south of Parque La Fortuna (the central park with the volcano view)",
     "Avenida Central storefront in central La Fortuna, between Jungle Bowls and The Blue Spa"),
    ("la-fortuna", 2,
     "La Fortuna Red Taxi Meter 'María' Tampering & Inflated Excursion-Meetup Fares",
     "La Fortuna Red-Taxi Meter Tampering",
     "Red taxis flagged outside La Fortuna hotels (Arenal Observatory Lodge, Hotel Magic Mountain, Volcano Lodge), the Calle Central red-taxi stand at Parque La Fortuna, and Sunday-morning runs to Rio Celeste / Mistico / Arenal trailheads",
     "Calle Central red-taxi stand at Parque La Fortuna; runs to Río Celeste / Mistico / Arenal trailheads"),
    ("la-fortuna", 3,
     "Roadside 'Private Hot Springs' Booth Scam — Fake Day-Pass Collectors Near Rio Chollín",
     "Río Chollín Fake Hot-Springs Day-Pass",
     "Route 142 (the main La Fortuna → Nuevo Arenal road) between the Tabacón bridge and the EcoTermales turnoff, specifically the Rio Chollín (sometimes spelled Choyín / El Chollín) pullout and the short access trail down to the free hot spring river",
     "Route 142 between the Tabacón bridge and the EcoTermales turnoff; Río Chollín pullout to the free hot-spring river"),
    ("la-fortuna", 4,
     "La Fortuna Waterfall 'Unofficial Parking Permit' Collectors at ADIFORT Gate",
     "La Fortuna Waterfall Fake-Permit Collectors",
     "Access road to La Fortuna Waterfall (Cataratas La Fortuna), specifically the 1 km dirt-road stretch between the intersection at Calle Real La Fortuna and the official ADIFORT gate/parking lot; also the paved waterfall-viewpoint turnoff 2 km earlier",
     "Access road to La Fortuna Waterfall; 1 km dirt approach to the official ADIFORT gate"),
    ("la-fortuna", 5,
     "Jeep-Boat-Jeep Monteverde Shuttle — Double-Booking & Luggage-Weight 'Overage' Fees",
     "Jeep-Boat-Jeep Monteverde Shuttle Overage Fees",
     "La Fortuna hotel pickups (6 AM–8 AM departures), Arenal Lake boat dock at Rio Piedras Blancas (Boat segment), Río Chiquito / Monteverde dock on the Pacific side, downtown La Fortuna tour-office sellers on Avenida Central",
     "La Fortuna hotel pickups (6–8 AM); Arenal Lake boat dock at Río Piedras Blancas"),
    ("la-fortuna", 6,
     "Arenal Backpackers / Societal La Fortuna — Hostel Listing-vs-Reality & Third-Party Booking Freeze-Out",
     "Arenal Backpackers Hostel Listing-vs-Reality Bait",
     "Arenal Backpackers Resort and multiple budget hostels on Avenida Arenal / Calle 11 in La Fortuna town center; also third-party-booked properties via Expedia / Booking.com / Hostelworld in the La Fortuna area",
     "Avenida Arenal / Calle 11 hostels in La Fortuna; Expedia / Booking.com third-party listings"),
    ("la-fortuna", 7,
     "La Fortuna Vrbo / Vacation-Rental Inside Job — Last-Night Power-Cut Electronics Theft",
     "La Fortuna Vrbo Last-Night Power-Cut Theft",
     "Short-term rentals in the La Fortuna–El Castillo–Chachagua corridor (particularly remote villa rentals with volcano views), properties advertised on Vrbo with 'Premier Host' status, isolated roads 5–15 km from central La Fortuna",
     "Vrbo villa rentals in the La Fortuna–El Castillo–Chachagua corridor; isolated roads 5–15 km from town"),

    # ---- liberia-costa-rica ----
    ("liberia-costa-rica", 1,
     "Avis LIR 'Mandatory Insurance' Bait-and-Switch — $123 Online Becomes $444 at the Counter",
     "Avis LIR 'Mandatory Insurance' Bait-and-Switch",
     "Avis rental counter inside and just outside the Daniel Oduber Quirós International Airport (LIR) in Liberia, Guanacaste, plus the Avis franchise office on the Liberia airport access road serving pickups diverted from the terminal",
     "Avis counter inside LIR (Daniel Oduber Quirós Airport); Avis off-airport franchise on the access road"),
    ("liberia-costa-rica", 2,
     "Budget / Hertz / Fox / Europcar LIR Counter Phantom-Fee Stack — $800 Rental Becomes $1,800",
     "Hertz LIR Counter Phantom-Fee Stack",
     "Budget, Hertz, Fox Rent a Car, Europcar counters inside the LIR terminal plus their off-airport franchise offices 2–4 km away on the airport access road; third-party broker websites like Economybookings.com and GEC Group / NextCar EK Chele S.A.",
     "Hertz, Budget, Fox, Europcar counters at LIR plus their off-airport franchise offices 2–4 km away"),
    ("liberia-costa-rica", 3,
     "Pinchonazo / Flat-Tire Robbery on Route 21 and the Liberia Gas-Station Circuit",
     "Pinchonazo Flat-Tire Robbery on Route 21",
     "Route 21 between Liberia city and the Guanacaste beach towns (Playas del Coco, Playa Hermosa, Playa Flamingo, Tamarindo), Delta and Recope gas stations on the Liberia belt-road, and the first 20 km stretch south of LIR on Route 1 / Pan-American",
     "Route 21 between Liberia and the Guanacaste beach towns; Delta and Recope gas stations on the LIR belt road"),
    ("liberia-costa-rica", 4,
     "Unofficial Airport Porter / Luggage Grab at LIR Arrivals — $20 Tip Demanded at the Curb",
     "Unofficial Airport Porter Luggage Grab at LIR",
     "LIR (Daniel Oduber Quirós International Airport) arrivals hall immediately past the customs exit and the outdoor curb under the taxi / shuttle canopy, plus the Avis / Budget / Hertz shuttle waiting area where luggage is handed off between vehicles",
     "LIR arrivals hall past customs; outdoor curb under the taxi/shuttle canopy"),
    ("liberia-costa-rica", 5,
     "LIR Airport Taxi 'Broken Meter / Flat Rate' Overcharge — $80 for a $45 Playas del Coco Run",
     "LIR Airport Taxi 'Broken Meter' Overcharge",
     "Official and unofficial taxi ranks at LIR (Daniel Oduber Quirós International Airport) curbside, plus the taxi rank at the Liberia city central park (Parque Central / Parque Mario Cañas) serving hotel-bound tourists",
     "LIR curbside taxi ranks; Liberia Parque Central taxi rank serving hotel-bound tourists"),
    ("liberia-costa-rica", 6,
     "Gas Station 'Pump Not Zeroed' + Short-Change Colón-Dollar Swap — Delta / Recope Stations",
     "'Pump Not Zeroed' Short-Change at Delta Stations",
     "Delta, Recope, and Uno gas stations on Route 21 between LIR and Playas del Coco, the Delta on the Liberia airport belt road, and rural Guanacaste stations on the Pan-American Highway where Costa Rica still mandates attendant pump service",
     "Delta, Recope, Uno gas stations on Route 21 between LIR and Playas del Coco; rural Pan-American stations"),
    ("liberia-costa-rica", 7,
     "Global Exchange LIR Currency-Rate Skim + BAC/Scotiabank ATM Shoulder-Surf Skimming",
     "Global Exchange LIR Skim & ATM Shoulder-Surf",
     "Global Exchange currency kiosks inside LIR arrivals and departures halls, BAC San José / BAC Credomatic and Scotiabank ATMs on Avenida Central in Liberia city, and the ATM cluster inside the Pueblo Antiguo Mall / Pricesmart Liberia parking area",
     "Global Exchange kiosks inside LIR arrivals/departures; BAC and Scotiabank ATMs on Avenida Central in Liberia"),

    # ---- manuel-antonio ----
    ("manuel-antonio", 1,
     "Fake 'Park Ranger' Road Blockers on Route 618 — 'Park Full / Park Closed' Parking Extortion",
     "Fake 'Park Ranger' Parking Extortion on Route 618",
     "Route 618 approach to Manuel Antonio National Park, roughly 500 m–1 km before the actual SINAC gate, between the Manuel Antonio '1 km' sign and the circular turnaround at the park entrance, also along Playa Espadilla Norte frontage road",
     "Route 618 approach to Manuel Antonio National Park, 500 m–1 km before the SINAC gate"),
    ("manuel-antonio", 2,
     "Fake 'SINAC Ticket Booth' Paper Ticket Resellers at the Park Entrance",
     "Fake 'SINAC Ticket Booth' Paper Resellers",
     "Final 200 m of Route 618 before the official SINAC turnstile, near the circular turnaround in Manuel Antonio village, and outside Playa Espadilla Norte restaurants that advertise 'park tickets here'",
     "Final 200 m of Route 618 before the SINAC turnstile; Playa Espadilla Norte restaurants"),
    ("manuel-antonio", 3,
     "Unofficial 'ICT-Certified' Guides at the Park Gate — $60 Shortest-Route Rip-Off",
     "Fake 'ICT-Certified' Guides at the Park Gate",
     "Immediately outside the SINAC turnstile at the Manuel Antonio National Park entrance, ticket-queue area, and along the first 300 m of the Sendero Principal trail just inside the park",
     "Outside the SINAC turnstile at Manuel Antonio National Park; ticket-queue area"),
    ("manuel-antonio", 4,
     "Playa Espadilla Beach 'Parking + Umbrella' Cash-Only Intimidation at David's Crew",
     "Playa Espadilla 'Parking + Umbrella' Cash-Only Shakedown",
     "Playa Espadilla (main public beach directly in front of Manuel Antonio village), particularly the section closest to the park entrance; informal parking lots north of the river separating Espadilla from Manuel Antonio beach",
     "Playa Espadilla (the public beach in front of Manuel Antonio village); section closest to the park entrance"),
    ("manuel-antonio", 5,
     None, None,
     "Tracopa bus route San José (Terminal Plaza Víquez) → Jacó → Quepos → Manuel Antonio; specifically the mid-route restroom stop north of Jacó where most passengers disembark briefly and leave valuables on board",
     "Tracopa bus route San José → Jacó → Quepos → Manuel Antonio; mid-route restroom stop north of Jacó"),
    ("manuel-antonio", 6,
     "White-Faced Capuchin & Raccoon Beach-Theft Distraction — Monkey-Feeding Bag Grab",
     "Capuchin & Raccoon Beach-Theft Distraction",
     "Playa Manuel Antonio (the crescent-shaped main beach inside the park), Playa Espadilla Sur, the tree line at the back of both beaches (especially near manzanillo trees), and Cathedral Point trail picnic areas",
     "Playa Manuel Antonio inside the park; Playa Espadilla Sur tree line; Cathedral Point picnic areas"),
    ("manuel-antonio", 7,
     "Manuel Antonio Strip Restaurant 'Gringo Menu' & Hidden Service-Charge Upcharge",
     "Manuel Antonio 'Gringo Menu' Service-Charge Upcharge",
     "Main tourist strip of Manuel Antonio village from the park turnaround back toward Quepos — along Route 618 roughly 1 km south of the park, especially restaurants with English-only menus and ocean-view decks",
     "Manuel Antonio village strip on Route 618, ~1 km south of the park entrance"),

    # ---- monteverde ----
    ("monteverde", 1,
     "Fake/Unlicensed 'Certified Guide' Ambush at Monteverde Cloud Forest Reserve Gate",
     "Fake 'Certified Guide' Ambush at the Reserve Gate",
     "Road approach to Reserva Biológica Bosque Nuboso Monteverde (Route 606 past Cerro Plano, final 2 km), Santa Elena Cloud Forest Reserve (Reserva Bosque Nuboso Santa Elena) approach road, parking lot of the Monteverde Reserve visitor center",
     "Approach road to Reserva Bosque Nuboso Monteverde (Route 606 past Cerro Plano); Santa Elena Reserve approach"),
    ("monteverde", 2,
     "Monteverde Shuttle Bus & Bookaway Private-Transfer Wrong-Pickup / Kidnapping Scare",
     "Bookaway Shuttle Wrong-Pickup Kidnapping Scare",
     None, None),
    ("monteverde", 3,
     "Monteverde 'Hostel Desk' Commission Overcharge on Tour Bookings (Night Walks, Zipline, Coffee Tours)",
     "Monteverde 'Hostel Desk' Tour-Booking Commission Overcharge",
     "Hostel and budget-hotel front desks across Santa Elena village (Pensión Santa Elena, Sabine's Smiling Horses Hostel area, Camino Verde, Cabinas Vista Al Golfo), tour-booking kiosks on the main Santa Elena strip",
     "Hostel and budget-hotel front desks across Santa Elena village; tour-booking kiosks on the main strip"),
    ("monteverde", 4,
     "Monteverde Jeep-Boat-Jeep Double-Booking & Wrong-Hotel Pickup (Monteverde End)",
     "Monteverde Jeep-Boat-Jeep Wrong-Hotel Pickup",
     "Santa Elena village jeep pickup points (multiple hostels + central plaza), Monteverde-side dock on Lake Arenal (Río Chiquito ramp), transfer to La Fortuna side (Puerto San Luis / Arenal Lake dock)",
     "Santa Elena village pickup points; Monteverde-side dock on Lake Arenal (Río Chiquito ramp)"),
    ("monteverde", 5,
     "Monteverde Tours CR Copycat & 'Roy's Nature Guide' Advance-Fee Tour Fraud",
     "Monteverde Tours CR Copycat-Domain Fraud",
     None, None),

    # ---- puerto-viejo-costa-rica ----
    ("puerto-viejo-costa-rica", 1,
     "Masked Machete Robberies on the Volio / Bribri Waterfall Trails — Kekoldi Buffer to Gandoca-Manzanillo",
     "Masked Machete Robberies on Volio & Bribri Trails",
     "Volio Falls trail inland from Puerto Viejo in Bribri / Kekoldi Indigenous territory, unsigned footpaths off Route 36 between Hone Creek and Bribri, plus Gandoca-Manzanillo Wildlife Refuge back trails",
     "Volio Falls trail in Bribri / Kekoldi territory inland from Puerto Viejo; unsigned paths off Route 36"),
    ("puerto-viejo-costa-rica", 2,
     "Key-Fob Jammer Car Break-Ins on Playa Cocles, Playa Chiquita, and Route 256 Beach Pullouts",
     "Key-Fob Jammer Car Break-Ins on Route 256",
     "Dirt pullouts along Route 256 between Puerto Viejo and Manzanillo — Playa Cocles surf parking, Playa Chiquita access points, Punta Uva public lot — plus the MEPE terminal lot on Calle 217",
     "Route 256 dirt pullouts between Puerto Viejo and Manzanillo — Playa Cocles, Playa Chiquita, Punta Uva"),
    ("puerto-viejo-costa-rica", 3,
     "'You Want Weed?' Drug-Dealer Stalking and Robbery-After-Deal Setup on Calle 217 and the Beach Path",
     "'You Want Weed?' Robbery-After-Deal on Calle 217",
     "Puerto Viejo main drag (Calle 217) between Hot Rocks and Lazy Mon, the dirt beach path along Playa Negra behind the bar strip, and the jungle footpath leading from Calle 215 to unlit hostels — especially after 9 PM",
     "Calle 217 between Hot Rocks and Lazy Mon; Playa Negra dirt path behind the bar strip after 9 PM"),
    ("puerto-viejo-costa-rica", 4,
     "Beach Belongings Snatch during Swim / Snorkel — Playa Cocles, Playa Chiquita, Punta Uva",
     "Beach Belongings Snatch on Playa Cocles & Punta Uva",
     "Playa Cocles 1 km south of Puerto Viejo town (particularly the tree-lined section opposite La Costa de Papito), Playa Chiquita between Playa Chiquita Lodge and Shawandha, and the coral reef snorkel beaches at Punta Uva and Manzanillo",
     "Playa Cocles south of Puerto Viejo town; Playa Chiquita and Punta Uva snorkel beaches"),
    ("puerto-viejo-costa-rica", 5,
     None, None,
     "Unlicensed rental shacks lining Calle 217 and Calle 213 in Puerto Viejo town, especially the ones east of the bus terminal with hand-painted signs and no printed contract; also Playa Cocles bike-rental stands near the Jaguar Rescue Center",
     "Unlicensed rental shacks on Calle 217 and Calle 213 in Puerto Viejo town; Playa Cocles bike stands near the Jaguar Rescue Center"),
    ("puerto-viejo-costa-rica", 6,
     "MEPE vs Fake Shuttle Fare Gouging — San José Atlántico Norte Terminal to Puerto Viejo",
     "Fake MEPE Shuttle Fare Gouging from San José",
     "Terminal Atlántico Norte (also called Terminal del Caribe or 'Gran Terminal del Caribe') in San José for the MEPE departure, the Puerto Viejo MEPE drop-off on Calle 217, and hostels/travel agencies on Calle 217 selling unlicensed 'shuttle' tickets",
     "Terminal Atlántico Norte (Gran Terminal del Caribe) in San José; Puerto Viejo MEPE drop-off on Calle 217"),
    ("puerto-viejo-costa-rica", 7,
     "Airbnb / Villa Inside-Job Burglary during Advertised 'Power Outage' — Playa Cocles and Punta Uva Rentals",
     "Airbnb 'Power Outage' Inside-Job Burglary",
     "Beachfront Airbnb rentals and villas along Playa Cocles and Punta Uva, particularly units with a single caretaker who holds a key and has advance notice of guest movements; also remote 'jungle cabinas' off Route 256 south of Puerto Viejo",
     "Beachfront Airbnbs along Playa Cocles and Punta Uva; remote 'jungle cabinas' off Route 256 south of Puerto Viejo"),

    # ---- quepos (titles already short, just prune locations) ----
    ("quepos", 2, None, None,
     "Calle 2 waterfront strip, Mercado Central perimeter, the marina-side restaurant row at Marina Pez Vela, Avenida Central seafood spots in Quepos Centro, the corridor between the Tracopa terminal and the futbol field",
     "Calle 2 waterfront strip; Marina Pez Vela restaurant row; Quepos Centro seafood spots"),
    ("quepos", 3, None, None,
     "La Managua airstrip (XQP) terminal exit, Sansa and Skyway arrivals curb, the road shoulder leading to Avenida Central in Quepos, hotel transfer pickup zone, the unmarked-vehicle queue across from the airstrip gate",
     "La Managua airstrip (XQP) terminal exit; Sansa and Skyway arrivals curb"),
    ("quepos", 4, None, None,
     "Marina Pez Vela jet-ski rental kiosks, Avenida Central ATV operators in Quepos Centro, the catamaran-tour booking row on the marina boardwalk, beach-launch jet-ski stands on the Quepos waterfront, hotel-lobby tour desks pushing rental coupons",
     "Marina Pez Vela jet-ski rental kiosks; ATV operators on Avenida Central in Quepos Centro"),
    ("quepos", 5, None, None,
     "Tracopa Quepos terminal boarding platform, the coffee-stand and snack-counter line, the queue for Route 27 buses to San José, the seat-pocket and overhead-bin area during the first ten minutes of boarding, the sidewalk between the terminal and the futbol field",
     "Tracopa Quepos terminal boarding platform; Route 27 bus queue to San José"),

    # ---- san-jose-costa-rica ----
    ("san-jose-costa-rica", 1,
     "SJO Airport Pirate-Taxi Cartel — $40 for a 4-Minute Ride & Worse",
     "SJO Airport Pirate-Taxi Cartel",
     "Juan Santamaría International Airport (SJO / Alajuela) arrivals curb — exit lanes 1–8 immediately outside baggage claim; the informal 'bus station' pickup zone where pirate taxis cluster; late-night exits where the official orange-taxi kiosk is less staffed",
     "Juan Santamaría International Airport (SJO) arrivals curb — exit lanes 1–8; the informal 'bus station' pickup zone"),
    ("san-jose-costa-rica", 2,
     "Fake Uber at SJO + Driver-Doesn't-End-Trip Fare Gouge",
     "Fake Uber at SJO Fare-Gouge",
     "SJO arrivals curb, the departures-level Uber pickup stairs (the workaround to the airport-police ban), the Selina/Adventure Hostel pickup zone along Avenida 7 in San José Centro, and stops near Parque Morazán where Uber drivers canceling is common",
     "SJO arrivals curb; departures-level Uber pickup stairs; Selina / Adventure Hostel pickup zone on Avenida 7"),
    ("san-jose-costa-rica", 3,
     "Claro / Kolbi SIM-Card 'Activation Fee' Fraud at SJO Baggage Claim",
     "SJO Baggage-Claim SIM-Card 'Activation Fee' Fraud",
     "Kiosk at SJO baggage-claim hall 1 (between the two carousels), the arrivals-area Claro counter opposite the currency-exchange booth, and the secondary Kolbi kiosk at departures pre-security",
     "Kiosk at SJO baggage-claim hall 1 (between the carousels); arrivals-area Claro counter opposite currency exchange"),
    ("san-jose-costa-rica", 4,
     "SJO Rental-Car Counter 'Mandatory Insurance' $2,000 Ambush — Expedia / Hertz / Fox Trap",
     "SJO Rental-Car 'Mandatory Insurance' $2K Ambush",
     "SJO airport rental-car shuttle zone (arrivals → van shuttle to off-airport lots); Adobe, Vamos, Economy, Alamo, Hertz, Fox, Budget, Enterprise, National, Sixt counters clustered on the service road along Route 1 just west of the terminal",
     "SJO rental-car shuttle zone (arrivals → off-airport lots); Hertz, Fox, Budget, Enterprise counters on the service road"),
    ("san-jose-costa-rica", 5,
     "San José Airbnb / Rental Home-Invasion — The Calendar-Leak Pattern",
     "San José Airbnb 'Calendar-Leak' Home-Invasion",
     "Airbnbs and VRBOs across Escazú, Santa Ana, Barrio Escalante, Sabana Oeste, San Pedro, Curridabat, and the Central Valley outskirts — any property where the booking calendar publicly shows arrival dates, and isolated homes outside guarded communities",
     "Airbnbs across Escazú, Santa Ana, Barrio Escalante, San Pedro, Curridabat — properties with public booking calendars"),
    ("san-jose-costa-rica", 6,
     "Coca-Cola Bus Terminal Pickpocket & Luggage-Theft at the Zona Roja Edge",
     "Coca-Cola Bus Terminal Pickpocket & Luggage Theft",
     "Terminal 7-10 (Coca-Cola) and adjacent bus bays along Calle 14 / Avenida 1–5 in San José Centro; the Mercado Central five blocks south; the 'zona roja' (red-light) blocks immediately north of the terminal near Hotel Del Rey; nearby Tracopa, Alfaro, and MEPE bus bays",
     "Terminal 7-10 (Coca-Cola) and bus bays along Calle 14 / Avenida 1–5 in San José Centro; the 'zona roja' blocks north of the terminal"),
    ("san-jose-costa-rica", 7,
     "Parque Central / Avenida 2 Cambista Currency-Exchange & 'Counterfeit Bill' Swap",
     "Parque Central Cambista 'Counterfeit Bill' Swap",
     "Parque Central San José (Avenida 2, Calle Central), Plaza de la Cultura edges, Avenida Central pedestrian strip between Calle 2 and Calle 9, the Correos de Costa Rica building cluster on Calle 2, and the casa de cambio clusters near Hotel Del Rey",
     "Parque Central (Avenida 2, Calle Central); Plaza de la Cultura edges; casa de cambio cluster near Hotel Del Rey"),

    # ---- santa-teresa: titles + locations already concise; no changes ----

    # ---- tamarindo ----
    ("tamarindo", 1,
     "'Guachimán' Yellow-Vest Watchmen Parking Extortion on the Tamarindo Strip",
     "'Guachimán' Yellow-Vest Parking Extortion",
     "Main street of Tamarindo village (Calle Central / the road running parallel to Playa Tamarindo), the dirt lots behind Volcano Brewing / Witch's Rock Surf Camp, Playa Langosta access roads, and the gravel pullouts on the approach from Villarreal (Route 152)",
     "Calle Central Tamarindo (the road parallel to Playa Tamarindo); dirt lots behind Volcano Brewing / Witch's Rock Surf Camp"),
    ("tamarindo", 2,
     "Beach-Hustler 'Surf Instructor' Lesson & $200 Board-Damage Ambush",
     "Beach 'Surf Instructor' $200 Board-Damage Ambush",
     "Playa Tamarindo main beach in front of the Diria, Volcano Brewing, and the Tamarindo river-mouth sandbar where beginners are taken; informal beach-front board-rental tents set up between Plaza Tamarindo and the estuary; Langosta rocks section for 'advanced' lessons",
     "Playa Tamarindo in front of the Diria and Volcano Brewing; Tamarindo river-mouth sandbar where beginners are taken"),
    ("tamarindo", 3,
     "Rental-Home & Airbnb Home Invasion — The Los Jobos Tamarindo Pattern",
     "Los Jobos Airbnb Home-Invasion Pattern",
     "Rental villas and Airbnbs in Los Jobos (north Tamarindo), Playa Langosta gated sections, Playa Grande beachfront homes, Playa Negra south of Tamarindo, and any isolated beach-access Airbnb where the calendar shows arrivals online",
     "Rental villas in Los Jobos (north Tamarindo); Playa Langosta gated sections; Playa Grande beachfront homes"),
    ("tamarindo", 4,
     "Rental-Car Relay-Theft & Main-Strip Smash-and-Grab outside Witch's Rock / Volcano Brewing",
     "Rental-Car Relay-Theft outside Witch's Rock / Volcano Brewing",
     "Main-street parking pullouts in front of Volcano Brewing / Witch's Rock Surf Camp on Calle Central Tamarindo, Banco Nacional / BAC Credomatic ATM lots, the gravel shoulders between Playa Tamarindo and Playa Langosta, and unattended rental-car spots while you surf for 2+ hours at the river-mouth",
     "Main-street parking outside Volcano Brewing / Witch's Rock Surf Camp on Calle Central; Banco Nacional / BAC ATM lots"),
    ("tamarindo", 5,
     "LIR Shuttle / Pirate-Taxi Tamarindo Gouge — $80–$150 for a $55 Ride",
     "LIR Shuttle / Pirate-Taxi Tamarindo Gouge",
     "Liberia Airport (LIR) arrivals curb, Tamarindo main-street taxi stands (Plaza Conchal, in front of Diria), and the informal 'friend with a van' networks touted at hostels and beach bars for SJO/LIR runs",
     "Liberia Airport (LIR) arrivals curb; Tamarindo main-street taxi stands (Plaza Conchal, Diria)"),
    ("tamarindo", 6,
     "Tamarindo Banco Nacional / BAC ATM Skimming + Counterfeit-Bill Swap",
     "Tamarindo Banco Nacional ATM Skimming + Counterfeit Swap",
     "Banco Nacional ATM on the Tamarindo main strip (Plaza Tamarindo), BAC Credomatic ATM at Plaza Conchal, Scotiabank ATM between Diria and the roundabout, and adjacent street-side change booths near the main strip / restaurant cluster",
     "Banco Nacional ATM on the Tamarindo main strip (Plaza Tamarindo); BAC Credomatic ATM at Plaza Conchal"),
    ("tamarindo", 7,
     "Tamarindo Nightlife Drink-Spiking & 'Sexpat' Prostitution-Ring Extortion at the Casino",
     "Tamarindo Nightlife Drink-Spiking & Casino Extortion",
     "Monkey Bar / Crazy Monkey nightclub district, the Tamarindo Diria casino, Sharky's Sports Bar, beach-front DJ bars between Plaza Tamarindo and the river-mouth, and 'date back to Airbnb' routes through the unlit beach path to Langosta",
     "Monkey Bar / Crazy Monkey nightclub district; Tamarindo Diria casino; Sharky's Sports Bar"),

    # ---- tortuguero: titles + locations already concise; no changes ----
]


def update_html(city: str, changes_for_city: list[tuple]) -> int:
    """Apply title + location changes for one city's HTML. Returns # edits made."""
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    edits = 0
    for _city, _n, old_t, new_t, old_l, new_l in changes_for_city:
        if old_t and new_t:
            if old_t in html:
                count_before = html.count(old_t)
                html = html.replace(old_t, new_t)
                edits += count_before
            else:
                print(f"  WARN: title not found in HTML: {city}/scam-{_n}: {old_t[:60]}")
        if old_l and new_l:
            # Locations only appear in <div class="scam-location">📍 LOC</div>.
            # Match the literal location string (no 📍 in our tuples — that's already
            # in the HTML).
            if old_l in html:
                count_before = html.count(old_l)
                html = html.replace(old_l, new_l)
                edits += count_before
            else:
                print(f"  WARN: location not found in HTML: {city}/scam-{_n}: {old_l[:60]}")
    path.write_text(html)
    return edits


def update_json(city: str, changes_for_city: list[tuple]) -> int:
    """Apply title changes to api/v1/scams/<city>.json. Locations are not stored
    in the same shape there; we update the `name` field by index match."""
    path = REPO / f"api/v1/scams/{city}.json"
    data = json.loads(path.read_text())
    scams = data["scams"]
    edits = 0
    for _city, n, old_t, new_t, _ol, _nl in changes_for_city:
        if not (old_t and new_t):
            continue
        # scams may be 0-indexed; n is 1-indexed. Match by `id` field if present.
        target = None
        for i, s in enumerate(scams):
            if s.get("id") == n or i + 1 == n:
                target = s
                break
        if target is None:
            print(f"  WARN: json scam #{n} not found in {city}")
            continue
        if target.get("name") == old_t:
            target["name"] = new_t
            edits += 1
        else:
            # Try matching anyway — title may have already been edited or have
            # subtle whitespace differences. Be strict: only update on exact match.
            print(f"  WARN: json {city}/scam-{n} name mismatch.")
            print(f"        expected: {old_t[:80]}")
            print(f"        actual:   {target.get('name','?')[:80]}")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return edits


def main() -> None:
    by_city: dict[str, list[tuple]] = {}
    for chg in CHANGES:
        by_city.setdefault(chg[0], []).append(chg)

    total_html = total_json = 0
    for city in sorted(by_city):
        changes = by_city[city]
        h = update_html(city, changes)
        j = update_json(city, changes)
        print(f"  {city}: {h} HTML replacements, {j} JSON name updates "
              f"({len(changes)} change tuples)")
        total_html += h
        total_json += j
    print(f"\nTOTAL: {total_html} HTML replacements, {total_json} JSON updates "
          f"across {len(by_city)} cities")


if __name__ == "__main__":
    main()
