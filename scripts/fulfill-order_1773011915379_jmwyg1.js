const fulfillOrder = require('../functions/fulfill-order');
const path = require('path');

const order = {
  id: 'order_1773011915379_jmwyg1',
  email: 'eduardo.henrique0518@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-04-27',
  endDate: '2026-05-11',
  groupSize: '3-4',
  requests: "We love cars and it's our first time in Japan. We are going to Tokyo, Osaka, Kyoto(round trip in a day), Nagoya and finally Tokyo again for the last 2 days of the trip"
};

// Load days from JSON files
const days1to5 = require(path.join(__dirname, 'fulfill-order_1773011915379_jmwyg1-day1-5.json'));
const days6to10 = require(path.join(__dirname, 'fulfill-order_1773011915379_jmwyg1-day6-10.json'));
const days11to15 = require(path.join(__dirname, 'fulfill-order_1773011915379_jmwyg1-day11-15.json'));

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Japan for Car Lovers — First Time, Full Throttle',
  subtitle: '15 days across Tokyo, Osaka, Kyoto, Nagoya & back — JDM culture, ancient temples & family fun',
  description: "This is the ultimate first-time Japan trip for a family that lives and breathes cars. You'll hunt JDM legends at Daikoku PA, stand where Toyota was born in Nagoya, go-kart through Tokyo's neon streets, and still have time for ancient temples, insane street food, and Golden Week festivals. From the Wangan highway to the bamboo groves of Arashiyama — every day is a new gear.",
  duration: '14 nights',
  dates: 'Apr 27 – May 11, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Families · Car Enthusiasts · First-Timers',
  highlights: [
    'Daikoku PA night car meet — legendary JDM gathering',
    'Toyota Commemorative Museum in Nagoya — where it all began',
    'Go-kart through Tokyo streets in costume',
    'Super Autobacs & Up Garage — JDM parts paradise',
    'Fushimi Inari & Arashiyama Bamboo Grove day trip',
    'Osaka street food crawl through Dotonbori',
    'teamLab Borderless — immersive digital art',
    'Akihabara car culture shops & anime district',
    'Golden Week festivals & celebrations',
    'SCMAGLEV Railway Park — world\'s fastest train'
  ],
  essentials: [
    { title: '🚅 Shinkansen & IC Cards', text: "Get a 14-day Japan Rail Pass before you go — it covers all Shinkansen (bullet trains) between cities and most JR local lines. For subways and buses, grab a Suica or Pasmo IC card at any station — tap-and-go everywhere. Kids 6-11 ride at half price; under 6 free." },
    { title: '🌸 Golden Week Alert', text: "Your trip overlaps with Golden Week (Apr 29 – May 5) — Japan's biggest holiday stretch. Trains, attractions, and hotels will be packed. Book Shinkansen seats in advance, arrive at popular spots early, and embrace the festive energy. Many special events happen only during this week." },
    { title: '🚗 Car Culture Tips', text: "Daikoku PA is busiest Friday/Saturday nights (9pm–1am). Super Autobacs in Odaiba is the biggest auto parts store. Up Garage has used JDM parts. For go-karting, book 2+ days ahead — you need an International Driving Permit (IDP). Drivers must be 18+." },
    { title: '👨‍👩‍👧‍👦 Family Essentials', text: "Japan is incredibly family-friendly. Convenience stores (7-Eleven, Lawson, FamilyMart) are everywhere with snacks, drinks, and ATMs. Most train stations have elevators. Coin lockers store luggage. Kids love capsule toy machines (gashapon) found everywhere." },
    { title: '💴 Money & Budget', text: "Japan is still partly cash-based — carry ¥10,000-20,000 daily. 7-Eleven ATMs accept foreign cards. Budget roughly: meals ¥800-3,000/person, trains (with JR Pass) covered, attractions ¥500-2,500. Your $5,000-10,000 for 15 days with 3-4 people is comfortable for mid-range." },
    { title: '🗣️ Language & Etiquette', text: "Learn: Sumimasen (excuse me), Arigatou (thank you), Onegaishimasu (please). Bow slightly when greeting. Remove shoes entering homes/temples/some restaurants. Don't tip — it's considered rude. Slurp ramen loudly — it's a compliment to the chef!" }
  ],
  days: [...days1to5, ...days6to10, ...days11to15]
};

fulfillOrder(order, itineraryData);
