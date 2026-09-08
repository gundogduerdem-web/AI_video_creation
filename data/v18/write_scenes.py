# -*- coding: utf-8 -*-
"""V18 — "The Winter" — ARAMA TALEBI TESTI. KURGU DEGIL.

Bu video kanalin normal formatindan tek bir degiskenle ayriliyor: konu
uydurma degil, gercek ve ARANAN bir konu. Uretim tarafi sabit tutuluyor
(8 sahne, ayni ses, ayni gorsel dil, 13-15 dk) ki trafik kirilimindaki
fark konudan gelsin.

Olgusal kurallar:
  * Uydurma sahne, uydurma diyalog, uydurma ayrinti YOK.
  * Belgelenen ile tartismali olan acikca ayriliyor (6. sahne).
  * Kurgu beyani yerine kaynak/belirsizlik beyani (8. sahne).

Yeni kurallar (7 Eyl teshisi):
  * Sahne 1'de META CUMLE YOK — hikaye dogrudan basliyor.
  * Hedef 1570-1630 karakter/sahne (Vertex TTS hizina gore).
"""
import json, os

S = {}

S[1] = (
"On the fifteenth of August 1942, in a wood outside the Dutch town of Goirle, a man named Otto Ernst "
"Gelder, Count van Limburg Stirum, was put in front of a firing squad and shot. He was one of five "
"hostages executed that day. He had done nothing. That was the entire point of him: the Germans had "
"taken prominent Dutchmen into custody precisely so that they could be killed later, in response to "
"something somebody else did, and in August 1942 somebody else did something. He was a lawyer and a judge, and he was married to a woman "
"named Miesje, whose sister had a daughter of thirteen. The girl's name was Audrey Kathleen "
"Ruston, and Otto was her uncle, and she had been living in his house. She was told the way children "
"were told things in that year, which is to say quickly and by an adult who was trying not to come "
"apart in front of her. Reprisal killing of hostages was not an aberration in the occupied "
"Netherlands; it was policy, and the men held for it were chosen for their standing rather than for "
"anything they had done, on the reasoning that the deaths of people who mattered locally would deter "
"a population more efficiently. What is known about what it did to her is not very much and comes almost "
"entirely from remarks she made decades later, in her fifties and sixties, usually briefly and "
"usually when asked about something else. One of the few consistent things across those "
"remarks is that she did not say his name. Not that she avoided the subject — she referred to the "
"execution more than once — but the man himself went unnamed, for fifty years, in every account of "
"hers that anybody wrote down."
)

S[2] = (
"Her family were not ordinary people in that part of Holland, and this cut both ways. Her "
"grandfather, Baron Aarnoud van Heemstra, had been mayor of Arnhem and before that governor of "
"Surinam. Her mother was a baroness. They were the sort of family whose name appeared in a newspaper when somebody died, and in "
"an occupied country that is a mixed inheritance: it buys a certain amount of protection right up "
"until the moment it makes you useful as a hostage, and then it is the reason they take you. Otto "
"was not taken because of anything he had done. He was taken because of who his family were, which "
"is to say for the same reason that had kept them comfortable for two hundred years. After "
"Otto was shot, Audrey and her mother left Arnhem and moved to Velp, a village about five kilometres "
"away, into the grandfather's house, where she spent the rest of the war. Moving did not make them "
"safer in any meaningful way: it left them inside the same occupation, with the same name, in a "
"district about to become a front line. Arnhem was where she had trained; by 1944 she was the town's "
"best-known young dancer, which in a place that size is a real distinction and a very small one. Velp "
"was close enough that when Arnhem was destroyed she could hear it. There is a detail here that gets "
"lost in most retellings, and it matters for everything that follows: she was not in a city under "
"occupation, distant from the fighting. She was five kilometres from what became, in September 1944, "
"one of the worst battles of the war in western Europe, and she stayed there through all of it."
)

S[3] = (
"What she did during the occupation that is best attested, and least dramatic, was dance. There was a "
"practice in the occupied Netherlands of holding what were called black evenings: closed performances "
"in private houses, curtains drawn, no advertising, no posters, an invited audience, and money "
"collected afterward for people who needed it — families in hiding, people without ration cards, "
"whoever the organisers were supporting. Audrey performed at these. This is not seriously disputed by "
"anybody, including the people most sceptical of the larger claims about her war. She described it "
"herself, more than once, and the descriptions are consistent and unglamorous. It is also, if you "
"think about it for a moment, not a small thing to have done. An unauthorised gathering was itself "
"punishable, the money went to people the occupier was hunting, and a girl of fifteen standing in a "
"lit room in front of thirty witnesses is not an anonymous participant. The detail everybody "
"remembers is that there was no music, or almost none: a piano played very quietly, or nothing at "
"all, because sound carried and a gathering was itself the offence. She said afterward that the "
"audiences did not applaud when it was over. They could not. They sat in a room in the dark and at "
"the end of it they made no noise whatsoever, and then they went home separately at intervals so that "
"nobody outside would see a crowd leaving a house. She said it was the best audience she ever had, "
"and she said it flatly, as a matter of fact, and she was still saying it in the nineteen-eighties, "
"forty years and an entire film career later."
)

S[4] = (
"In September 1944 the war arrived. The operation was called Market Garden and its object was a "
"bridge at Arnhem, and what matters here is not the plan but what happened to the town. "
"British and Polish airborne troops landed west of Arnhem on the seventeenth of September. The "
"fighting lasted nine days and ended with the survivors withdrawing across the river and the town in "
"German hands and largely wrecked. Then, at the end of September, the Germans ordered "
"Arnhem evacuated. The whole town. Something like ninety-five thousand people were put out of their "
"houses and told to go, and they went east and north into villages with no capacity to hold them, "
"carrying what they could push or drag, ahead of the coldest winter anybody there could remember. "
"Arnhem stayed empty for the rest of the war and was systematically looted, so the people who came "
"back in 1945 came back to a town stripped as well as shelled. "
"and Velp is one of the villages they went to. Velp had perhaps eight thousand people in it before "
"this. The van Heemstra house took in refugees, as most houses did, because there was nowhere else "
"for anyone to be. So the winter that follows does not begin with a full larder and a quiet village. "
"It begins with a village holding several times its own population, in a region stripped by nine "
"days of fighting, with the front line a few kilometres away and no prospect of it "
"moving, because after Market Garden failed the Allies stopped, and the Netherlands north of the "
"rivers stayed occupied for another seven months. The south of the country was free by that autumn; "
"Velp was on the wrong side of the line."
)

S[5] = (
"The Hunger Winter is what happened next, and the name is not a figure of speech. A rail "
"strike, a German embargo on food transport, an early hard frost that froze the canals the barges "
"used, and a region that had just been fought over: those four things produced a famine in one of "
"the most developed countries in Europe. Around twenty thousand people "
"died of it. Rations in the worst weeks fell to a few hundred calories a day, which is not a diet, "
"is a rate of dying. People ate sugar beets, which are livestock feed, and tulip bulbs, and that "
"detail deserves to survive, because it is as bad as it sounds: bulbs are not food, they "
"have to be prepared carefully to be edible at all, and eating them means the beets are gone. Some of "
"the bulbs eaten that winter had been kept for planting, which tells you what people had concluded "
"about the spring. Audrey ate them, and nettles, and drank water to "
"fill her stomach, which is what you do when there is nothing, and which does not work. By the spring "
"of 1945 she was about five foot six and weighed roughly forty kilos. She had oedema — the swelling "
"that comes when the body has no protein left to hold fluid where it belongs — and jaundice, "
"and anaemia, and the respiratory trouble that had started that winter stayed with her for years. "
"There is a long-running claim that the famine is why she was thin for the rest of her life, and it "
"is not quite right: she was naturally slight and said so herself. What that winter left was less "
"visible than a figure: by every account including her own, she was never again able to be relaxed "
"about food being thrown away in front of her."
)

S[6] = (
"The part everybody has heard is also the part with the least evidence behind it. The widely told version is that she worked as a "
"courier for the Dutch resistance, carrying messages in her shoes, and that she once helped hide an "
"Allied paratrooper. It is repeated everywhere. It may well be true in some form. But the honest "
"position is that it is not established, and the reasons are worth stating plainly. She left no "
"diary and no memoir. The detailed version rests largely on a single biography published in 2019, "
"built from interviews and local archives rather than from wartime documents naming her. When the "
"Airborne Museum at Arnhem — the institution with the strongest possible motive to confirm a story "
"like this, and the best archive to do it from — went looking for corroboration in 2016, it did not "
"find any. Dutch people who lived through the occupation there have been sceptical for decades. None "
"of that makes it false. There is also a reason the claim grew in the telling: she was asked about "
"the war for forty years by interviewers who wanted a particular kind of answer, and the gap between "
"what she actually said — usually about hunger, about being frightened, about her uncle — and what "
"got printed is wide enough to see from a distance. Resistance work was deliberately undocumented; that was the point of it, and "
"a fifteen-year-old carrying something a short distance is exactly the kind of act that leaves no "
"record. What it means is that we do not know, and that anybody telling you confidently in "
"either direction is going beyond what the evidence will carry."
)

S[7] = (
"Velp was liberated on the sixteenth of April 1945, by Canadian troops, and the thing she remembered "
"about it was not the tanks. In the days that followed, the relief operation came in behind the army "
"— eventually under the United Nations Relief and Rehabilitation Administration — and it used the "
"local schools as distribution points. Food, medicine, clothing, sent from abroad, laid out in rooms "
"where children had been taught. She went, like everybody, and she came away with food and with "
"clothes shipped from America, and the detail she kept returning to for the rest of her "
"life was smaller than any of that. It was the smell of the food, and the fact that the tins had "
"come from people who would never find out whether it had worked. She said that the first thing she "
"did was eat too much of it and make herself extremely ill, which is a documented hazard of "
"refeeding after starvation and which was happening all over the country that month; the relief "
"workers learned quickly to hand out small amounts repeatedly rather than a great deal at once. She also said, "
"much later and in a context where she had nothing to gain by saying it, that she had never in her "
"life felt anything like what she felt in that schoolroom, and that she did not have a good word for "
"it, and that gratitude was not really the right one because gratitude is something you feel toward a "
"person and there was no person there, just a room with things in it that had come from strangers. "
"The whole of what is reliably known about her war fits between two rooms: a house with the curtains "
"drawn and no applause, and a school with tins in it."
)

S[8] = (
"That relief administration was wound up in 1947, and part of what it had been doing was handed to a "
"new body set up to look after children in countries wrecked by the war. It was called the United "
"Nations International Children's Emergency Fund. Forty years later, Audrey Hepburn spent the last "
"five years of her life working for it, travelling to Ethiopia and Sudan and Somalia and Vietnam and "
"Bangladesh, and she was asked, constantly and by everybody, why she was doing it. She gave the same "
"answer every time and it was never a very satisfying one for an interviewer, because it was not a "
"story about herself. She said that she had been on the receiving end, that there is nothing "
"exceptional about a child who was fed by an international organisation and later worked for one, and "
"that the only unusual thing about her case was that she had become famous in between and was "
"therefore useful. She was blunter than that, in fact, on at least one occasion: asked whether the "
"work was a way of repaying something, she said that it was not a debt, because a debt implies "
"somebody is owed, and the people who had put the tins in that schoolroom in 1945 were not waiting "
"for anything and most of them were dead by then anyway. She died in January 1993, five years after "
"she started. This account is not fiction. The dates, the deaths, the "
"famine, the numbers and the relief work are drawn from the historical record; where accounts differ "
"— above all about the resistance work — that has been said in the telling rather than smoothed over, "
"and no scene, conversation or detail has been invented."
)

for k in sorted(S):
    n = len(S[k])
    print(k, n, ("OK" if 1570 <= n <= 1630 else n - 1600))

here = os.path.dirname(os.path.abspath(__file__))
json.dump({str(k): S[k] for k in sorted(S)},
          open(os.path.join(here, "scenes.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
with open(os.path.join(here, "script.txt"), "w", encoding="utf-8") as fh:
    for k in sorted(S):
        fh.write(f"[SCENE{k}]\n{S[k]}\n[/SCENE{k}]\n\n")
