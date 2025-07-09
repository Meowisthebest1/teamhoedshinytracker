
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

TIER_POINTS = {
    "Tier 6": 2,
    "Tier 5": 3,
    "Tier 4": 6,
    "Tier 3": 10,
    "Tier 2": 15,
    "Tier 1": 25,
    "Tier 0": 30
}

LEGENDARIES = ["Articuno", "Moltres", "Zapdos", "Entei", "Raikou", "Suicune", "Heatran"]
tier_pokemon = {
  "Tier 6": [
    "Abra",
    "Aron",
    "Baltoy",
    "Basculin [Red-Striped Form]",
    "Bidoof",
    "Blitzle",
    "Bouffalant",
    "Bronzor",
    "Buizel",
    "Chinchou",
    "Clamperl",
    "Cubchoo",
    "Cubone",
    "Deerling",
    "Diglett",
    "Drowzee",
    "Druddigon",
    "Dunsparce",
    "Durant",
    "Duskull",
    "Dwebble",
    "Elgyem",
    "Foongus",
    "Frillish",
    "Gastly",
    "Geodude",
    "Goldeen",
    "Golett",
    "Gothita",
    "Grimer",
    "Heatmor",
    "Hoppip",
    "Horsea",
    "Jigglypuff",
    "Jynx",
    "Koffing",
    "Krabby",
    "Lickitung",
    "Lillipup",
    "Litwick",
    "Lotad",
    "Lunatone",
    "Machop",
    "Magikarp",
    "Magnemite",
    "Makuhita",
    "Mantine",
    "Marill",
    "Meowth",
    "Mienfoo",
    "Nidoran\u2640",
    "Nidoran\u2642",
    "Numel",
    "Oddish",
    "Onix",
    "Paras",
    "Patrat",
    "Pidgey",
    "Pidove",
    "Pikachu",
    "Poliwag",
    "Ponyta",
    "Poochyena",
    "Psyduck",
    "Purrloin",
    "Rattata",
    "Rhyhorn",
    "Roggenrola",
    "Roselia",
    "Sandile",
    "Sandshrew",
    "Seel",
    "Sewaddle",
    "Shellos",
    "Shelmet",
    "Shuppet",
    "Slowpoke",
    "Slugma",
    "Smeargle",
    "Sneasel",
    "Snover",
    "Solosis",
    "Solrock",
    "Spearow",
    "Spheal",
    "Stunfisk",
    "Surskit",
    "Swablu",
    "Swinub",
    "Taillow",
    "Tangela",
    "Tentacool",
    "Timburr",
    "Torkoal",
    "Tympole",
    "Voltorb",
    "Whismur",
    "Wingull",
    "Wobbuffet",
    "Woobat",
    "Wooper",
    "Yamask",
    "Zigzagoon",
    "Zubat"
  ],
  "Tier 5": [
    "Axew",
    "Caterpie",
    "Deino",
    "Delibird",
    "Ditto",
    "Doduo",
    "Ekans",
    "Electrike",
    "Ferroseed",
    "Gible",
    "Girafarig",
    "Glameow",
    "Gligar",
    "Growlithe",
    "Hoothoot",
    "Joltik",
    "Klink",
    "Kricketot",
    "Mankey",
    "Mareep",
    "Mawile",
    "Meditite",
    "Natu",
    "Phanpy",
    "Rufflet",
    "Sableye",
    "Scraggy",
    "Seedot",
    "Shinx",
    "Snorunt",
    "Spinarak",
    "Teddiursa",
    "Vanillite",
    "Vullaby",
    "Vulpix",
    "Weedle"
  ],
  "Tier 4": [
    "Bellsprout",
    "Buneary",
    "Chimecho",
    "Clefairy",
    "Cottonee",
    "Darumaka",
    "Dratini",
    "Drifloon",
    "Electabuzz",
    "Hippopotas",
    "Karrablast",
    "Larvitar",
    "Ledyba",
    "Magmar",
    "Miltank",
    "Minccino",
    "Misdreavus",
    "Murkrow",
    "Nosepass",
    "Pachirisu",
    "Petilil",
    "Sawk",
    "Snubbull",
    "Spinda",
    "Spoink",
    "Stantler",
    "Starly",
    "Stunky",
    "Sunkern",
    "Tauros",
    "Throh",
    "Trapinch",
    "Trubbish",
    "Tynamo",
    "Venipede",
    "Venonat",
    "Wurmple"
  ],
  "Tier 3": [
    "Bagon",
    "Barboach",
    "Cacnea",
    "Carvanha",
    "Chatot",
    "Corphish",
    "Corsola",
    "Cryogonal",
    "Finneon",
    "Houndour",
    "Illumise",
    "Luvdisc",
    "Maractus",
    "Munna",
    "Nincada",
    "Pawniard",
    "Ralts",
    "Remoraid",
    "Sentret",
    "Seviper",
    "Shellder",
    "Sigilyph",
    "Staryu",
    "Unown",
    "Volbeat",
    "Wailmer",
    "Zangoose"
  ],
  "Tier 2": [
    "Aerodactyl",
    "Aipom",
    "Anorith",
    "Archen",
    "Combee",
    "Cranidos",
    "Croagunk",
    "Exeggcute",
    "Farfetch'd",
    "Gulpin",
    "Heracross",
    "Kabuto",
    "Kangaskhan",
    "Lapras",
    "Lileep",
    "Minun",
    "Mr. Mime",
    "Omanyte",
    "Pineco",
    "Plusle",
    "Qwilfish",
    "Relicanth",
    "Shieldon",
    "Shroomish",
    "Shuckle",
    "Tirtouga",
    "Tropius",
    "Yanma"
  ],
  "Tier 1": [
    "Absol",
    "Beldum",
    "Burmy",
    "Carnivine",
    "Castform",
    "Chansey",
    "Cherubi",
    "Eevee",
    "Feebas",
    "Kecleon",
    "Larvesta",
    "Panpour",
    "Pansage",
    "Pansear",
    "Pinsir",
    "Scyther",
    "Skarmory",
    "Skitty",
    "Skorupi",
    "Slakoth",
    "Snorlax",
    "Sudowoodo",
    "Zorua"
  ],
  "Tier 0": [
    "Alomomola",
    "Audino",
    "Basculin [Blue-Striped Form]",
    "Bulbasaur",
    "Charmander",
    "Chikorita",
    "Chimchar",
    "Cyndaquil",
    "Drilbur",
    "Ducklett",
    "Emolga",
    "Mudkip",
    "Oshawott",
    "Piplup",
    "Porygon",
    "Riolu",
    "Rotom",
    "Shedinja",
    "Snivy",
    "Spiritomb",
    "Squirtle",
    "Tepig",
    "Togepi",
    "Torchic",
    "Totodile",
    "Treecko",
    "Turtwig",
    "Tyrogue"
  ]
}
usernames = [
  "Akshit",
  "Anax",
  "Burly",
  "Cowdoy",
  "Default",
  "Dislikable",
  "dwrecklus",
  "Entitled",
  "Eziroh",
  "Inori",
  "Iuigi",
  "Karp",
  "KimSuhanmu",
  "Minish",
  "nieljuliaaan",
  "Pancham",
  "Papysan",
  "PokeVoon",
  "Proh",
  "Raddiction",
  "Reversed",
  "Roach",
  "Samuel",
  "Shaco",
  "Slip",
  "TheMagicalOne",
  "Thricee",
  "Tien",
  "Tuna",
  "Versatile"
]

conn = sqlite3.connect("shiny_tracker.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shiny_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        pokemon TEXT,
        tier TEXT,
        alpha INTEGER,
        legendary INTEGER,
        secret INTEGER,
        safari INTEGER,
        egg INTEGER,
        points INTEGER,
        timestamp TEXT
    )
""")
conn.commit()

def get_base_name(name):
    return name.lower().split()[0]

def is_duplicate(username, pokemon):
    base = get_base_name(pokemon)
    df = pd.read_sql_query("SELECT pokemon FROM shiny_log WHERE username = ?", conn, params=(username,))
    user_species = [get_base_name(p) for p in df["pokemon"]]
    return user_species.count(base) > 0

def is_unique_species(pokemon):
    base = get_base_name(pokemon)
    df = pd.read_sql_query("SELECT pokemon FROM shiny_log", conn)
    species = [get_base_name(p) for p in df["pokemon"]]
    return base not in species

st.title("🐲 Team Horde Shiny Tracker")

st.header("🔘 Log a New Shiny Pokémon")
username = st.selectbox("Choose your username", usernames)
selected_tier = st.selectbox("Select Tier", list(tier_pokemon.keys()))

caught_pokemon = set(pd.read_sql_query("SELECT pokemon FROM shiny_log", conn)["pokemon"].tolist())
dropdown_options = []
option_map = {}

for p in sorted(tier_pokemon[selected_tier]):
    label = f"{p} (Caught)" if p in caught_pokemon else p
    dropdown_options.append(label)
    option_map[label] = p

selected_label = st.selectbox("Select Pokémon", dropdown_options)
selected_pokemon = option_map[selected_label]


alpha = st.checkbox("Alpha Shiny (50 pts)", value=False)
legendary = st.checkbox("Legendary/Mythical (100 pts)", value=False)
secret = st.checkbox("Secret Shiny (+10 pts)", value=False)
safari = st.checkbox("Safari Catch (+5 pts)", value=False)
egg = st.checkbox("Egg Hatch (20 pts or Tier)", value=False)

if st.button("✅ Mark as Caught"):
    tier_points = TIER_POINTS[selected_tier]
    base = get_base_name(selected_pokemon)

    if legendary or selected_pokemon in LEGENDARIES:
        points = 100
    elif alpha:
        points = 50
    elif egg:
        points = max(20, tier_points)
    else:
        points = tier_points

    if is_duplicate(username, selected_pokemon):
        points = 1 if not alpha else 25

    if is_unique_species(selected_pokemon):
        points += 5

    if secret:
        points += 10
    if safari:
        points += 5

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO shiny_log (username, pokemon, tier, alpha, legendary, secret, safari, egg, points, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, selected_pokemon, selected_tier, int(alpha), int(legendary), int(secret), int(safari), int(egg), points, timestamp))
    conn.commit()
    st.success(f"🎉 {selected_pokemon} logged for {username} — {points} points!")

st.header("❌ Delete a Shiny Entry")
del_user = st.selectbox("Select Username to Remove From", usernames, key="delete_user")
del_df = pd.read_sql_query("SELECT pokemon FROM shiny_log WHERE username = ?", conn, params=(del_user,))
del_list = sorted(set(del_df['pokemon'].tolist()))
if del_list:
    del_pokemon = st.selectbox("Select Pokémon to Delete", del_list)
    if st.button("🗑️ Delete Entry"):
        cursor.execute("DELETE FROM shiny_log WHERE username = ? AND pokemon = ?", (del_user, del_pokemon))
        conn.commit()
        st.success(f"🗑️ Deleted {del_pokemon} from {del_user}'s log.")

st.header("🏆 Live Scoreboard")
score_df = pd.read_sql_query("SELECT username, SUM(points) as total_points FROM shiny_log GROUP BY username ORDER BY total_points DESC", conn)
st.dataframe(score_df)

st.header("📜 Full Shiny Log")
log_df = pd.read_sql_query("SELECT * FROM shiny_log ORDER BY timestamp DESC", conn)
st.dataframe(log_df)

if st.button("📥 Export Excel Log"):
    log_df.to_excel("shiny_log_export.xlsx", index=False)
    st.success("✅ Log saved as shiny_log_export.xlsx")
