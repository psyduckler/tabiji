#!/usr/bin/env python3
"""
Generate the Vietnam book comic assets via Wavespeed (Nano Banana Pro):
 - front cover (single dramatic panel, 2:3 aspect)
 - back cover (single scene with empty upper portion for text overlay, 2:3)
 - 66 per-scam comics (2x2 grid, 1:1) across 11 cities.

Vietnam style — locked for V6: Dong Ho folk-woodblock-print inspired,
warm earth palette (terracotta red, mustard yellow, ochre, deep indigo,
black ink outlines) on hand-made cream dó rice paper. Hand-carved
woodblock line quality — slightly rough, slightly uneven, unmistakably
Vietnamese. Speech bubbles are clean white rectangles with black
woodblock-style borders. Numbered panels 1-4 in small circles. English
dialogue must be grammatically correct and legible.

Shared cast convention (cross-book):
  Margie (62F, white, glasses), Priya (34F, brown, short bob),
  Harry (64M, white, bald), Marcus (34M, Black, beard).

Usage:
    python3 book-vietnam/scripts/gen_comics.py              # all assets
    python3 book-vietnam/scripts/gen_comics.py --covers-only
    python3 book-vietnam/scripts/gen_comics.py --scams-only
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import subprocess
import sys
import time
from pathlib import Path

import requests


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
COVERS_DIR = BOOK / "assets" / "covers"
SCAMS_DIR = BOOK / "assets" / "scam-comics"
COVERS_DIR.mkdir(parents=True, exist_ok=True)
SCAMS_DIR.mkdir(parents=True, exist_ok=True)


STYLE_COMIC = (
    "Dong Ho Vietnamese folk-woodblock-print style: hand-carved woodblock "
    "linework in black ink with slight roughness and character, warm earth "
    "palette of terracotta red, mustard yellow, ochre, and deep indigo on "
    "hand-made cream dó rice-paper background. Flat color fills inside bold "
    "black outlines. Faces are warm and readable, not caricatured. Speech "
    "bubbles are clean white rectangles with thin black woodblock borders. "
    "English text in speech bubbles must be clear, grammatically correct, "
    "and legible. No logos, no watermarks, no signatures. "
    "Unmistakably Vietnamese fine-folk-art feel."
)

STYLE_2X2 = (
    "Four-panel 2x2 comic grid. Each panel is a clean square with a thin "
    "cream-paper gutter between panels. Panels numbered 1-4 in small "
    "black-ink circles in the corner of each panel. "
)

# Shared cast — reuse wording verbatim so cross-book consistency holds.
CAST = (
    "Cast note: female tourists are either Margie (age 62, white, silver "
    "short bob, round tortoiseshell glasses, travel-linen shirt) or Priya "
    "(age 34, South Asian, shoulder-length brown hair, olive linen). Male "
    "tourists are either Harry (age 64, white, bald, khaki shirt) or "
    "Marcus (age 34, Black, short beard, teal shirt). Pick one per scam. "
)

# --- COVER PROMPTS --------------------------------------------------------

COVERS = [
    (
        "front",
        (
            "A single dramatic Dong Ho woodblock-folk-print scene, portrait "
            "2:3 aspect, depicting a Vietnam tourist-scam moment: Priya (age "
            "34, South Asian, shoulder-length brown hair, olive linen shirt), "
            "a female tourist standing in front of Hanoi's Old Quarter — a "
            "narrow yellow-ochre colonial facade with wooden shutters and a "
            "bánh mì cart — while a friendly-looking Vietnamese man in a polo "
            "shirt holding a smartphone says 'Grab driver? Your car this way!' "
            "in a white speech bubble. A small red motorbike waits at the "
            "curb. Warm golden-hour light. Composition leaves generous empty "
            "cream sky in the upper third for a book-cover title to be "
            "overlaid later. No book title, no watermark, no logo — just the "
            "illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single Dong Ho woodblock-folk-print scene, portrait 2:3 "
            "aspect, depicting a bustling Hanoi Old Quarter evening from a "
            "three-quarter overhead view: red paper lanterns strung across "
            "the street, a pho cart with steam rising, a cyclo passing in "
            "the distance, a pagoda silhouette against the twilight sky, and "
            "a small group of tourists walking among the locals. Substantial "
            "empty deep-indigo sky in the upper two-thirds of the frame to "
            "leave space for back-cover copy to be overlaid. Palette: "
            "terracotta red, mustard yellow, warm lantern glow, deep indigo. "
            "No text, no watermark, no book title."
        ),
        "2:3",
    ),
]


# --- ALL 66 SCAM COMICS ---------------------------------------------------
# Format: (city, n, scene description including dialogue)

SCAM_COMICS: list[tuple[str, int, str]] = [
    # HANOI (6)
    ("hanoi", 1,
     "Panel 1: Priya arrives at Hanoi Noi Bai Airport (HAN) arrivals hall "
     "with her carry-on; a friendly Vietnamese man in a polo shirt flashes "
     "a phone screen and says 'I am your Grab driver!' Panel 2: Priya looks "
     "at her own phone — the real Grab app shows a different driver name and "
     "plate. Panel 3: Priya says 'That's not the car in my app' and walks "
     "toward the official Grab pickup zone. Panel 4: Priya rides away in the "
     "correct, metered Grab car, smiling."),
    ("hanoi", 2,
     "Panel 1: Harry gets into a street taxi in Hanoi Old Quarter; driver "
     "says 'Meter okay!' Panel 2: The meter is jumping unusually fast — "
     "120,000 VND in just two minutes. Panel 3: Harry says 'Please stop the "
     "car' and gets out, handing the fair 50,000 VND. Panel 4: Harry opens "
     "Grab on his phone and books a licensed Mai Linh taxi instead."),
    ("hanoi", 3,
     "Panel 1: Harry walks through Hanoi Old Quarter; a shoe-shine boy "
     "suddenly starts polishing his sandal strap and says 'Glue break, "
     "need fix!' Panel 2: A moment later the boy demands '500,000 VND!' "
     "Panel 3: Harry firmly says 'No. I didn't ask for this.' and places "
     "20,000 VND on the step. Panel 4: Harry walks on, the boy moves to "
     "find another target."),
    ("hanoi", 4,
     "Panel 1: Margie strolls around Hoan Kiem Lake with a small crossbody "
     "bag; two teenagers on a motorbike approach from behind. Panel 2: One "
     "bumps into her — 'So sorry!' — while the other slips a hand toward "
     "her bag. Panel 3: Margie steps back, grips her bag strap, and says "
     "'No thank you!' firmly. Panel 4: Margie walks on with her bag now "
     "worn cross-body in front, hand resting on the zipper."),
    ("hanoi", 5,
     "Panel 1: Marcus near St. Joseph's Cathedral; a xe-om motorbike rider "
     "says 'Free Hanoi tour, friend! Only for you.' Panel 2: They ride; "
     "three hours later the rider demands '2,000,000 VND.' Panel 3: Marcus "
     "firmly: 'You said free. I'll pay 200,000 for the ride.' Panel 4: "
     "Marcus pays the fair ride fee and walks to his hotel, rider looks "
     "embarrassed."),
    ("hanoi", 6,
     "Panel 1: Marcus matches with a local woman on Tinder; she suggests "
     "'Let's meet at this bar in the Old Quarter.' Panel 2: At the bar, "
     "drinks keep arriving; the tab comes: '8,000,000 VND!' Panel 3: Marcus "
     "says 'Show me the menu prices.' Panel 4: He pays only the menu-priced "
     "drinks and leaves — lesson: pick the bar yourself, never follow."),

    # HA LONG BAY (6)
    ("ha-long-bay", 1,
     "Panel 1: Priya at her laptop booking a 'Ha Long Bay luxury cruise' on "
     "a slick-looking website. Panel 2: Arrival day — the meeting point "
     "doesn't exist and the phone number is disconnected. Panel 3: Priya "
     "checks the Ministry of Culture licensed-operator list on her phone — "
     "her 'cruise' isn't on it. Panel 4: Priya re-books on-site with a "
     "listed operator, boards a real cruise ship."),
    ("ha-long-bay", 2,
     "Panel 1: Margie at her Hanoi hotel lobby; a driver says 'Private "
     "transfer to Ha Long, 2,500,000 VND.' Panel 2: Margie checks a printed "
     "schedule: shared shuttle 300,000 VND, private transfer 1,200,000 VND "
     "tops. Panel 3: Margie: 'I'll take the shared shuttle, please.' "
     "Panel 4: Margie on the shuttle watching the karst limestone scenery "
     "roll past."),
    ("ha-long-bay", 3,
     "Panel 1: Harry aboard a Ha Long cruise; the crew says 'Kayak: "
     "500,000 VND extra. Cave entry: 300,000 VND extra.' Panel 2: Harry "
     "pulls up the cruise's official inclusion list on his phone — all "
     "listed as included. Panel 3: Harry shows the list to the manager. "
     "Panel 4: The activities are honored at no extra charge."),
    ("ha-long-bay", 4,
     "Panel 1: Marcus on a day trip; the guide says 'Special authentic "
     "floating village visit, 400,000 VND more.' Panel 2: They arrive at "
     "a staged dock with empty houses. Panel 3: Marcus researches on his "
     "phone: 'Cua Van is the real floating village.' Panel 4: Marcus "
     "switches to a licensed Cua Van tour the next day."),
    ("ha-long-bay", 5,
     "Panel 1: Priya exits Tuan Chau pier; a street-taxi driver says "
     "'Hotel? 800,000 VND.' Panel 2: The Grab app shows 180,000 VND for "
     "the same route. Panel 3: Priya declines and walks to the Grab pickup "
     "zone. Panel 4: Priya rides to her hotel at the fair metered price."),
    ("ha-long-bay", 6,
     "Panel 1: Margie booking on Booking.com; a host messages 'Pay by bank "
     "transfer, 20% discount!' Panel 2: Margie recognizes the red flag — "
     "off-platform = no protection. Panel 3: Margie replies 'I'll pay on "
     "the platform only.' Panel 4: The host backs down and accepts the "
     "Booking.com-processed payment."),

    # SAPA (6)
    ("sapa", 1,
     "Panel 1: Harry steps off the overnight train at Lao Cai station; a "
     "man waves 'Sapa bus, 200,000 VND each!' Panel 2: The official shuttle "
     "sign reads 50,000 VND. Panel 3: Harry walks past and boards the "
     "official green minivan. Panel 4: Harry enjoys the scenic hour ride "
     "up to Sapa at the correct price."),
    ("sapa", 2,
     "Panel 1: Priya in Sapa; an H'mong guide offers 'Village trek, only "
     "300,000 VND.' Panel 2: At a handicraft hut, intense pressure: 'You "
     "must buy scarf, our family need!' Panel 3: Priya says 'I'll buy one "
     "scarf I like — thank you for the trek.' Panel 4: Priya walks back "
     "to Sapa with one scarf she actually wanted."),
    ("sapa", 3,
     "Panel 1: Margie arriving at her booked Sapa homestay; the host says "
     "'Your room is closed. Upgrade 800,000 VND per night.' Panel 2: Margie "
     "shows her booking confirmation clearly. Panel 3: Host retreats: "
     "'Oh, your room is available actually.' Panel 4: Margie settles into "
     "her booked room at the booked rate."),
    ("sapa", 4,
     "Panel 1: Marcus at the Fansipan cable car; a tout says 'Cable car "
     "closed — I'll drive you to viewpoint for 1,500,000 VND.' Panel 2: "
     "Marcus checks the official Sun World website — cable car is running. "
     "Panel 3: Marcus buys the official ticket at the real booth. Panel 4: "
     "Marcus at the 3,143-meter summit, cable-car ride in the morning mist."),
    ("sapa", 5,
     "Panel 1: Priya boards a Sapa electric cart; driver says '500,000 "
     "VND for short trip.' Panel 2: The posted town-rate board reads "
     "50,000 VND per person. Panel 3: Priya points at the board; driver "
     "agrees to 50,000. Panel 4: Priya rides to her destination at the "
     "posted rate."),
    ("sapa", 6,
     "Panel 1: Harry in a Sapa village shop; a vendor insists 'Try on, "
     "try on! Must buy if you touch.' Panel 2: Harry politely says 'I am "
     "just looking, thank you.' Panel 3: The vendor blocks the doorway "
     "briefly. Panel 4: Harry firmly: 'No — excuse me,' and walks on; "
     "vendor steps aside."),

    # HUE (6)
    ("hue", 1,
     "Panel 1: Margie hops into a cyclo in Hue; rider says 'Tour, 100,000 "
     "VND, all day!' Panel 2: Midway, the rider stops and says 'Actually "
     "500,000 VND now.' Panel 3: Margie says 'We agreed 100,000. I'll pay "
     "that and take another cyclo home.' Panel 4: Margie pays 100,000, "
     "walks to a hotel-recommended cyclo stand instead."),
    ("hue", 2,
     "Panel 1: Priya lands at Hue Phu Bai Airport; a taxi driver says "
     "'Hotel? 700,000 VND!' Panel 2: Grab app shows 250,000 VND for the "
     "same route. Panel 3: Priya books Grab through the app. Panel 4: "
     "Priya arrives at her hotel at the fair fare."),
    ("hue", 3,
     "Panel 1: Marcus by the Perfume River; a guide says 'Dragon boat, "
     "must book now, last one!' Panel 2: Marcus sees five identical "
     "dragon boats waiting. Panel 3: Marcus takes his time and compares "
     "prices. Panel 4: Marcus boards a fairly-priced boat, no pressure."),
    ("hue", 4,
     "Panel 1: Harry at the Hue Imperial City entrance; a man outside says "
     "'Your ticket is single-entry — can't come back!' Panel 2: The real "
     "sign says 'Single entry valid for the day.' Panel 3: Harry checks "
     "the official ticket booth. Panel 4: Harry re-enters freely at the "
     "Imperial City within the same day."),
    ("hue", 5,
     "Panel 1: Priya on a Hue bicycle tour; an older woman approaches — "
     "'My granddaughter sick, please help.' Panel 2: A pushy handler is "
     "behind her. Panel 3: Priya says 'I can donate to a registered "
     "charity' and notes the local Red Cross address. Panel 4: Priya "
     "cycles on, handlers move off."),
    ("hue", 6,
     "Panel 1: Marcus rents a motorbike in Hue; owner says 'Just 150,000 "
     "VND per day!' Panel 2: Owner asks for passport as deposit — Marcus "
     "offers a photocopy and deposit cash instead. Panel 3: On return a "
     "'scratch' is pointed out; Marcus shows his time-stamped rental "
     "photos. Panel 4: Full deposit returned."),

    # HOI AN (6)
    ("hoi-an", 1,
     "Panel 1: Priya at a Hoi An tailor; the owner says 'Exclusive silk, "
     "3,000,000 VND for shirt!' Panel 2: Two shops down, the identical "
     "silk is 800,000 VND. Panel 3: Priya politely: 'I will think about "
     "it.' Panel 4: Priya orders at the fair-priced tailor with a receipt "
     "and fitting schedule."),
    ("hoi-an", 2,
     "Panel 1: Marcus on a Hoi An lantern boat at dusk; a monk in robes "
     "presses blessing bracelets on him. Panel 2: The 'monk' demands "
     "'Donation 500,000 VND.' Panel 3: Marcus hands the bracelet back — "
     "'Real monks do not demand. No thank you.' Panel 4: Marcus enjoys "
     "the ride, releasing his own paper lantern."),
    ("hoi-an", 3,
     "Panel 1: Margie on a Hoi An side street; a man with a lanyard says "
     "'Your ticket expired, pay 500,000 VND fine!' Panel 2: The real ticket "
     "is 120,000 VND valid for multiple days. Panel 3: Margie asks 'Which "
     "official office are you from?' Panel 4: The man walks off; Margie "
     "continues her visit."),
    ("hoi-an", 4,
     "Panel 1: Priya photographs a 'fruit lady' with her bamboo-pole "
     "baskets; the woman loads her shoulders — 'Now you pay 500,000 "
     "VND!' Panel 2: Priya looks shocked. Panel 3: Priya firmly: 'I will "
     "pay 50,000 for one photo, no more.' Panel 4: Priya continues; the "
     "fruit lady accepts the fair amount."),
    ("hoi-an", 5,
     "Panel 1: Harry at his hotel; the concierge says 'Best cooking class, "
     "I book for you.' Panel 2: At the class, quality is poor and the "
     "price is triple the Google rating. Panel 3: Harry cross-references "
     "Google reviews on his phone. Panel 4: Harry books directly with a "
     "well-reviewed school the next day."),
    ("hoi-an", 6,
     "Panel 1: Marcus rents a bicycle at the Hoi An beach; owner says "
     "'No deposit, just have fun!' Panel 2: On return the owner points "
     "at the chain: 'Broken, 2,000,000 VND!' Panel 3: Marcus shows a "
     "time-stamped rental photo. Panel 4: No extra charge; Marcus notes "
     "the shop's name to warn others."),

    # DA NANG (6)
    ("da-nang", 1,
     "Panel 1: Margie arrives late at Da Nang Airport (DAD); a man says "
     "'Grab? Your car this way!' Panel 2: Her Grab app shows a different "
     "driver. Panel 3: Margie: 'I'll wait for the driver in my app.' "
     "Panel 4: Her real Grab arrives — correct plate, metered ride to "
     "her hotel."),
    ("da-nang", 2,
     "Panel 1: Priya at Ba Na Hills cable car entrance in winter; a tout "
     "insists 'Fog too much, go to another viewpoint with me, 2,000,000 "
     "VND.' Panel 2: Priya checks the Sun World website — cable car is "
     "running. Panel 3: Priya buys the official cable-car ticket. "
     "Panel 4: Priya atop Ba Na Hills at the Golden Bridge."),
    ("da-nang", 3,
     "Panel 1: Harry inside a Marble Mountains jade shop; a clerk "
     "'gifts' a bracelet and expects a big purchase in return. Panel 2: "
     "Harry firmly: 'No thank you — I cannot accept.' and returns the "
     "bracelet. Panel 3: Harry leaves without pressure. Panel 4: Harry "
     "at the Marble Mountains summit, enjoying the view."),
    ("da-nang", 4,
     "Panel 1: Marcus walking My Khe Beach; a friendly man asks 'Where "
     "are you from?' then invites for 'tea, local custom.' Panel 2: At "
     "the tea shop the bill arrives: 6,000,000 VND. Panel 3: Marcus "
     "firmly refuses, offers menu-priced amount only. Panel 4: Marcus "
     "walks away — never follow strangers to an unchosen venue."),
    ("da-nang", 5,
     "Panel 1: Margie watches the Dragon Bridge fire show on a weekend "
     "evening — crowded. Panel 2: A teenager brushes against her pocket. "
     "Panel 3: Margie shifts her bag cross-body in front and taps her "
     "phone into a zipped pocket. Panel 4: Show ends; Margie still has "
     "phone, wallet, and passport."),
    ("da-nang", 6,
     "Panel 1: Priya rents a self-drive car in Da Nang; the owner says "
     "'Sign here, very simple.' Panel 2: On return the owner flags "
     "'invisible' damage and claims 40,000,000 VND. Panel 3: Priya "
     "shows her pre-drive video walkaround. Panel 4: Full deposit "
     "returned; Priya walks off."),

    # NHA TRANG (6)
    ("nha-trang", 1,
     "Panel 1: Harry lands at Cam Ranh Airport (CXR); a taxi driver says "
     "'1,200,000 VND to your hotel.' Panel 2: Grab shows 400,000 VND. "
     "Panel 3: Harry books Grab through the app. Panel 4: Harry arrives "
     "at the fair fare."),
    ("nha-trang", 2,
     "Panel 1: Margie on Nha Trang beach with her phone on a towel. "
     "Panel 2: A jogger 'trips' and snatches the phone in a single motion. "
     "Panel 3: Margie uses a friend's phone: 'Find My iPhone' + police "
     "113 + Tourist Information. Panel 4: Next day Margie keeps valuables "
     "in her hotel safe, only a cheap beach phone at the shore."),
    ("nha-trang", 3,
     "Panel 1: Marcus walking Nha Trang nightlife street; a woman invites "
     "'Special massage, very cheap!' Panel 2: Inside, the bill inflates "
     "to 5,000,000 VND with 'services.' Panel 3: Marcus pays menu amount, "
     "firmly. Panel 4: Marcus leaves — lesson: avoid street solicitations, "
     "book reputable spas by Google reviews."),
    ("nha-trang", 4,
     "Panel 1: Priya on a '4-island booze cruise'; guide says 'All drinks "
     "extra on board, 200,000 VND each.' Panel 2: The booking listed "
     "drinks included. Panel 3: Priya shows the booking confirmation. "
     "Panel 4: Drinks honored at no extra charge."),
    ("nha-trang", 5,
     "Panel 1: Harry picks up a menu at a Nha Trang restaurant — English "
     "menu shows 300,000 VND for pho. Panel 2: He glances at the Vietnamese "
     "menu left on another table: 80,000 VND. Panel 3: Harry asks: 'Please "
     "give me the Vietnamese menu — I can read prices.' Panel 4: Harry "
     "pays the local price, tipping fairly."),
    ("nha-trang", 6,
     "Panel 1: Margie books a Nha Trang hotel; manager asks for bank "
     "transfer outside Booking.com. Panel 2: Margie recognizes the red "
     "flag. Panel 3: Margie insists 'On-platform only, please.' Panel 4: "
     "Manager accepts; booking is protected."),

    # DALAT (6)
    ("dalat", 1,
     "Panel 1: Priya at Dalat Lien Khuong Airport (DLI); a man in a "
     "pretend-official vest says 'Taxi 1,500,000 VND, regulated price.' "
     "Panel 2: The Grab app shows 300,000 VND. Panel 3: Priya walks to "
     "the official taxi desk inside the terminal. Panel 4: Priya rides "
     "to Dalat at the fair rate."),
    ("dalat", 2,
     "Panel 1: Marcus signs up for Dalat canyoning; the operator has no "
     "visible license. Panel 2: On-site the harness looks frayed and there "
     "is no briefing. Panel 3: Marcus cancels and re-books with a "
     "Vietnam-National-Administration-of-Tourism-listed operator. Panel 4: "
     "Marcus safely rappels down a waterfall with proper gear."),
    ("dalat", 3,
     "Panel 1: Margie at the Dalat Flower Gardens entrance; scalper says "
     "'Ticket 300,000 VND — official booth closed.' Panel 2: The real "
     "booth is 40 meters away, 40,000 VND. Panel 3: Margie walks to the "
     "real booth. Panel 4: Margie inside, photographing the hydrangeas."),
    ("dalat", 4,
     "Panel 1: Harry book a 'luxury Dalat resort' on a flashy site. "
     "Panel 2: On arrival the address is a vacant lot. Panel 3: Harry "
     "cross-checks: listing wasn't on Booking.com or Agoda. Panel 4: "
     "Harry re-books through a recognized platform and reports the fake."),
    ("dalat", 5,
     "Panel 1: Priya at a Dalat night-market food stall; vendor charges "
     "'250,000 VND' for a tiny banh mi. Panel 2: Nearby stall posts "
     "40,000 VND. Panel 3: Priya politely declines and moves one stall "
     "over. Panel 4: Priya enjoys a proper banh mi at the fair price."),
    ("dalat", 6,
     "Panel 1: Marcus approached by an 'Easy Rider' motorbike guide: "
     "'Full day, 3,000,000 VND.' Panel 2: Guesthouse posted rate is "
     "700,000 VND. Panel 3: Marcus walks to a vetted Easy Rider "
     "collective. Panel 4: Marcus on a proper countryside ride at the "
     "fair rate."),

    # HO CHI MINH CITY (6)
    ("ho-chi-minh-city", 1,
     "Panel 1: Priya arrives at HCMC Tan Son Nhat Airport (SGN); a man "
     "says 'Grab? Your car!' flashing a phone screen. Panel 2: Her real "
     "Grab app shows a different driver/plate. Panel 3: Priya walks to "
     "the official Grab pickup zone. Panel 4: Priya rides away in the "
     "correct metered car."),
    ("ho-chi-minh-city", 2,
     "Panel 1: Harry in a taxi in District 1; meter runs unusually fast. "
     "Panel 2: Harry realizes the taxi is 'Vinasun' mis-spelled — a "
     "copycat. Panel 3: Harry says 'Stop here, please' and pays the "
     "fair amount by street distance. Panel 4: Harry hails a real "
     "Vinasun or Mai Linh the next time."),
    ("ho-chi-minh-city", 3,
     "Panel 1: Marcus on Bui Vien walking street; a 'hostess' waves him "
     "into a bar. Panel 2: Drinks and 'companionship' charges pile on; "
     "bill: 4,000,000 VND. Panel 3: Marcus firmly: 'Show me the menu. I "
     "pay menu prices only.' Panel 4: Marcus pays menu items and leaves — "
     "lesson: choose the bar, never follow a solicitor."),
    ("ho-chi-minh-city", 4,
     "Panel 1: Margie walking District 1 with her bag on the outside of "
     "her shoulder; a motorbike approaches. Panel 2: The passenger lunges "
     "for the strap. Panel 3: Margie has worn it cross-body under her "
     "jacket — the strap holds. Panel 4: Margie steps back against a "
     "wall; the motorbike speeds off empty-handed."),
    ("ho-chi-minh-city", 5,
     "Panel 1: Priya at Ben Thanh Market; a vendor says 'T-shirt, "
     "400,000 VND, real silk!' Panel 2: Saigon Square a block away shows "
     "80,000 VND for the same item. Panel 3: Priya negotiates down to "
     "100,000 VND at Ben Thanh or walks to Saigon Square. Panel 4: "
     "Priya leaves with the same shirt at a fair local price."),
    ("ho-chi-minh-city", 6,
     "Panel 1: Marcus booking an HCMC hotel; the host messages 'Pay by "
     "bank transfer, discount!' Panel 2: Marcus recognizes the off-platform "
     "red flag. Panel 3: Marcus insists on Booking.com/Agoda processing. "
     "Panel 4: Booking is protected; Marcus checks in smoothly."),

    # CAN THO (6)
    ("can-tho", 1,
     "Panel 1: Margie on a Mekong Delta day tour from HCMC; guide stops "
     "at a 'typical local restaurant' with no prices. Panel 2: Lunch bill "
     "is 800,000 VND per person for simple rice plates. Panel 3: Margie "
     "says 'I need to see a menu with prices.' Panel 4: Margie pays fair "
     "80,000 VND equivalent and notes the restaurant to avoid."),
    ("can-tho", 2,
     "Panel 1: Priya at Cai Rang floating market; a boat owner says "
     "'Private boat, 1,500,000 VND.' Panel 2: Group boat at the pier is "
     "150,000 VND per person. Panel 3: Priya joins the group boat. "
     "Panel 4: Priya watches the floating market at dawn at the fair rate."),
    ("can-tho", 3,
     "Panel 1: Harry steps off the bus in Can Tho; a driver offers "
     "'Hotel ride, 500,000 VND.' Panel 2: Grab shows 60,000 VND. Panel 3: "
     "Harry books Grab in-app. Panel 4: Harry arrives at his hotel at the "
     "fair price."),
    ("can-tho", 4,
     "Panel 1: Marcus books a 'Mekong homestay' off a sketchy listing. "
     "Panel 2: The address doesn't exist; a driver tries to reroute him "
     "to a commission partner. Panel 3: Marcus cancels and re-books a "
     "Booking.com-listed homestay. Panel 4: Marcus arrives at a real, "
     "licensed homestay with a proper welcome."),
    ("can-tho", 5,
     "Panel 1: Priya on a Mekong tour; guide pulls up to a 'coconut candy "
     "factory' — pressure to buy. Panel 2: Prices are double the town "
     "shops. Panel 3: Priya politely: 'I already have candy, thank you.' "
     "Panel 4: Priya enjoys the rest of the tour; guide gets the message."),
    ("can-tho", 6,
     "Panel 1: Margie signs up for a Mekong Delta tour with no visible "
     "license. Panel 2: On arrival the 'guide' is unlicensed and safety "
     "is thin. Panel 3: Margie checks Vietnam NAT license list on her "
     "phone. Panel 4: Margie re-books with a licensed tour company."),

    # PHU QUOC (6)
    ("phu-quoc", 1,
     "Panel 1: Marcus at Phu Quoc Airport (PQC) exit; a driver insists "
     "'Grab doesn't work here — 1,000,000 VND to hotel.' Panel 2: Marcus "
     "opens Grab — it works at the designated zone 50 meters away. "
     "Panel 3: Marcus walks to the zone. Panel 4: Metered Grab ride to "
     "his hotel at the fair rate."),
    ("phu-quoc", 2,
     "Panel 1: Margie on a 'pearl farm educational tour'; the 'tour' is "
     "a 45-minute sales pitch ending at the shop. Panel 2: Hard-sell: "
     "'Only one like it, 15,000,000 VND.' Panel 3: Margie firmly: 'I am "
     "not buying today.' Panel 4: Margie boards the bus back without a "
     "purchase; nothing lost but time."),
    ("phu-quoc", 3,
     "Panel 1: Harry rents a jet ski on a Phu Quoc beach; operator says "
     "'Deposit 10,000,000 VND, easy.' Panel 2: On return the operator "
     "points at a pre-existing scratch: '50,000,000 VND damage!' Panel 3: "
     "Harry shows his pre-ride time-stamped video. Panel 4: Full deposit "
     "returned."),
    ("phu-quoc", 4,
     "Panel 1: Priya at a beachfront Phu Quoc spa; the menu is 500,000 "
     "VND massage. Panel 2: Mid-massage, therapist says 'Add-on 1,000,000 "
     "VND?' Panel 3: Priya politely: 'Just the massage on the menu, "
     "thank you.' Panel 4: Priya pays the menu price and tips fairly."),
    ("phu-quoc", 5,
     "Panel 1: Marcus buys a 'Hon Thom cable car 4-island package' at a "
     "booth; seller adds 'Lunch upgrade, 1,000,000 VND extra.' Panel 2: "
     "Official Sun World listing shows lunch included. Panel 3: Marcus "
     "shows the listing. Panel 4: Upgrade canceled; Marcus enjoys the "
     "cable car and 4 islands at the published price."),
    ("phu-quoc", 6,
     "Panel 1: Margie books 'Phu Quoc Airbnb' — host asks for bank "
     "transfer off-platform. Panel 2: Margie recognizes the off-platform "
     "red flag. Panel 3: Margie insists on Airbnb processing. Panel 4: "
     "Host relents; booking is protected."),
]


def get_api_key() -> str:
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key.strip()
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "wavespeed-api-key", "-w"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit("could not read WAVESPEED_API_KEY from keychain or env")
    return result.stdout.strip()


def submit(api_key: str, prompt: str, aspect_ratio: str = "1:1") -> str:
    url = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
    r = requests.post(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, json={
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": "2k",
        "output_format": "jpeg",
    }, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["data"]["id"] if "data" in data and "id" in data["data"] else data["id"]


def poll(api_key: str, task_id: str, timeout: int = 360) -> str:
    url = f"https://api.wavespeed.ai/api/v3/predictions/{task_id}/result"
    headers = {"Authorization": f"Bearer {api_key}"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        body = r.json()
        payload = body.get("data", body)
        status = payload.get("status")
        if status == "completed":
            outputs = payload.get("outputs") or payload.get("output") or []
            return outputs if isinstance(outputs, str) else outputs[0]
        if status == "failed":
            raise RuntimeError(f"task failed: {body}")
        time.sleep(3)
    raise TimeoutError(f"task {task_id} timed out")


def download(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def generate(api_key: str, prompt: str, dest: Path, aspect_ratio: str) -> bool:
    try:
        task = submit(api_key, prompt, aspect_ratio)
        out_url = poll(api_key, task)
        download(out_url, dest)
        return True
    except Exception as e:
        print(f"✗ {dest}: {e}", file=sys.stderr)
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--covers-only", action="store_true")
    ap.add_argument("--scams-only", action="store_true")
    ap.add_argument("--workers", type=int, default=6,
                    help="parallel generations (default 6)")
    args = ap.parse_args()

    api_key = get_api_key()

    tasks: list[tuple[str, Path, str]] = []  # (prompt, dest, aspect)
    if not args.scams_only:
        for name, subject, aspect in COVERS:
            dest = COVERS_DIR / f"{name}.jpg"
            if dest.exists():
                print(f"· {name}.jpg exists — skipping (delete to regen)")
                continue
            prompt = f"{subject}\n\n{STYLE_COMIC}\n\n{CAST}"
            tasks.append((prompt, dest, aspect))

    if not args.covers_only:
        for city, n, subject in SCAM_COMICS:
            dest = SCAMS_DIR / city / f"{n}.jpg"
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                print(f"· {city}/{n}.jpg exists — skipping (delete to regen)")
                continue
            prompt = (
                f"{STYLE_2X2}Scene: {subject}\n\n{STYLE_COMIC}\n\n{CAST}"
            )
            tasks.append((prompt, dest, "1:1"))

    if not tasks:
        print("· nothing to generate")
        return

    print(f"→ Queuing {len(tasks)} generations across {args.workers} workers…")
    ok = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(generate, api_key, prompt, dest, aspect): dest
            for prompt, dest, aspect in tasks
        }
        for fut in concurrent.futures.as_completed(futures):
            dest = futures[fut]
            if fut.result():
                ok += 1
                kb = dest.stat().st_size / 1024
                print(f"  ✓ {dest.relative_to(BOOK)} ({kb:.0f} KB)  [{ok}/{len(tasks)}]")
    print(f"\nDone: {ok} / {len(tasks)} succeeded")


if __name__ == "__main__":
    main()
