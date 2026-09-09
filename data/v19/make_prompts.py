# -*- coding: utf-8 -*-
"""V19 gorsel prompt'lari.

Merkezde HAREKET var: sekiz sahne bir gunun sekiz saatini gosteriyor,
sabahin acik isigindan aksamin sicak lamba isigina. Isik hikayeyi
tasiyor — kadraj ilerledikce gunes aliciyor.

Cocuk her sahnede ayni: ayni ceket, ayni kahverengi paket. Paket gorsel
devamlilik unsuru (V14'teki bisiklet gibi).

KAPAK (8 Eyl CTR kurallari):
  * Tek basina sakin yuz DEGIL — kapakta cocuk ve paket var, Audrey
    kapida; iki figur ve bir eylem.
  * Sahne dusk; "night" modeli karanliga cekiyor.
  * Doygun renk acikca isteniyor (onceki kapaklar 4-14 arasindaydi).
"""
import json, os

STYLE = ("Cinematic film still, black and white 35mm photography, single strong "
         "practical light source, deep chiaroscuro shadows, strong compositional "
         "depth and leading lines, foreground bokeh, shallow depth of field, fine "
         "film grain, painterly photorealism, 16:9")

BOY = ("a thin boy of fifteen in a worn jacket too big at the shoulders and scuffed "
       "shoes, carrying a brown paper parcel about the size of a shoebox under one arm")

S = {}

S["1"] = (f"Early morning light in a narrow Roman street in 1962, long shadows and clean "
          f"air. {BOY} walks away from the camera down the middle of the empty street, "
          f"unhurried, small in a wide frame. Shuttered shops on both sides. {STYLE}")

S["2"] = (f"Mid-morning. {BOY} stands still in front of a shuttered workshop with a faded "
          f"number sixteen on the wall beside him, looking up at the blank facade of the "
          f"building next to it, a torn piece of card held in his free hand. The street "
          f"runs out behind him. {STYLE}")

S["3"] = (f"Interior of a small Roman tobacconist's shop at midday, seen from behind the "
          f"counter: shelves of packets and papers, a man in shirtsleeves mid-sentence with "
          f"a newspaper folded under his elbow, and in the doorway against the bright street "
          f"outside, the silhouette of {BOY}. Strong contrast between shop and street. {STYLE}")

S["4"] = (f"A municipal records office in the early afternoon: tall wooden filing cabinets, "
          f"a high counter, ledgers, and a clerk in an apron standing with an open register "
          f"held against his chest, looking down at {BOY} on the other side of the counter. "
          f"Dusty light from high windows. Seen from behind the boy. {STYLE}")

S["5"] = (f"Late afternoon, the light going amber and low. {BOY} sits alone on a low stone "
          f"wall at the edge of a wide empty piazza, the parcel on his knees, both hands flat "
          f"on top of it, looking at nothing in particular. Long shadows across the stones. "
          f"Nobody else nearby. {STYLE}")

S["6"] = (f"Early evening in a modest Roman apartment building corridor: a door standing open "
          f"and warm interior light spilling out across the tiled floor, {BOY} in the doorway "
          f"seen from behind and slightly below, still holding the parcel, and beyond him the "
          f"blurred figure of a slender woman. His shoulders are the sharpest thing. {STYLE}")

S["7"] = (f"A modest apartment kitchen at night lit by one hanging bulb: a plate with bread "
          f"and cold chicken on a scrubbed wooden table, a glass of water, a boy's worn jacket "
          f"hung on the back of a chair, and a brown paper parcel set carefully on a side "
          f"table by the door. Nobody in the frame. Warm and very quiet. {STYLE}")

S["8"] = (f"The following morning, bright and ordinary: an empty Roman street from the same "
          f"low angle as the first shot, a tram passing at the far end in the distance, and "
          f"no one in the foreground at all. The street simply going on. {STYLE}")

here = os.path.dirname(os.path.abspath(__file__))
json.dump(S, open(os.path.join(here, "prompts.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

COLOUR = ("rich saturated colour, warm amber light from an open doorway against cool blue "
          "dusk in the corridor, strong colour contrast, bright clean exposure on faces, "
          "fine film grain, painterly photorealism")

A = ("a fictional depiction of a woman resembling Audrey Hepburn in her early thirties, very "
     "slender, dark hair, large expressive dark eyes, delicate features, a simple dark dress, "
     "natural anatomically correct proportions, realistic head-to-body ratio, minimal makeup")

json.dump({"1": (f"A doorway at dusk in 1962 Rome. On the left of the frame and lit warmly "
                 f"from inside the flat, {A}, standing in the open doorway looking down with "
                 f"an expression of surprise and concern, her face the brightest thing in the "
                 f"picture. On the right, facing her and seen three-quarters from behind, a "
                 f"thin exhausted boy of fifteen holding out a brown paper parcel with both "
                 f"hands. The parcel is between them at the centre. {COLOUR}, 16:9")},
          open(os.path.join(here, "thumb_h.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

json.dump({"1": (f"Vertical composition of a doorway at dusk in 1962 Rome. Above, lit warmly "
                 f"from inside the flat, {A}, in the open doorway looking down with surprise "
                 f"and concern, her face the brightest thing in the frame. Below her and seen "
                 f"from behind, a thin boy of fifteen holding out a brown paper parcel with "
                 f"both hands. {COLOUR}, vertical 9:16 composition")},
          open(os.path.join(here, "thumb_v.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("prompts.json, thumb_h.json, thumb_v.json yazildi")
