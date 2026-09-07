# -*- coding: utf-8 -*-
"""V16 gorsel prompt'lari.

Yapi topluluk anlatimi oldugu icin merkezde SOKAK var. Sekiz sahnenin
yedisi ayni sokagin farkli bakis acilari; gorsel devamlilik icin sokak
her prompt'ta ayni sozlerle tarif ediliyor.

Audrey her zaman uzak / arkadan / kismi: sokak onu hep parca parca
gordu, kamera da oyle gormeli. Yuzu hicbir sahnede net degil.
IMAGE_SAFETY: asker, uniforma, sembol yok.
"""
import json, os

STYLE = ("Cinematic film still, black and white 35mm photography, single strong "
         "practical light source, deep chiaroscuro shadows, strong compositional "
         "depth and leading lines, foreground bokeh, shallow depth of field, fine "
         "film grain, painterly photorealism, 16:9")

STREET = ("a narrow working-class Roman street in 1960, tall shuttered tenements on "
          "both sides, washing strung between balconies, wet cobblestones, a single "
          "streetlamp")

WOMAN = ("a slender woman in a plain dark belted coat and low heels, seen from a "
         "distance and from behind, her face not visible")

S = {}

S["1"] = (f"{STREET} at night, seen in a very wide shot from one end. {WOMAN} walks away "
          f"from the camera toward a doorway far down the street, small in the frame. Lit "
          f"windows above her on both sides. Nobody else on the street. {STYLE}")

S["2"] = (f"Interior of a tiny corner grocery in 1960 Rome at night, shot from behind the "
          f"counter past jars and hanging goods: an older woman in an apron stands watching "
          f"through the window glass, and beyond the glass, out of focus and reversed by the "
          f"reflection, the blurred dark shape of a woman passing on the pavement. The "
          f"shopkeeper's face is the sharp thing in the frame. {STYLE}")

S["3"] = (f"Three women in housecoats leaning out of two adjacent balcony windows above "
          f"{STREET}, talking to each other across the gap in the middle of the day, animated "
          f"and absorbed. Below them the empty street. Shot from street level looking steeply "
          f"up. Hard midday light and deep shadow between the buildings. {STYLE}")

S["4"] = (f"A dim tenement stairwell in 1960 Rome seen from a landing above: worn stone "
          f"steps, an iron banister, one bare bulb, a boy of about nine sitting on the top "
          f"step with his arms around his knees, and far below on the turn of the stair the "
          f"partial dark shape of a woman going up, only a shoulder and a hand on the rail "
          f"visible. {STYLE}")

S["5"] = (f"A small bare rented room in 1960 lit by one lamp: an upright piano against the "
          f"wall with the lid open, a wooden chair, a folded newspaper, and a brown paper "
          f"parcel on the table. An elderly woman with clouded unfocused eyes sits very "
          f"upright by the piano, listening rather than looking. Seen from the doorway. No "
          f"one else in the frame. {STYLE}")

S["6"] = (f"Very close on an elderly woman's hands resting on piano keys in lamplight, still, "
          f"not playing, the knuckles enlarged with age. Behind them and far out of focus, a "
          f"second figure sits with an open newspaper. Everything beyond the keyboard falls "
          f"into darkness. No faces. {STYLE}")

S["7"] = (f"{STREET} in the early morning after a death: a small funeral gathering of about "
          f"twenty people in dark clothes standing outside a doorway, seen from across the "
          f"street through a foreground of parked bicycles and a lamp post. Grey flat winter "
          f"light. Everyone turned inward, nobody looking at the camera. {STYLE}")

S["8"] = (f"The inside of a shoemaker's workshop the size of a wardrobe in 1963: lasts and "
          f"tools on every wall, a low bench, leather offcuts on the floor, one window "
          f"throwing daylight across the room. A very old man sits on a stool; opposite him "
          f"an empty second chair with a woman's gloves left on the seat. Warm daylight, dust "
          f"in the air. {STYLE}")

here = os.path.dirname(os.path.abspath(__file__))
json.dump(S, open(os.path.join(here, "prompts.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

TH = ("Colour cinematic film still, rich saturated colour, a narrow Roman street at "
      "night in 1960, cold blue lamplight with one warm window behind, deep shadows, "
      "fine film grain, painterly photorealism")

A = ("a fictional depiction of a woman resembling Audrey Hepburn in her early thirties, "
     "very slender, dark hair worn up, large expressive dark eyes, delicate features, a "
     "plain dark belted coat with the collar turned up, natural anatomically correct "
     "proportions, realistic head-to-body ratio, minimal makeup")

json.dump({"1": (f"Extreme close-up portrait of {A} stopped on a dark cobbled street at "
                 f"night, face filling the frame, glancing back over her shoulder past the "
                 f"camera, guarded and unsmiling, a lit tenement window glowing far behind "
                 f"her. {TH}, 16:9")},
          open(os.path.join(here, "thumb_h.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

json.dump({"1": (f"Vertical full-frame close-up portrait of {A} stopped on a dark cobbled "
                 f"street at night, face and shoulders filling the vertical frame, glancing "
                 f"back over her shoulder past the camera, guarded and unsmiling, a lit "
                 f"tenement window glowing far behind her. {TH}, vertical 9:16 composition")},
          open(os.path.join(here, "thumb_v.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("prompts.json, thumb_h.json, thumb_v.json yazildi")
