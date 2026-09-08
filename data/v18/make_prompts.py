# -*- coding: utf-8 -*-
"""V18 gorsel prompt'lari.

Merkezde ODA var: roportaj odasi ve icindeki sandalye duzeni. Sekiz sahne
1959'dan 2003'e ayni mesleki duzenin farkli anlarini gosteriyor.

KAPAK — 8 Eyl CTR teshisinden sonra degisen kurallar:
  * V10-V16'nin yedisi de tek basina sakin bir yuzdu; kapaklar birbirinden
    ayirt edilemiyordu. Bu kapak IKI KISILI ve kompozisyonun kendisi
    hikayeyi anlatiyor (onde konusan kadin, arkada sessiz cevirmen).
  * Doygunluk olculdu: yedi kapagin altisi 15'in altindaydi (neredeyse gri).
    Bu yuzden prompt acikca doygun renk istiyor.
  * Sahne "dusk" — "night" modeli karanliga cekiyor (V16'da olculdu).
  * Yuz kadredeki en parlak oge; arkada yuzden parlak lamba/pencere yok.
"""
import json, os

STYLE = ("Cinematic film still, black and white 35mm photography, single strong "
         "practical light source, deep chiaroscuro shadows, strong compositional "
         "depth and leading lines, foreground bokeh, shallow depth of field, fine "
         "film grain, painterly photorealism, 16:9")

ROOM = ("an over-furnished Roman hotel room used for press interviews, heavy curtains, "
        "a low table, two armchairs facing each other and a third plain chair set "
        "slightly behind and to the left of one of them")

S = {}

S["1"] = (f"Interior of {ROOM} in 1959, seen from the doorway. A woman in her thirties in a "
          f"plain suit sits in the plain chair with a notebook closed on her knee, composed "
          f"and entirely still, while two other people talk in the armchairs, both blurred "
          f"and cut by the frame. She is the only sharp thing in the picture. {STYLE}")

S["2"] = (f"A small Roman apartment kitchen at night in the 1960s: a woman alone at a table "
          f"under one hanging bulb, eating, a stack of dictionaries and reference books "
          f"pushed to one side of the table and a closed ledger in front of her. Shelves of "
          f"books in four languages behind. Nobody else. Seen slightly from above. {STYLE}")

S["3"] = (f"Very close on a woman's hands resting flat and motionless on a closed notebook in "
          f"her lap, in a lit room, with the blurred shapes of two seated people and a "
          f"microphone beyond her. Absolute stillness in the hands. The rest of the room "
          f"falls out of focus. No faces visible. {STYLE}")

S["4"] = (f"Interior of {ROOM} in the early 1970s, shot from behind the plain chair over the "
          f"interpreter's shoulder: her head and shoulder dark in the near foreground, and "
          f"beyond her a slender woman in an armchair mid-sentence, lit and in focus, "
          f"turned three-quarters away toward an unseen journalist. {STYLE}")

S["5"] = (f"A hotel room at the top of a building on a wide avenue in 1981, late afternoon: a "
          f"young man of about twenty-six leaning forward in an armchair holding a folded "
          f"list of typed questions, earnest and slightly out of his depth, a tape recorder "
          f"running on the table between him and an empty chair. Window light from behind "
          f"him. {STYLE}")

S["6"] = (f"Extreme close-up of a woman's mouth and jaw mid-word in profile, sharply lit from "
          f"one side, everything else in the room reduced to darkness and one soft highlight. "
          f"The image is about the act of speaking and nothing else. No eyes in frame. "
          f"{STYLE}")

S["7"] = (f"Interior of {ROOM}, the interview over: a journalist's back retreating through a "
          f"door at the far end, and in the middle distance two women left alone in the room, "
          f"not looking at each other, one still seated in an armchair and one standing "
          f"beside the plain chair with a bag in her hand. A held moment. {STYLE}")

S["8"] = (f"A cleared-out Roman flat in 2003 lit by bare afternoon light through an uncurtained "
          f"window: bookshelves emptied, tea chests on the floor, and on a bare table a stack "
          f"of twenty-nine identical slim work diaries squared up neatly, one open. No people "
          f"in the frame. Dust in the light. {STYLE}")

here = os.path.dirname(os.path.abspath(__file__))
json.dump(S, open(os.path.join(here, "prompts.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# --- KAPAKLAR ---
# Renk talebi acik ve tekrarli: onceki kapaklarin doygunlugu 4-14 arasindaydi.
COLOUR = ("rich saturated colour, warm amber lamplight against cool blue dusk through the "
          "window, strong colour contrast, deep but not murky shadows, bright clean "
          "exposure on skin, fine film grain, painterly photorealism")

A = ("a fictional depiction of a woman resembling Audrey Hepburn in her forties, very "
     "slender, dark hair worn up, large expressive dark eyes, delicate features, an "
     "elegant dark high-necked dress, natural anatomically correct proportions, realistic "
     "head-to-body ratio, minimal makeup")

G = ("a plain-looking Italian woman of about fifty-five in a grey suit, hair pulled back, "
     "no jewellery, entirely unremarkable, natural realistic proportions")

json.dump({"1": (f"Two women in a Roman hotel room at dusk in 1981. In the foreground and lit "
                 f"brightly, {A}, turned toward the camera and caught mid-sentence with a "
                 f"guarded expression, her face the brightest element in the frame. Directly "
                 f"behind her shoulder and slightly smaller, {G}, seated in a plain chair, "
                 f"looking straight at the viewer with an unreadable expression. The two "
                 f"faces are the only lit things in the room. {COLOUR}, 16:9")},
          open(os.path.join(here, "thumb_h.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

json.dump({"1": (f"Vertical composition of two women in a Roman hotel room at dusk in 1981. "
                 f"In the foreground, {A}, caught mid-sentence with a guarded expression, "
                 f"her face the brightest element. Behind her shoulder and lower in the "
                 f"frame, {G}, seated, looking straight at the viewer. {COLOUR}, vertical "
                 f"9:16 composition")},
          open(os.path.join(here, "thumb_v.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("prompts.json, thumb_h.json, thumb_v.json yazildi")
