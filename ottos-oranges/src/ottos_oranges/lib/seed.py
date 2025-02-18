orange_farms_csv = """
Farm ID;Farm Name;Farm Location;Farm Owner
1;Orlando's Own Oranges; Orlando, FL;orlando@ottosoranges.com
2;Tampa's Tempting Oranges;Tampa, FL;boat@ottosoranges.com
3;Land O' Lakes and Oranges Oranges;Land O' Lakes, FL;welikebutter@ottosoranges.com
""".strip()

orange_warehouses_csv = """
Warehouse ID;Warehouse Name;Warehouse Location;Warehouse Owner
1;warehouseA;Las Vegas, NV;otto@ottosoranges.com
2;warehouseB;Palo Alto, CA;alice@ottosoranges.com
3;warehouseC;Seattle, WA;bob@ottosoranges.com
4;warehouseD;Orlando, FL;steve@ottosoranges.com
5;warehouseE;New York, NY;steve2@ottosoranges.com
""".strip()

orange_stores_csv = """
Store ID|Store Name|Store Location|Store Owner
0|website|Internet|support@ottosoranges.com
1|Otto's Oranges (classic)|Las Vegas, NV|otto@ottosoranges.com
2|Otto's Oranges (original)|Palo Alto, CA|naes@ottosoranges.com
3|Coffee But It's Orange Juice|Seattle, WA|zebos@ottosoranges.com
4|Orlando's Orange Juice|Orlando, FL|orlando@ottosoranges.com
5|Oranges in the Big Apple|New York, NY|star@ottosoranges.com
""".strip()

orange_types_csv = """
Orange SKU,Description
VAL001,Valencia Sun Burst - Sweet and exceptionally juicy
MID002,Midnight Blood - Deep crimson flesh with notes of raspberry
FRO003,Frost Crystal - Naturally frosted appearance winter-hardy
GOL004,Golden Honeydew - Honey-sweet with pale yellow flesh
DRA005,Dragon's Breath - Spicy undertones with a fiery orange rind
MAN006,Mandarin Moon - Small intensely sweet nighttime harvester
STA007,Starlight Navel - Translucent flesh with stellar patterns
THU008,Thunder Cloud - Dark purple-tinged skin storm-resistant
DES009,Desert Rose - Drought-resistant with subtle floral notes
ARC010,Arctic Flame - Cold-resistant with warming citrus oils
TEM011,Temple Guardian - Ancient variety with thick protective rind
SUN012,Sunrise Burst - Pink-tinted flesh best harvested at dawn
OCE013,Ocean Mist - Subtle saltwater notes coastal growing
MOU014,Mountain Peak - High-altitude variety with dense flesh
TWI015,Twilight Tango - Dark purple skin with dancing gold streaks
RAI016,Rainbow Heart - Multi-colored segments within
CEL017,Celestial Sweet - Star-shaped segment pattern
EME018,Emerald Dream - Green-tinted flesh with classic flavor
RUB019,Ruby Cascade - Waterfall pattern on skin
MOO020,Moonlight Whisper - Pale white flesh nocturnal bloomer
FOR021,Forest Shadow - Dark green skin with woodland notes
CRY022,Crystal Kiss - Transparent segments with rainbow effect
PHO023,Golden Phoenix - Rises from winter frost damage
SIL024,Silver Lining - Metallic sheen on skin
AUT025,Autumn Ember - Fall harvesting with warm spice notes
SPR026,Spring Sentinel - Early season guardian variety
SUM027,Summer Storm - Heat-resistant with electric tang
WIN028,Winter Wish - Late season with frost resistance
MYS029,Mystic Morning - Changes flavor throughout the day
SSE030,Sunset Serenade - Evening-harvested for sweetness
CLO031,Cloud Walker - Extremely light and fluffy segments
EAR032,Earth Mother - Rich soil-influenced flavors
FIR033,Fire Dancer - Spicy-sweet with warming effect
WAT034,Water Weaver - Extra juicy with flowing patterns
AIR035,Air Whisper - Light airy texture
TIM036,Time Keeper - Long-lasting shelf life
SPA037,Space Drifter - Zero-gravity developed variety
DRE038,Dream Weaver - Calming aromatics
SOU039,Soul Singer - Harmonious flavor balance
HEA040,Heart Healer - Wellness-promoting variety
MIN041,Mind Reader - Cognitive-enhancing compounds
SPI042,Spirit Walker - Ancient medicinal variety
GAL043,Galaxy Guardian - Cosmic-inspired patterns
UNI044,Universe Unifier - Universal growing conditions
DIM045,Dimension Dancer - Shape-shifting appearance
REA046,Reality Ripple - Perception-altering aromatics
TRU047,Truth Teller - Clarity-promoting essence
WIS048,Wisdom Whisperer - Age-old variety
MEM049,Memory Maker - Unforgettable flavor
FUT050,Future Forger - Lab-developed hybrid
PAS051,Past Preserver - Heritage variety
PRE052,Present Perfect - Ideal balance of traits
INF053,Infinity Insight - Never-ending flavor development
ETE054,Eternal Echo - Long-lasting aftertaste
TEM055,Temporal Tang - Time-release flavor
SPA056,Spatial Sweet - Space-efficient growing
QUA057,Quantum Quick - Rapid-growing variety
COS058,Cosmic Crunch - Extra-crisp texture
SOL059,Solar Flare - Sun-loving variety
LUN060,Lunar Light - Moonlight-enhanced growing
STE061,Stellar Storm - Star-pattern skin
NEB062,Nebula Nectar - Cloud-like texture
BLA063,Black Hole - Ultra-dark flesh
MET064,Meteor Might - Impact-resistant skin
COM065,Comet Tail - Streaked skin pattern
AST066,Asteroid Belt - Ring-patterned segments
JUP067,Jupiter Jump - Giant variety
MAR068,Mars Morning - Red-tinted flesh
VEN069,Venus Veil - Misty skin appearance
MER070,Mercury Rise - Quick-ripening variety
SAT071,Saturn Ring - Circular growth pattern
NEP072,Neptune Night - Deep blue-tinted skin
URA073,Uranus Unity - Universal growing success
PLU074,Pluto Pride - Small but mighty variety
MIL075,Milky Way - Cream-colored flesh
AND076,Andromeda Autumn - Fall variety
ORI077,Orion's Belt - Triple-layered flesh
PHF078,Phoenix Fire - Self-healing tree variety
DRS079,Dragon Scale - Textured skin
UNI080,Unicorn Horn - Spiral-growing fruit
MER081,Mermaid Mist - Coastal variety
PEG082,Pegasus Pride - Flying fruit pattern
GRI083,Griffin Guard - Protective thick skin
SPH084,Sphinx Secret - Ancient Egyptian variety
CHI085,Chimera Change - Multi-characteristic fruit
HYD086,Hydra Head - Multiple fruit clusters
CER087,Cerberus Guard - Triple-sweet segments
MED088,Medusa Memory - Stone-resistant variety
CYC089,Cyclops Sight - Single-segment mutation
MIN090,Minotaur Maze - Complex internal patterns
CEN091,Centaur Charge - Racing stripe pattern
SIR092,Siren Song - Aromatic variety
HAR093,Harpy Heart - Wind-resistant type
KRA094,Kraken Deep - Ocean-depth colored
LEV095,Leviathan Length - Extra-long fruit
BAS096,Basilisk Breath - Snake-pattern skin
PHX097,Phoenix Flight - High-growing variety
TIT098,Titan Touch - Giant tree variety
ATL099,Atlas Arms - Strong-branched tree
OLY100,Olympian Crown - Peak performance variety
ANG101,Angel's Kiss - Heavenly sweet with golden glow
DEV102,Devil's Dance - Spicy-hot with deep red flesh
FAE103,Fairy Flight - Miniature with sparkle skin
WIZ104,Wizard Ward - Magic-inspired growing pattern
DRU105,Druid Dream - Nature-enhanced variety
SHA106,Shaman Share - Traditional healing variety
MON107,Monk's Morning - Meditation-enhancing type
PAL108,Paladin's Pride - Noble variety with golden core
BAR109,Bard's Beauty - Song-inspired growing pattern
RAN110,Ranger's Rest - Forest-dwelling variety
WAR111,Warrior's Watch - Protective rind type
ROG112,Rogue's Relief - Quick-growing stealth variety
CLE113,Cleric's Care - Blessing-enhanced growth
""".strip()
