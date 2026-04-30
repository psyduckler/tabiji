"""Per-variant manifest for /scams/everywhere/ comics.

Each entry: (page_slug, card_id, variant_slug, character, scene_md).

The variant_slug is the URL-safe identifier used as the R2 filename and
the <img> alt-text anchor. The character is one of the locked cast
members from cast.py. The scene is a 4-panel description matching the
flat-cel-shaded everywhere style.

Cast distribution across 51 variants — roughly even split:
  margie 13 · priya 12 · harry 13 · marcus 13
"""
from __future__ import annotations

# (page_slug, card_id, variant_slug, character, scene)
MANIFEST: list[tuple[str, str, str, str, str]] = [
    # ============================================================
    # AI VOICE CLONE SCAMS (5 variants)
    # ============================================================
    ("ai-voice-clone-scams", "scam-1", "family-emergency-voice-clone", "margie", (
        "Panel 1: Margie answers her cordless phone at her kitchen counter, "
        "concerned. Speech bubble (voice from phone): \"Mom, I'm in jail — I "
        "need bail money fast.\"\n"
        "Panel 2: Margie at her laptop initiating a wire transfer, the phone "
        "still pressed to her ear. Speech bubble (voice): \"Don't tell Dad — "
        "just wire it now.\"\n"
        "Panel 3: Margie pauses, sets the phone down, and dials a different "
        "number on her cell. Speech bubble (Margie): \"Wait — let me call you "
        "back on your real number.\"\n"
        "Panel 4: Margie smiles in relief, on a video call with her real son "
        "who is at home. Speech bubble (real son): \"I'm fine, Mom — that "
        "wasn't me.\""
    )),
    ("ai-voice-clone-scams", "scam-2", "reverse-grandparent-voice-clone", "priya", (
        "Panel 1: Priya at her dining table answers a call. Speech bubble "
        "(voice from phone): \"Honey, this is Grandma — I need you to wire "
        "money for the hospital.\"\n"
        "Panel 2: Priya frowns, the voice matches her grandmother's exactly. "
        "Speech bubble (voice): \"Don't tell your parents — they'll just "
        "worry.\"\n"
        "Panel 3: Priya hangs up and FaceTimes her real grandmother on her "
        "phone. Speech bubble (Priya): \"Grandma — are you in the hospital?\"\n"
        "Panel 4: Priya's real grandmother appears on screen, healthy at home "
        "with her tea. Speech bubble (real grandma): \"I'm fine, dear — "
        "someone cloned my voice.\""
    )),
    ("ai-voice-clone-scams", "scam-3", "workplace-cfo-voice-clone", "priya", (
        "Panel 1: Priya at her office desk answers her phone. Speech bubble "
        "(voice from phone): \"This is the CFO — I need you to approve a wire "
        "transfer right now.\"\n"
        "Panel 2: Priya looks at her laptop showing a wire-approval form, "
        "uncertain. Speech bubble (voice): \"Don't loop in IT — this is "
        "confidential.\"\n"
        "Panel 3: Priya walks down the hall and knocks on the real CFO's "
        "open office door. Speech bubble (Priya): \"Did you just call about a "
        "wire?\"\n"
        "Panel 4: The real CFO at her desk looks up, surprised. Speech bubble "
        "(real CFO): \"No — that wasn't me. Loop in security now.\""
    )),
    ("ai-voice-clone-scams", "scam-4", "ai-deepfake-romance-video", "harry", (
        "Panel 1: Harry on his couch on a video call with a smiling young "
        "woman on his laptop. Speech bubble (woman): \"I love seeing your "
        "face every day.\"\n"
        "Panel 2: The video call shows the woman asking for a wire transfer, "
        "Harry's expression turning concerned. Speech bubble (woman): \"My "
        "visa fee fell through — can you help?\"\n"
        "Panel 3: Harry drags the video into a reverse-image-search browser "
        "tab on his laptop. Speech bubble (Harry): \"Let me check this "
        "image.\"\n"
        "Panel 4: The reverse search shows the same face on a stock-photo site "
        "and a deepfake-detection report. Speech bubble (Harry): \"Not a real "
        "person.\""
    )),
    ("ai-voice-clone-scams", "scam-5", "silent-call-voice-harvest", "margie", (
        "Panel 1: Margie's phone rings showing UNKNOWN, she answers at her "
        "kitchen counter. Speech bubble (Margie): \"Hello? Hello?\"\n"
        "Panel 2: The line stays silent, then a faint click; Margie speaks "
        "again. Speech bubble (Margie): \"Is anyone there?\"\n"
        "Panel 3: Margie hangs up, the call log shows three unknown silent "
        "calls today. Caption box: \"Silent calls harvest your voice for "
        "later cloning.\"\n"
        "Panel 4: Margie taps the SILENCE UNKNOWN CALLERS toggle on her "
        "phone. Speech bubble (Margie): \"Unknown callers — straight to "
        "voicemail.\""
    )),
    # ============================================================
    # BANK IMPERSONATION + ZELLE (5 variants)
    # ============================================================
    ("bank-impersonation-and-zelle", "scam-1", "fake-bank-fraud-dept-safe-account", "margie", (
        "Panel 1: Margie at her kitchen counter answers her phone, alarmed. "
        "Speech bubble (voice from phone): \"This is your bank's fraud "
        "department — your account is being drained.\"\n"
        "Panel 2: Margie at her laptop with the bank's transfer form open, "
        "the voice still in her ear. Speech bubble (voice): \"Move your "
        "money to this safe account immediately.\"\n"
        "Panel 3: Margie hangs up and calls the number printed on the back of "
        "her debit card. Speech bubble (Margie): \"I'll call the number on "
        "my card.\"\n"
        "Panel 4: Real bank rep on the phone with Margie. Speech bubble "
        "(real rep): \"We didn't call you — and a real bank never asks you "
        "to move money.\""
    )),
    ("bank-impersonation-and-zelle", "scam-2", "reverse-deposit-oops-send-back", "harry", (
        "Panel 1: Harry at his kitchen table, phone in hand, sees a "
        "$3,000 deposit notification. Speech bubble (Harry): \"Where did "
        "this come from?\"\n"
        "Panel 2: Harry's phone rings; voice claims a wrong-account-number "
        "error. Speech bubble (voice): \"Sorry, that was meant for someone "
        "else — please send it back.\"\n"
        "Panel 3: Harry pauses, doesn't open Zelle. Speech bubble (Harry): "
        "\"Let me call the bank first.\"\n"
        "Panel 4: Harry on the phone with his real bank, learning the "
        "deposit was a fraudulent check that will reverse. Speech bubble "
        "(real bank rep): \"That deposit will bounce — don't send "
        "anything.\""
    )),
    ("bank-impersonation-and-zelle", "scam-3", "marketplace-seller-zelle-clawback", "priya", (
        "Panel 1: Priya at her apartment hands a buyer her old bicycle in "
        "exchange for a Zelle confirmation on his phone. Speech bubble "
        "(buyer): \"Just sent it — see?\"\n"
        "Panel 2: Three days later Priya's bank app shows the Zelle deposit "
        "reversed. Speech bubble (Priya): \"Reversed — what?\"\n"
        "Panel 3: Priya on the phone with her bank's fraud line. Speech "
        "bubble (real bank rep): \"The sender's account was compromised — "
        "Zelle has no buyer-protection clawback.\"\n"
        "Panel 4: Priya at her laptop filing a police report, an FTC "
        "complaint open in another tab. Speech bubble (Priya): \"Cash or "
        "verified bank transfer only next time.\""
    )),
    ("bank-impersonation-and-zelle", "scam-4", "authorized-but-deceived-pig-butchering", "harry", (
        "Panel 1: Harry at his kitchen table on a video call with a smiling "
        "woman, his laptop showing a crypto-trading dashboard. Speech "
        "bubble (woman): \"My uncle's signals never miss — wire just "
        "$50,000.\"\n"
        "Panel 2: Harry at his bank initiating an authorized wire transfer. "
        "The teller pauses, concerned. Speech bubble (teller): \"Sir — is "
        "someone telling you to send this?\"\n"
        "Panel 3: Harry pauses, taken aback. Speech bubble (Harry): \"It's "
        "for an investment platform online.\"\n"
        "Panel 4: The teller hands Harry an FBI pig-butchering pamphlet. "
        "Speech bubble (teller): \"Please call this number before we send "
        "anything.\""
    )),
    ("bank-impersonation-and-zelle", "scam-5", "hey-its-your-nephew-zelle", "margie", (
        "Panel 1: Margie's phone buzzes with a text from an unknown number. "
        "Speech bubble (text): \"Hey Aunt Margie, it's your nephew Tom — "
        "I lost my phone, can you Zelle me $500?\"\n"
        "Panel 2: Margie at her kitchen counter opens her Zelle app, "
        "uncertain. Speech bubble (Margie): \"Tom?\"\n"
        "Panel 3: Margie calls her real nephew Tom on his old number. Speech "
        "bubble (Margie): \"Tom — are you OK?\"\n"
        "Panel 4: Real Tom on FaceTime in his apartment, his phone fine. "
        "Speech bubble (real Tom): \"My phone is right here — that wasn't "
        "me.\""
    )),
    # ============================================================
    # CONCERT + EVENT TICKET SCAMS (3 variants)
    # ============================================================
    ("concert-and-event-ticket-scams", "scam-1", "reddit-dm-i-have-extras", "marcus", (
        "Panel 1: Marcus on his laptop scrolling Reddit DMs, a stranger "
        "offers extras. Speech bubble (DM): \"I have 2 extras for the show "
        "— Venmo F&F, $400.\"\n"
        "Panel 2: Marcus sees fake Ticketmaster confirmation screenshots in "
        "the DM. Speech bubble (DM): \"Real proof — see the screenshots?\"\n"
        "Panel 3: Marcus closes the DM and opens StubHub on his phone. "
        "Speech bubble (Marcus): \"Verified resale only.\"\n"
        "Panel 4: Marcus at the venue scanning his StubHub ticket at the "
        "gate. Speech bubble (Marcus): \"$1,000 platform fee beats $400 "
        "lost.\""
    )),
    ("concert-and-event-ticket-scams", "scam-2", "hijacked-verified-resale-account", "priya", (
        "Panel 1: Priya on her laptop browsing StubHub, sees a great-priced "
        "listing from a brand-new seller. Speech bubble (Priya): \"Way "
        "below market — too good?\"\n"
        "Panel 2: Priya hovers over the seller profile — created today, "
        "zero history. Speech bubble (Priya): \"Brand-new account.\"\n"
        "Panel 3: Priya picks a different listing from a long-tenured "
        "seller. Speech bubble (Priya): \"Established seller only.\"\n"
        "Panel 4: Priya enters the venue with a verified ticket while the "
        "first listing shows CANCELED. Speech bubble (Priya): \"Hijacked "
        "accounts get pulled before the show.\""
    )),
    ("concert-and-event-ticket-scams", "scam-3", "counterfeit-pdf-ticket-at-gate", "marcus", (
        "Panel 1: Marcus buys a PDF ticket from a Craigslist seller in a "
        "parking lot, hands over cash. Speech bubble (seller): \"Print "
        "this — section 110.\"\n"
        "Panel 2: Marcus at the venue gate, the gate scanner beeps red. "
        "Speech bubble (scanner display): \"DUPLICATE — TICKET ALREADY "
        "USED.\"\n"
        "Panel 3: Gate agent shakes her head, points to the verified-resale "
        "kiosk. Speech bubble (agent): \"This barcode was sold three times "
        "— next time use a verified platform.\"\n"
        "Panel 4: Marcus at home filing an FTC complaint with the bank "
        "fraud line on speakerphone. Speech bubble (Marcus): \"Gate scan "
        "is the only real verification.\""
    )),
    # ============================================================
    # FAKE JOB OFFERS (3 variants)
    # ============================================================
    ("fake-job-offers", "scam-1", "linkedin-fake-recruiter-dm", "priya", (
        "Panel 1: Priya at her apartment desk reads a LinkedIn DM on her "
        "laptop. Speech bubble (DM): \"Hi Priya — Senior PM role at a top "
        "fintech, $180K, fully remote.\"\n"
        "Panel 2: Priya gets an email asking for a $200 'equipment "
        "deposit.' Speech bubble (email): \"Reimbursed in your first "
        "paycheck.\"\n"
        "Panel 3: Priya searches the company's careers page directly — no "
        "such role listed. Speech bubble (Priya): \"Not on their site.\"\n"
        "Panel 4: Priya reports the recruiter's profile to LinkedIn and "
        "files an FTC complaint. Speech bubble (Priya): \"No real "
        "employer asks for money up front.\""
    )),
    ("fake-job-offers", "scam-2", "onboarding-identity-harvest", "marcus", (
        "Panel 1: Marcus on his laptop on a video interview, the "
        "interviewer in a generic backdrop. Speech bubble (interviewer): "
        "\"Welcome aboard — please fill out the W-9 link.\"\n"
        "Panel 2: The W-9 form asks for SSN, bank account, and a photo of "
        "Marcus's driver's license. Speech bubble (Marcus): \"Before any "
        "contract?\"\n"
        "Panel 3: Marcus looks up the company on the BBB and the state's "
        "business registry — no record found. Speech bubble (Marcus): "
        "\"Not a real company.\"\n"
        "Panel 4: Marcus closes the form, freezes his credit at the three "
        "bureaus on his phone. Speech bubble (Marcus): \"Credit frozen "
        "before they harvested anything.\""
    )),
    ("fake-job-offers", "scam-3", "equipment-deposit-cashiers-check", "priya", (
        "Panel 1: Priya opens her mailbox to find a cashier's check for "
        "$3,500 from her 'new employer.' Speech bubble (Priya): "
        "\"Equipment funds?\"\n"
        "Panel 2: An email instructs her to deposit the check, then Zelle "
        "$2,800 to a vendor. Speech bubble (email): \"Buy from this "
        "approved vendor — keep $700 as your bonus.\"\n"
        "Panel 3: Priya at the bank counter asks the teller about the "
        "check first. Speech bubble (teller): \"Cashier's checks can clear "
        "and then reverse — this is a fake-check scam.\"\n"
        "Panel 4: Priya tears up the check and reports the email to the "
        "FTC and FBI IC3. Speech bubble (Priya): \"Real employers don't "
        "send checks before contracts.\""
    )),
    # ============================================================
    # GIFT-CARD SCAMS (3 variants)
    # ============================================================
    ("gift-card-scams", "scam-1", "boss-impersonation-bec-gift-cards", "priya", (
        "Panel 1: Priya at her office desk reads an urgent email from "
        "'the CEO.' Speech bubble (email): \"Need 10 x $100 Amazon gift "
        "cards for a client gift — send codes ASAP.\"\n"
        "Panel 2: Priya at a Walgreens reaching for $1,000 in gift "
        "cards. She pauses to look at the email's sender domain.\n"
        "Panel 3: Priya squints at the email — the domain has an extra "
        "letter. Speech bubble (Priya): \"That's not the real domain.\"\n"
        "Panel 4: Priya at her desk calling the real CEO on his cell to "
        "verify. Speech bubble (real CEO): \"That wasn't me — forward it "
        "to security.\""
    )),
    ("gift-card-scams", "scam-2", "government-utility-gift-card-demand", "margie", (
        "Panel 1: Margie at her kitchen counter answers her phone, the "
        "voice claiming to be from the IRS. Speech bubble (voice): \"You "
        "owe back taxes — pay with Apple gift cards or face arrest.\"\n"
        "Panel 2: Margie at a drugstore reaching for $500 Apple gift "
        "cards, phone still pressed to her ear. Speech bubble (voice): "
        "\"Read me the codes immediately.\"\n"
        "Panel 3: A drugstore cashier intervenes, gesturing at the gift "
        "cards. Speech bubble (cashier): \"Ma'am — the IRS never asks for "
        "gift cards.\"\n"
        "Panel 4: Margie at home with her daughter on her laptop filing an "
        "FTC report. Speech bubble (Margie): \"No agency takes gift "
        "cards.\""
    )),
    ("gift-card-scams", "scam-3", "in-store-card-draining-sticker-overlay", "harry", (
        "Panel 1: Harry at a grocery-store gift-card rack picks a $500 "
        "Visa card off the rack to give as a birthday gift. Speech bubble "
        "(Harry): \"$500 should do it.\"\n"
        "Panel 2: Harry at home hands the card to his grandkid who scans "
        "the barcode at checkout — DECLINED. Speech bubble (cashier "
        "display): \"BALANCE: $0.\"\n"
        "Panel 3: Harry inspects the card under a lamp — the barcode "
        "sticker peels off, revealing a different barcode underneath. "
        "Speech bubble (Harry): \"Sticker overlay.\"\n"
        "Panel 4: Harry at a different store, picking a card from "
        "BEHIND the rack instead of the front. Speech bubble (Harry): "
        "\"Always pull from behind the front row.\""
    )),
    # ============================================================
    # MARKETPLACE SCAMS — FB / CRAIGSLIST (4 variants)
    # ============================================================
    ("marketplace-scams-fb-craigslist", "scam-1", "fake-listing-non-delivery", "priya", (
        "Panel 1: Priya on her laptop browsing Facebook Marketplace, sees a "
        "$200 PS5 listing with stock-photo images. Speech bubble (Priya): "
        "\"Way below market.\"\n"
        "Panel 2: Priya messages the seller; the seller demands Zelle "
        "before any meetup. Speech bubble (seller): \"Zelle me first, then "
        "I'll arrange shipping.\"\n"
        "Panel 3: Priya does a reverse-image search — the listing photo is "
        "from a different seller's eBay listing. Speech bubble (Priya): "
        "\"Stolen photo.\"\n"
        "Panel 4: Priya reports the listing to Facebook and finds a real "
        "local seller for in-person cash pickup. Speech bubble (Priya): "
        "\"Cash, in-person, daylight, public spot.\""
    )),
    ("marketplace-scams-fb-craigslist", "scam-2", "google-voice-6-digit-hijack", "marcus", (
        "Panel 1: Marcus on his phone listing a guitar on Craigslist, gets "
        "a buyer message. Speech bubble (buyer): \"Want to verify you're "
        "real — I'll send a 6-digit code, just text it back.\"\n"
        "Panel 2: Marcus's phone shows a Google Voice verification text. "
        "Speech bubble (Marcus): \"Why does buying a guitar need a "
        "code?\"\n"
        "Panel 3: Marcus searches 'Google Voice 6-digit code scam' on his "
        "laptop. Speech bubble (search result): \"Scammer hijacks your "
        "phone number to register Google Voice.\"\n"
        "Panel 4: Marcus blocks the buyer and never sends the code. Speech "
        "bubble (Marcus): \"Never share verification codes.\""
    )),
    ("marketplace-scams-fb-craigslist", "scam-3", "compromised-payment-clawback", "priya", (
        "Panel 1: Priya hands a buyer her bicycle in a coffee-shop parking "
        "lot, watching the Zelle confirmation appear on the buyer's phone. "
        "Speech bubble (buyer): \"Sent — see?\"\n"
        "Panel 2: Five days later Priya's bank app shows the Zelle "
        "reversed: \"Sender's account closed — funds returned.\" Speech "
        "bubble (Priya): \"Reversed?\"\n"
        "Panel 3: Priya on the phone with her bank's fraud line. Speech "
        "bubble (real bank rep): \"That sender used a stolen account — "
        "Zelle has no clawback protection.\"\n"
        "Panel 4: Priya updates her listings: 'CASH ONLY, IN-PERSON, "
        "DAYLIGHT.' Speech bubble (Priya): \"Bills first, then bicycle.\""
    )),
    ("marketplace-scams-fb-craigslist", "scam-4", "rental-scam-fake-apartment", "marcus", (
        "Panel 1: Marcus on his laptop browsing Facebook apartment "
        "listings, sees a $1,200/mo studio in a $2,500/mo neighborhood. "
        "Speech bubble (Marcus): \"This price is wrong.\"\n"
        "Panel 2: The 'landlord' messages: pay first month + deposit via "
        "Zelle to 'hold' the unit, no in-person tour. Speech bubble "
        "(landlord): \"I'm overseas — Zelle the deposit and I'll mail you "
        "keys.\"\n"
        "Panel 3: Marcus reverse-image-searches the photo — same "
        "apartment posted by the real landlord on Apartments.com at the "
        "actual market rate. Speech bubble (Marcus): \"Stolen listing "
        "photo.\"\n"
        "Panel 4: Marcus reports the fake to Facebook and books a real "
        "in-person tour. Speech bubble (Marcus): \"No tour, no rent — "
        "ever.\""
    )),
    # ============================================================
    # MEDICARE + ELDER SCAMS (6 variants)
    # ============================================================
    ("medicare-and-elder-scams", "scam-1", "new-plastic-medicare-card", "margie", (
        "Panel 1: Margie at her kitchen counter answers her phone. Speech "
        "bubble (voice from phone): \"Medicare is issuing new plastic "
        "cards — verify your number to receive yours.\"\n"
        "Panel 2: The voice asks for her full Medicare number, SSN, and "
        "bank account. Speech bubble (Margie): \"That's a lot of "
        "information.\"\n"
        "Panel 3: Margie hangs up and calls 1-800-MEDICARE on her phone. "
        "Speech bubble (real Medicare rep): \"We never call to ask for "
        "your number — your card is paper, not plastic.\"\n"
        "Panel 4: Margie reports the call to Senior Medicare Patrol on "
        "her laptop. Speech bubble (Margie): \"Medicare doesn't cold-call "
        "anyone.\""
    )),
    ("medicare-and-elder-scams", "scam-2", "catheter-dme-billing-fraud", "harry", (
        "Panel 1: Harry opens a package in his mailbox — unsolicited "
        "catheters and a leg brace he never ordered. Speech bubble "
        "(Harry): \"I didn't order any of this.\"\n"
        "Panel 2: Harry checks his Medicare Summary Notice on his laptop "
        "— $4,200 billed for DME he never received. Speech bubble "
        "(Harry): \"Billed in my name.\"\n"
        "Panel 3: Harry on the phone with Senior Medicare Patrol, "
        "documenting the fraud. Speech bubble (real SMP rep): \"This is "
        "the catheter-billing scheme — we'll file the fraud report.\"\n"
        "Panel 4: Harry returns the unopened box and shreds his old "
        "Medicare statements. Speech bubble (Harry): \"Always check the "
        "Summary Notice.\""
    )),
    ("medicare-and-elder-scams", "scam-3", "medicare-advantage-open-enrollment-pressure", "margie", (
        "Panel 1: Margie at her kitchen counter answers her phone. Speech "
        "bubble (voice from phone): \"Your Medicare plan is changing — "
        "switch today or lose coverage.\"\n"
        "Panel 2: The voice pressures Margie to give her plan ID and "
        "credit card. Speech bubble (voice): \"Just confirm your details "
        "and I'll switch you now.\"\n"
        "Panel 3: Margie hangs up and calls her real plan's customer "
        "service. Speech bubble (real plan rep): \"No agent calls you "
        "first — that was an unsolicited contact, which is illegal.\"\n"
        "Panel 4: Margie reports the call to her State Health Insurance "
        "Assistance Program. Speech bubble (Margie): \"Real Medicare "
        "agents wait for me to call them.\""
    )),
    ("medicare-and-elder-scams", "scam-4", "utility-shutoff-fear-call", "harry", (
        "Panel 1: Harry at his kitchen table answers his phone. Speech "
        "bubble (voice from phone): \"This is the power company — your "
        "service shuts off in 30 minutes if you don't pay.\"\n"
        "Panel 2: The voice demands payment via prepaid debit card. "
        "Speech bubble (voice): \"Buy a $300 card and read me the "
        "number.\"\n"
        "Panel 3: Harry hangs up and calls his utility's customer-service "
        "number from his last paper bill. Speech bubble (real utility "
        "rep): \"Your account is current — we never demand prepaid "
        "cards.\"\n"
        "Panel 4: Harry reports the spoofed call to his utility's fraud "
        "line. Speech bubble (Harry): \"Real utilities mail letters — "
        "they don't threaten 30-minute shutoffs.\""
    )),
    ("medicare-and-elder-scams", "scam-5", "fake-jury-duty-sheriff-call", "margie", (
        "Panel 1: Margie at her kitchen counter answers her phone, the "
        "voice claiming to be a sheriff. Speech bubble (voice): \"You "
        "missed jury duty — there's a warrant for your arrest.\"\n"
        "Panel 2: The voice demands a 'bond payment' via gift card or "
        "wire transfer. Speech bubble (voice): \"Buy $1,500 in cards or "
        "we'll send a deputy.\"\n"
        "Panel 3: Margie hangs up and calls her county courthouse "
        "directly. Speech bubble (real court clerk): \"No warrant — and "
        "no court ever takes gift cards.\"\n"
        "Panel 4: Margie reports the call to the FTC and her state AG "
        "consumer-protection line. Speech bubble (Margie): \"Real "
        "courts use mail, not phones.\""
    )),
    ("medicare-and-elder-scams", "scam-6", "fake-arrest-warrant-mailer", "harry", (
        "Panel 1: Harry at his mailbox holds an official-looking arrest-"
        "warrant letter. Speech bubble (letter): \"WARRANT — call this "
        "number within 24 hours to clear.\"\n"
        "Panel 2: Harry at his kitchen table calls the listed number, the "
        "voice demands $2,800 in gift cards. Speech bubble (voice): "
        "\"Pay now or face arrest.\"\n"
        "Panel 3: Harry hangs up and calls the real court clerk in the "
        "jurisdiction shown on the letter. Speech bubble (real clerk): "
        "\"No such warrant — that's a known scam mailer.\"\n"
        "Panel 4: Harry shreds the letter and files an FTC complaint on "
        "his laptop. Speech bubble (Harry): \"Real warrants come from a "
        "real court, never with a payment hotline.\""
    )),
    # ============================================================
    # PACKAGE-TEXT SCAMS (3 variants)
    # ============================================================
    ("package-text-scams", "scam-1", "usps-redelivery-fee-text", "priya", (
        "Panel 1: Priya on her phone gets a USPS-looking text. Speech "
        "bubble (text): \"Package held for $1.95 redelivery fee — click "
        "to pay.\"\n"
        "Panel 2: Priya pauses, the link is 'usps-redelivery.com' (not a "
        ".gov). Speech bubble (Priya): \"Not a real USPS domain.\"\n"
        "Panel 3: Priya opens the real USPS Informed Delivery app — no "
        "package held. Speech bubble (app): \"No outstanding packages.\"\n"
        "Panel 4: Priya reports the text to 7726 (SPAM) and deletes it. "
        "Speech bubble (Priya): \"USPS uses .gov, never charges $1.95 "
        "fees.\""
    )),
    ("package-text-scams", "scam-2", "fedex-ups-amazon-carrier-clones", "marcus", (
        "Panel 1: Marcus on his phone gets a FedEx-branded text with a "
        "tracking-failure notice. Speech bubble (text): \"FedEx — your "
        "package failed delivery, click to reschedule.\"\n"
        "Panel 2: The link looks like 'fedx-update.net' — Marcus zooms in, "
        "spots the misspelling. Speech bubble (Marcus): \"Missing an E.\"\n"
        "Panel 3: Marcus on the FedEx website (typed manually) checks "
        "tracking — no package in transit. Speech bubble (FedEx site): "
        "\"No packages found.\"\n"
        "Panel 4: Marcus forwards the text to FedEx's abuse address and "
        "reports to 7726. Speech bubble (Marcus): \"Always type the real "
        "domain — never click texted links.\""
    )),
    ("package-text-scams", "scam-3", "address-verification-identity-harvest", "priya", (
        "Panel 1: Priya gets a text claiming Amazon needs to verify her "
        "address. Speech bubble (text): \"Your package can't be "
        "delivered — verify address and last 4 of card.\"\n"
        "Panel 2: The link asks for full name, address, DOB, and last 4 "
        "of credit card. Speech bubble (Priya): \"They never need a card "
        "for an address.\"\n"
        "Panel 3: Priya logs into Amazon directly — no delivery problem "
        "anywhere. Speech bubble (Amazon site): \"All shipments on "
        "schedule.\"\n"
        "Panel 4: Priya reports the link to Amazon's 'stop-spoofing' page "
        "and 7726. Speech bubble (Priya): \"Amazon never asks for card "
        "details over text.\""
    )),
    # ============================================================
    # PIG-BUTCHERING (7 variants)
    # ============================================================
    ("pig-butchering", "scam-1", "hinge-bumble-uncles-trading-signals", "priya", (
        "Panel 1: Priya on her couch swiping Hinge, matches with a "
        "smiling man named 'Daniel.' Speech bubble (chat): \"You're "
        "stunning — let's move to WhatsApp.\"\n"
        "Panel 2: Three weeks later on WhatsApp, Daniel pitches his "
        "uncle's trading platform. Speech bubble (Daniel): \"My uncle's "
        "signals never miss — let me show you.\"\n"
        "Panel 3: Priya searches 'Daniel Lin trader' on her laptop — same "
        "photo on a known pig-butchering scam site. Speech bubble "
        "(Priya): \"Stock photo from a scam database.\"\n"
        "Panel 4: Priya unmatches, blocks, and reports to Hinge + FBI "
        "IC3. Speech bubble (Priya): \"Investment pitches off dating "
        "apps — always a scam.\""
    )),
    ("pig-butchering", "scam-2", "wrong-number-text-crypto-pitch", "harry", (
        "Panel 1: Harry at his kitchen table gets a 'wrong number' text. "
        "Speech bubble (text): \"Hi Linda, dinner Friday at 7?\"\n"
        "Panel 2: Harry replies 'wrong number' — the sender chats back, "
        "two weeks later mentions her crypto trading. Speech bubble "
        "(text): \"My uncle's platform is amazing.\"\n"
        "Panel 3: Harry searches the platform name — known pig-butchering "
        "shell on the FBI IC3 advisory list. Speech bubble (Harry): "
        "\"Pig-butchering script.\"\n"
        "Panel 4: Harry blocks the number, reports to FBI IC3. Speech "
        "bubble (Harry): \"No 'wrong number' leads to a real "
        "friendship.\""
    )),
    ("pig-butchering", "scam-3", "linkedin-mentor-trading-class", "marcus", (
        "Panel 1: Marcus at his desk gets a LinkedIn DM from a 'mentor' "
        "offering a side-hustle trading group. Speech bubble (DM): \"Join "
        "my private trading class — first week free.\"\n"
        "Panel 2: The Telegram group adds him; signals + screenshots show "
        "huge gains. Speech bubble (group admin): \"Deposit $5K to start "
        "— withdraw anytime.\"\n"
        "Panel 3: Marcus checks the trading platform's domain on the FBI "
        "IC3 advisory list — flagged as pig-butchering. Speech bubble "
        "(Marcus): \"On the IC3 list.\"\n"
        "Panel 4: Marcus leaves the group, reports the LinkedIn account, "
        "files an IC3 complaint. Speech bubble (Marcus): \"Real mentors "
        "don't pitch deposits.\""
    )),
    ("pig-butchering", "scam-4", "withdrawal-tax-trap", "harry", (
        "Panel 1: Harry on his laptop sees a $200,000 'profit' on a "
        "trading-platform dashboard. Speech bubble (Harry): \"Time to "
        "cash out.\"\n"
        "Panel 2: A withdrawal request triggers a pop-up: '20% withdrawal "
        "tax due — wire $40,000 to release funds.' Speech bubble (popup): "
        "\"Tax payment required.\"\n"
        "Panel 3: Harry pauses, searches 'withdrawal tax crypto' — top "
        "result is the IC3 pig-butchering advisory. Speech bubble "
        "(Harry): \"That tax is fake.\"\n"
        "Panel 4: Harry on the phone with the FBI IC3 hotline, the "
        "platform locked on his laptop. Speech bubble (Harry): \"No real "
        "platform charges a withdrawal tax.\""
    )),
    ("pig-butchering", "scam-5", "telegram-liquidity-yield-farming", "marcus", (
        "Panel 1: Marcus on his phone in a Telegram channel watches a "
        "'liquidity provider' pitch. Speech bubble (admin): \"Stake your "
        "USDT — 8% daily yield, fully audited.\"\n"
        "Panel 2: Marcus's wallet shows a small test deposit returning "
        "the promised yield, then a banner urges scaling up. Speech "
        "bubble (admin): \"Whale tier opens at $50K.\"\n"
        "Panel 3: Marcus pulls up DeFiLlama and the smart contract — no "
        "audit, owner-controlled. Speech bubble (Marcus): \"No real "
        "audit. Owner can drain it.\"\n"
        "Panel 4: Marcus withdraws the test deposit and posts the "
        "contract address to a public scam-tracker. Speech bubble "
        "(Marcus): \"If the smart contract isn't audited, it's a "
        "rug.\""
    )),
    ("pig-butchering", "scam-6", "spouse-doesnt-know-secret-account", "harry", (
        "Panel 1: Harry at his kitchen table on his laptop, the trading "
        "dashboard hidden behind a different tab. Speech bubble (chat): "
        "\"Don't tell your wife — she'll just worry.\"\n"
        "Panel 2: Harry has wired $80,000 from a hidden account; his "
        "wife is in another room. Caption box: \"The 'secret' framing IS "
        "the scam.\"\n"
        "Panel 3: Harry pauses, closes his laptop, walks into the living "
        "room and sits down with his wife. Speech bubble (Harry): \"I "
        "need to tell you something.\"\n"
        "Panel 4: Harry and his wife together at the kitchen table on "
        "the FBI IC3 victim hotline. Speech bubble (Harry): \"Secrecy is "
        "the diagnostic — every time.\""
    )),
    ("pig-butchering", "scam-7", "recovery-scam-after-public-victim-post", "priya", (
        "Panel 1: Priya at her laptop posts an r/Scams victim story. "
        "Within an hour, three DMs arrive offering 'fund recovery.' "
        "Speech bubble (DM): \"I can recover your funds — 15% upfront "
        "fee.\"\n"
        "Panel 2: Priya reads the next DM, identical wording from a "
        "different account. Speech bubble (Priya): \"Same script.\"\n"
        "Panel 3: Priya screenshots the DMs and posts them to the same "
        "thread as a warning. Speech bubble (post): \"Recovery DMs are "
        "the parasite layer — block them all.\"\n"
        "Panel 4: Priya reports each account to Reddit + IC3, blocks "
        "every recovery DM. Speech bubble (Priya): \"Real recovery is "
        "free — through the FBI, not DMs.\""
    )),
    # ============================================================
    # REAL-ESTATE WIRE FRAUD (3 variants)
    # ============================================================
    ("real-estate-wire-fraud", "scam-1", "last-minute-wire-instruction-swap", "priya", (
        "Panel 1: Priya at her kitchen table reads an email from her "
        "title company on closing day. Speech bubble (email): \"Updated "
        "wire instructions — please use the new account.\"\n"
        "Panel 2: Priya at her bank with the wire form open, the teller "
        "ready to send $300,000. Speech bubble (Priya): \"Wait — let me "
        "verify first.\"\n"
        "Panel 3: Priya calls the title company on the number from her "
        "original signed contract. Speech bubble (real title agent): "
        "\"We didn't send any new instructions — that's a fraud "
        "email.\"\n"
        "Panel 4: Priya wires to the original account and forwards the "
        "fraud email to the title company's IT. Speech bubble (Priya): "
        "\"Always verify on the original number.\""
    )),
    ("real-estate-wire-fraud", "scam-2", "email-editing-mitm", "marcus", (
        "Panel 1: Marcus at his laptop sees an email thread with his "
        "real-estate agent — the account number is different from "
        "yesterday's email. Speech bubble (Marcus): \"This account "
        "changed.\"\n"
        "Panel 2: Marcus's mailbox shows two near-identical 'agent' "
        "emails — one with one extra letter in the domain. Speech bubble "
        "(Marcus): \"Lookalike domain.\"\n"
        "Panel 3: Marcus calls his agent on her cell from his phone "
        "contacts. Speech bubble (real agent): \"My account hasn't "
        "changed — your inbox is being intercepted.\"\n"
        "Panel 4: Marcus on a fresh email account, his old inbox "
        "quarantined, IT working on it. Speech bubble (Marcus): \"Always "
        "verify wire details by phone, never by email reply.\""
    )),
    ("real-estate-wire-fraud", "scam-3", "spoofed-callback-number", "priya", (
        "Panel 1: Priya at her kitchen table calls the 'verify' phone "
        "number printed in the wire-instruction email. Speech bubble "
        "(voice): \"Yes, the new instructions are correct.\"\n"
        "Panel 2: The voice confirms everything — but the number was "
        "spoofed by the same scammer. Caption box: \"Email-listed numbers "
        "can be spoofed.\"\n"
        "Panel 3: Priya hangs up, opens her ORIGINAL signed contract, "
        "and dials the title company's number from page one. Speech "
        "bubble (Priya): \"Use the original document number.\"\n"
        "Panel 4: Priya on the phone with the real title company — fraud "
        "confirmed, original instructions intact. Speech bubble (real "
        "agent): \"Always call the number you had before this email.\""
    )),
    # ============================================================
    # RECOVERY SCAMS (4 variants)
    # ============================================================
    ("recovery-scams", "scam-1", "fund-recovery-specialist-dm", "margie", (
        "Panel 1: Margie at her laptop posts an r/Scams story about "
        "losing $5,000 to a tech-support scam. Within an hour, a DM "
        "arrives. Speech bubble (DM): \"I can recover your funds — 15% "
        "upfront fee.\"\n"
        "Panel 2: The 'specialist' asks for a $750 retainer via "
        "cryptocurrency. Speech bubble (DM): \"Send the retainer to this "
        "wallet to start.\"\n"
        "Panel 3: Margie googles the specialist's name + 'scam' — same "
        "name on the FBI IC3 advisory and r/Scams warning post. Speech "
        "bubble (Margie): \"Recovery scammer.\"\n"
        "Panel 4: Margie blocks the DM and reports to Reddit + IC3. "
        "Speech bubble (Margie): \"Real recovery is free, through the "
        "FBI.\""
    )),
    ("recovery-scams", "scam-2", "blockchain-forensic-crypto-recovery", "marcus", (
        "Panel 1: Marcus at his laptop reads an email from a "
        "'blockchain forensic firm.' Speech bubble (email): \"We can "
        "trace and recover your stolen crypto for a 20% fee.\"\n"
        "Panel 2: The firm asks for $2,500 in advance + Marcus's wallet "
        "private key. Speech bubble (email): \"Send your seed phrase to "
        "begin the trace.\"\n"
        "Panel 3: Marcus checks the firm's name on the SEC + state AG "
        "advisories — flagged as fraudulent. Speech bubble (Marcus): "
        "\"Real forensic firms never ask for your seed phrase.\"\n"
        "Panel 4: Marcus reports the email to FBI IC3 and the SEC. "
        "Speech bubble (Marcus): \"Anyone asking for a seed phrase is "
        "the second scam.\""
    )),
    ("recovery-scams", "scam-3", "fake-law-firm-asset-recovery", "harry", (
        "Panel 1: Harry at his kitchen table reads an unsolicited "
        "letter on letterhead from 'Asset Recovery Counsel.' Speech "
        "bubble (letter): \"We've located your stolen funds — call our "
        "office to claim them.\"\n"
        "Panel 2: A voice on the office line asks for a $3,500 "
        "'court-filing fee' wired to an escrow account. Speech bubble "
        "(voice): \"Standard court fee — refundable on settlement.\"\n"
        "Panel 3: Harry searches the firm on his state bar's "
        "attorney-search tool — no record. Speech bubble (Harry): \"No "
        "such firm.\"\n"
        "Panel 4: Harry forwards the letter to his state bar's consumer "
        "fraud line and the FTC. Speech bubble (Harry): \"Real lawyers "
        "are listed on the state bar.\""
    )),
    ("recovery-scams", "scam-4", "government-recovered-funds-release-fee", "margie", (
        "Panel 1: Margie at her kitchen counter answers her phone, the "
        "voice claiming to be from the FTC. Speech bubble (voice): \"We "
        "recovered your scam funds — pay the $1,200 release fee.\"\n"
        "Panel 2: The voice demands a wire transfer or gift card to "
        "release the funds. Speech bubble (voice): \"Wire the fee — "
        "funds release in 24 hours.\"\n"
        "Panel 3: Margie hangs up and calls the real FTC at "
        "1-877-FTC-HELP. Speech bubble (real FTC rep): \"We never call "
        "you, and we never charge a release fee.\"\n"
        "Panel 4: Margie reports the call to the FTC and her state AG. "
        "Speech bubble (Margie): \"No agency takes fees to release "
        "money.\""
    )),
    # ============================================================
    # TECH-SUPPORT SCAMS (5 variants)
    # ============================================================
    ("tech-support-scams", "scam-1", "browser-popup-windows-locked", "margie", (
        "Panel 1: Margie at her laptop sees a full-screen red Windows-"
        "branded popup with a phone number. Speech bubble (popup): "
        "\"WINDOWS LOCKED — call 1-800-XXX-XXXX immediately.\"\n"
        "Panel 2: Margie reaches for her phone, then pauses. Caption "
        "box: \"No real OS asks you to call a phone number.\"\n"
        "Panel 3: Margie holds the laptop power button to force shutdown, "
        "doesn't dial. Speech bubble (Margie): \"Just turn it off.\"\n"
        "Panel 4: Margie reboots, runs an antivirus scan, the popup "
        "gone. Speech bubble (Margie): \"Real Microsoft never displays a "
        "phone number.\""
    )),
    ("tech-support-scams", "scam-2", "geek-squad-norton-renewal-email", "harry", (
        "Panel 1: Harry at his kitchen table reads an email from 'Geek "
        "Squad' about a $499 auto-renewal. Speech bubble (email): "
        "\"Charge processed — call to dispute.\"\n"
        "Panel 2: The phone agent asks for remote access to 'process the "
        "refund.' Speech bubble (voice): \"Install AnyDesk so I can "
        "refund you.\"\n"
        "Panel 3: Harry hangs up and logs into his actual Best Buy "
        "account — no charge, no subscription. Speech bubble (Harry): "
        "\"No charge anywhere.\"\n"
        "Panel 4: Harry reports the email to Geek Squad's abuse address "
        "and deletes it. Speech bubble (Harry): \"Real refunds never "
        "need remote access.\""
    )),
    ("tech-support-scams", "scam-3", "seo-poisoned-microsoft-support", "margie", (
        "Panel 1: Margie at her laptop searches 'Microsoft support phone' "
        "and clicks the top result. Speech bubble (search result): "
        "\"Microsoft 24/7 Help — 1-800-XXX-XXXX.\"\n"
        "Panel 2: A voice on the line asks Margie to install "
        "ConnectWise to 'verify her account.' Speech bubble (voice): "
        "\"Install this app so I can check your computer.\"\n"
        "Panel 3: Margie pauses, types support.microsoft.com directly "
        "into her browser. Speech bubble (Margie): \"Type the real "
        "domain.\"\n"
        "Panel 4: Margie on Microsoft's actual support chat, the "
        "scammer's call dropped. Speech bubble (real Microsoft agent): "
        "\"Microsoft support never calls you, and we never need remote "
        "access.\""
    )),
    ("tech-support-scams", "scam-4", "remote-access-installation", "harry", (
        "Panel 1: Harry on the phone at his kitchen table, the voice "
        "guiding him to install AnyDesk on his laptop. Speech bubble "
        "(voice): \"Type 'AnyDesk' and install it now.\"\n"
        "Panel 2: Harry's screen shows the AnyDesk download page, his "
        "cursor hovering over INSTALL. Speech bubble (Harry): \"Why do "
        "they need to see my screen?\"\n"
        "Panel 3: Harry hangs up, closes the browser tab, doesn't "
        "install. Speech bubble (Harry): \"Never install for a "
        "stranger.\"\n"
        "Panel 4: Harry on a video call with his real bank's fraud "
        "line. Speech bubble (real bank rep): \"AnyDesk + a stranger = "
        "always a scam.\""
    )),
    ("tech-support-scams", "scam-5", "bank-drain-via-remote-controlled-browser", "margie", (
        "Panel 1: Margie at her laptop, the scammer remote-controlling "
        "her browser to log into her bank. Speech bubble (voice): \"Just "
        "let me verify the balance.\"\n"
        "Panel 2: The cursor moves on its own, drafting a $9,800 "
        "outbound transfer. Speech bubble (Margie): \"Why is it making "
        "transfers?\"\n"
        "Panel 3: Margie unplugs her laptop power and Wi-Fi, terminating "
        "the session. Speech bubble (Margie): \"Off — now.\"\n"
        "Panel 4: Margie at her bank in person, the teller freezing the "
        "account. Speech bubble (real teller): \"You stopped it — we'll "
        "reverse the transfer.\""
    )),
]

assert len(MANIFEST) == 51, f"Expected 51 entries, got {len(MANIFEST)}"
