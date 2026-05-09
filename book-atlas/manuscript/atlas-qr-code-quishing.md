# Q · QR Code Quishing

> **Pattern: Brand-Mimicry Storefront** · 4 mechanics · 12 countries · 300–4,000 USD per harvest · *Updated April 2026*

<!-- comic-insert -->
![Comic illustration of Qr Code Quishing](../build/images/atlas-qr-code-quishing.jpg){ width=100% }

## The sticker

Marcus stood in front of the BVG ticket kiosk at U-Bahnhof
Alexanderplatz at three on a Friday afternoon, four days into a
Berlin coworking residency. The kiosk had a printed QR code on its
front face under SCAN TO BUY YOUR TICKET. He held up his phone and
scanned.

The URL preview banner appeared at the top of the screen for half
a second. He missed it. He tapped the banner. A page styled
identically to the BVG payment flow loaded: same blue header, same
logo, same fonts. He selected a single-ride ticket, entered card
number, expiration, CVV, and German postal code. Confirmation page:
*Ticket gültig*. He boarded the U2 toward Pankow.

That night his Chase Sapphire Reserve issuer phoned him from
Wilmington. The card had been used at four merchants in Bucharest
for a total of 3,400 US dollars on premium-rate digital
subscriptions and gift-card purchases. The card was canceled.

Marcus walked back to Alexanderplatz the next morning. The QR
sticker on the kiosk peeled off cleanly with a fingernail.
Underneath was the genuine BVG QR. The sticker on top had loaded
*bvg-tickets.de* (one hyphen and a different top-level domain from
the genuine *bvg.de*) which captured the card and dispensed the
genuine BVG payment from the stolen card so the ticket actually
worked.

## The trick

QR-code phishing, or *quishing*, is the modern Brand-Mimicry
Storefront variant. The QR sticker is glued over the legitimate
one on a parking meter, transit kiosk, restaurant table-tent, or
rental-car windshield. The fake page styles itself identically to
the legitimate payment flow. The URL is the only tell. Phishing
crews print rolls of QR stickers with lookalike domains
(*bvg-tickets.de* instead of *bvg.de*, *paybyfone.fr* instead of
*paybyphone.fr*, *tfl-tickets.uk* instead of *tfl.gov.uk*) and
apply them in the early morning before the city wakes up.

The harvested card data is sold to a clearinghouse within minutes
and used at offshore merchants within six to twenty-four hours.
The legitimate payment is sometimes dispatched from the harvested
card so the actual service (parking, transit, restaurant) functions
and the tourist does not notice the breach until the credit-card
statement arrives weeks later.

The defense is two rules.

The URL-preview rule: read the URL preview banner before tapping.
Modern phones display the URL for about half a second after the
QR scan. The banner is the only signal that distinguishes
legitimate domains from lookalikes. Pause, read the URL, then tap
or cancel. The five-second routine eliminates every variant.

The official-app rule: pay through official city or chain apps
instead of QR codes whenever possible. The BVG app, the
PayByPhone app, the TfL Pay app, the OPAL app: these cannot be
quished because the URL never changes. Apps remove the
sticker-overlay attack surface, though apps have their own attack
vectors (rogue Wi-Fi, lookalike app-store listings) that the URL-
preview rule does not address.

The defense in depth is the sticker-tampering check. Glued-on
overlays have raised edges or air bubbles. Printed-on QRs are
flush with the surface. A fingernail catches an overlay; nothing
catches a print. A ten-second visual inspection of any QR before
a sticker check catches the majority of variants.

## The four mechanics

**Parking-meter overlay.** The most-documented variant globally. A
phishing crew applies a sticker over the meter's genuine QR with a
typo-domain (*paybyfone.fr* instead of *paybyphone.fr*;
*parkrightnow.com* instead of *parkmobile.us*). The fake page
captures card data and dispenses the legitimate parking payment so
the meter shows valid time. Most reported in Paris (Avenue
Montaigne, Rue du Faubourg Saint-Honoré, Champs-Élysées), Berlin
(Mitte, Charlottenburg), London (West End, Soho), San Francisco
(Union Square, the Marina), New York (SoHo, Tribeca). Closing
loss: 1,000–4,000 USD per harvest.

**Transit-kiosk spoof.** Stickers applied to U-Bahn, Metro,
Underground, or bus kiosks at high-traffic stations. The fake site
styles itself like the city's transit operator and harvests card
data the same way. Most reported at Berlin Alexanderplatz and
Hauptbahnhof, Paris Châtelet–Les Halles and Gare du Nord, London
Oxford Circus and Victoria, NYC Times Square 42nd, San Francisco
Powell. Closing loss: 300–2,000 USD per harvest.

**Restaurant menu QR.** A fake table-tent placed on the table or
stuck inside the menu cover. The fake page styles itself like the
restaurant's online ordering or payment flow and harvests card data
when the diner pays the bill or orders. Most reported in Italian
tourist-zone trattorie (Rome Trastevere, Florence Duomo), Spanish
tapas bars (Barcelona Eixample), French cafés. Sometimes paired
with bill-padding at the same table.

**Fake-fine windshield slip.** A printed slip placed on the
rental-car windshield claiming a parking fine, with a QR code to
"pay online to avoid additional charges." The fake site styles
itself like the city's traffic-violation portal. Most reported in
Italian historic centers (ZTL fine cascades), Spanish historic
centers, German low-emission zones. The actual fine often does not
exist. Closing loss: 80–400 USD per harvest plus card-data exposure.

## Where it runs (12 countries, Western Europe dominant)

Quishing concentrates in cities with two conditions: high
QR-payment penetration in public infrastructure and weak
sticker-tampering enforcement on shared assets (parking meters,
transit kiosks, public table-tents). France, Germany, the UK,
Italy, Spain, the Netherlands, the USA, Canada, Australia,
Singapore, Japan, and the UAE account for the bulk of documented
variants.

Western Europe dominates because public-infrastructure QR rollout
outpaced anti-tampering controls during 2022–2024. The 2025 EU
Cyber Resilience Act explicitly addresses this attack vector but
enforcement is still uneven. Singapore and Tokyo run smaller-volume
variants because public-infrastructure QR codes there are typically
engraved or printed in tamper-evident enclosures.

You will see less of this in cities where QR payment is rare (most
of Latin America, sub-Saharan Africa, parts of Eastern Europe). The
pattern requires the QR-payment infrastructure to exist before it
can be subverted.

## The five red flags

Any one of these before you tap the URL banner: cancel and use the
official app.

- **A QR sticker with raised edges, peeling corners, or air
  bubbles.** Genuine QRs are printed flush with the surface or
  engraved. Tampered overlays catch a fingernail.
- **A URL with a hyphen, an unusual top-level domain (.org, .info,
  .biz, .uk-tickets), or a typo of the official site.** Memorize
  the canonical domain for any city where you will pay by QR
  (*paybyphone.fr*, *bvg.de*, *tfl.gov.uk*, *parkmobile.us*).
- **A URL shortener (bit.ly, tinyurl, t.ly) at the URL preview
  banner.** Real public-infrastructure QRs use the official long
  URL. Shorteners hide the destination.
- **A printed slip on your rental-car windshield claiming a fine.**
  Real fines are issued by local police or municipal authorities
  through the rental-car company, not by paper QR slips.
- **A table-tent QR with no restaurant logo, generic font, or
  fresh adhesive.** Legitimate restaurant table-tents carry the
  venue's branding and are typically printed in volume.

## The phrases that shut it down

The quishing defense is non-verbal: read the URL, do not tap. These
phrases handle the in-person variant where staff direct you to the
QR.

| Language | Phrase | Translation |
|---|---|---|
| English | "I'd rather pay through the app, thanks." |  |
| French | *Je préfère payer par l'application, merci.* | I'd rather pay through the app, thanks. |
| German | *Ich zahle lieber über die App, danke.* | I'd rather pay through the app, thanks. |
| Italian | *Preferisco pagare tramite l'app, grazie.* | I'd rather pay through the app, thanks. |
| Spanish | *Prefiero pagar con la aplicación, gracias.* | I'd rather pay through the app, thanks. |

If the venue insists on the QR and has no app alternative, walk to
the next venue. The QR-only payment model with no backup channel
is itself a yellow flag.

## If this happens to you

You entered card data on a phishing page. Within hours your card
is being run online. Recovery depends on speed.

Within five minutes: phone your card issuer's twenty-four-hour
fraud line. Most US issuers have a number on the back of every
card. Save photos of every card back separately on your phone for
exactly this moment. Report the charge as fraud, not as a
merchant dispute. Visa, Mastercard, and Amex all have fraud-dispute paths;
well-documented fraud disputes typically resolve in twenty to
forty-five days.

Within thirty minutes: enable instant card-fraud alerts in your
bank app. The clone-to-first-fraud window is six to twenty-four
hours; instant alerts close the window in seconds. Set alerts for
any transaction above five US dollars while traveling.

Within sixty minutes: change passwords on any accounts that share
the harvested email or use the same card on file. Fraud crews
sometimes test the harvested card across linked accounts (Apple
ID, Google, Amazon, Spotify) to extract additional card-on-file
value.

For the parking-meter or transit-kiosk overlay specifically:
photograph the tampered sticker (peel back a corner if safe to do
so) and the underlying genuine QR. Report the location to the
city's transit authority via email or in-app form. Berlin BVG
(kundendialog@bvg.de), Paris Mairie (paris.fr/signal), London TfL
(tfl.gov.uk/help), San Francisco MTA. The cities maintain
enforcement registers and the photo accelerates removal at that
location.

For travel-insurance claims: card-fraud alone is typically not
covered (issuers handle reimbursement). Time-loss and
account-recovery hours are not covered. The actionable response
is preventive for future trips.

Marcus got the 3,400 US dollars back from Chase. The chargeback
succeeded eighteen days later under fraud. He spent two evenings of
his Berlin residency on the phone with Chase from a coworking-space
booth on Rosenthaler Straße. He did not scan another public QR for
the rest of the trip; he installed the BVG app and the PayByPhone
app on his phone instead. On future trips, he checked the URL
preview banner on every QR scan and reported tampered stickers to
the local transit authority within an hour of seeing them.

---

*For city-by-city playbooks, see **France: Tourist Scams** (Paris
Avenue Montaigne and Champs-Élysées parking-meter quishing),
**Germany: Tourist Scams** (Berlin Alexanderplatz transit-kiosk and
Mitte parking-meter), **United Kingdom: Tourist Scams** (London
West End parking-meter and Oxford Circus transit-kiosk), **Italy:
Tourist Scams** (Rome and Florence restaurant table-tent QRs), and
**Spain: Tourist Scams** (Barcelona Eixample restaurant table-tent
QRs).*
