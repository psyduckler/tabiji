#!/usr/bin/env python3
"""Part 4: Days 45-46"""
import json

def P(lat,lng,label,n,cat="attraction",desc=""):
    return {"lat":lat,"lng":lng,"label":label,"num":n,"cat":cat,"desc":desc or label}
def A(t,d,det=None):
    return {"title":t,"description":d,"details":det or []}
def M(t,n,d,m=""):
    return {"type":t,"name":n,"description":d,"meta":m}
def T(t):
    return {"type":"tip","text":t}
def TB(l,a=None,m=None,t=None):
    return {"label":l,"activities":a or [],"meals":m or [],"tips":t or []}
def D(n,t,h,d,tbs,pins):
    return {"num":n,"title":t,"neighborhoods":h,"description":d,"timeBlocks":tbs,"mapPins":pins}

days = []

# DAY 45 - Tasmania: Family & Wilderness
days.append(D(45,"Tasmania — Family & Wilderness","Hobart · Cradle Mountain · Friends",
"A treasured day with Tasmanian friends and family, and a chance to see more of this wild island.",
[TB("Morning — Cradle Mountain Day Trip (Optional)",
    [A("🏔️ Cradle Mountain — Dove Lake Circuit","If energy permits, drive to Cradle Mountain (2.5 hrs each way). The Dove Lake Circuit (6 km, 2-3 hrs) around the glacial lake with Cradle Mountain reflected in still water is one of Australia's greatest walks.",
       ["📍 Cradle Mountain-Lake St Clair NP · $30 vehicle pass",
        "💡 May/June = stunning autumn colours but check snow/ice forecast",
        "⏱️ Full day with driving — early start 6 AM"]),
     A("🐨 Or: Bonorong Wildlife Sanctuary","If Cradle Mountain is too far, Bonorong near Richmond is excellent — hand-feed kangaroos, see wombats, and the Tasmanian devil feeding sessions are extraordinary.",
       ["📍 593 Mt Pleasant Rd · $28/adult",
        "💡 Tassie devils are genuinely bizarre and wonderful"])],
    [M("Breakfast","Hobart","Early start whichever direction you go.","💰 $10-15/pp")]),
 TB("Afternoon — Family Time",
    [A("👨‍👩‍👧 Friends & Family in Tasmania","Spend quality time with your Tassie connections. Let them take you to their secret spots — this is how you truly know a place.",
       ["📍 Wherever they take you"])],
    [M("Lunch","Family or Local Café","Enjoy the company.","💰 $12-20/pp"),
     M("Dinner","Farewell Tasmania Dinner","One last excellent meal in Hobart. Franklin Restaurant for wood-fired vegetarian dishes if budget allows.",
       "📍 Hobart · 💰 $35-55/pp")])],
[P(-41.6386,145.9373,"Cradle Mountain",1),P(-42.7773,147.4517,"Bonorong Wildlife",2),P(-42.8821,147.3272,"Hobart",3)]))

# DAY 46 - Final Day: Fly back to Sydney
days.append(D(46,"Fly Home — Sydney Farewell","Hobart → Sydney",
"The final day. Fly back to Sydney to complete your extraordinary 46-day journey around Australia and New Zealand.",
[TB("Morning — Last Hobart Morning",
    [A("🌅 Final Hobart Morning","A slow morning. Walk to the waterfront, grab a coffee at Salamanca, and watch the fishing boats.",
       ["📍 Salamanca Wharf · FREE",
        "💡 Pick up local honey, lavender products, or Tasmanian whisky as gifts"])],
    [M("Breakfast","Jackman & McRoss (Battery Point)","One of Hobart's best bakeries. Croissants, pastries, coffee.",
       "📍 57-59 Hampden Rd · 💰 $10-16/pp")]),
 TB("Midday — Flight to Sydney",
    [A("✈️ Hobart → Sydney","~2-hour flight. You've done it.",
       ["📍 HBA → SYD · ~2 hrs",
        "💡 You leave having seen more of Australia than most Australians ever will"])],
    [M("Lunch","Airport or on arrival","Transition meal.","💰 $12-20/pp")]),
 TB("Evening — Sydney Homecoming",
    [A("🎉 Sydney — You Made It!","46 days. Two countries. Six Australian states plus the Northern Territory. New Zealand. Major natural wonders, cultural landmarks, ancient Indigenous sites, family connections, and one very meaningful grave visit in Auckland.",
       ["🏆 Sydney Opera House, Great Barrier Reef, Uluru, Kakadu, Twelve Apostles, Whitehaven Beach, Freycinet, MONA, Blue Mountains, Daintree, Rangitoto, Te Papa, Weta Workshop — and so much more",
        "💙 And Auckland: a great grandfather remembered across generations",
        "💡 You deserve a very nice dinner tonight"])],
    [M("Dinner","Quay or Aria (Sydney)","Celebrate with a special dinner at one of Sydney's finest. Both have spectacular harbour views and excellent vegetarian menus.",
       "📍 Sydney Harbour · 💰 $80-150/pp · Book ahead")],
    [T("💡 You've just completed one of the great travel experiences. Australia is vast — you've touched its heart in 46 extraordinary days.")])],
[P(-42.8821,147.3272,"Hobart",1),P(-33.8568,151.2153,"Sydney Opera House",2),P(-33.8523,151.2108,"Sydney Harbour Bridge",3)]))

if __name__ == "__main__":
    print(json.dumps(days))
