# -*- coding: utf-8 -*-
"""V22 — "Table Nine". Tamamen kurgu.
Yapi: TEK MEKAN, KIRK YIL — bir kose masasi ve basindan gecen sekiz an,
1953-1994. Her sahnede baska insanlar; tekrar eden bir gozlemci YOK
(V16 bir sokagin tanıklariydi, V18 tek kisinin seanslariydi; burada
sureklilik masanin kendisi).
Duygusal cekirdek: bir seyin en onemli ani, yasandigi sirada kimse
tarafindan onemli sayilmaz. (Kanalda ilk)
Katalog kontrolu: 61+ videonun hicbirinde mekan-zaman yapisi yok.

Kurallar: sahne 1'de META CUMLE YOK; 1570-1630 karakter/sahne.
"""
import json, os

S = {}

S[1] = (
"The table was in the corner by the service door, which is the worst position in any restaurant, and "
"it was numbered nine on a plan drawn up in 1949 that nobody ever revised. It seated two "
"comfortably and four badly. It was against the wall, under a window that had been painted shut at "
"some point in the war and never opened again, and the service door swung past it roughly every "
"forty seconds during a busy evening. The owner of the trattoria, which was on a side street about "
"eight minutes' walk from the Spanish Steps, gave table nine to people he did not know, people who "
"arrived alone, and people who had not booked. He was not being unkind. It was simply the table "
"that was free. On the evening of the eleventh of October 1953, a man of about fifty sat at it on "
"his own for two hours, ate very little, and asked three separate times whether anybody had "
"telephoned. Nobody had. He paid, left a large tip that the waiter tried to reduce, and walked out, "
"and there is no more to be said about him, because nobody ever found out who he was waiting for "
"and he never came back. A man waiting two hours for a telephone call that does not come is the "
"exact texture of what restaurants actually contain. He asked for the telephone twice before he "
"ordered and spent the last forty minutes looking not at his food but at the doorway the owner "
"would have come through if there had been a message. Most of what passes through a room is "
"unresolved. The waiter "
"mentioned him to nobody and remembered him for fifty years, which is also typical, and he was the "
"first of many people at that table who did not know what they were looking at."
)

S[2] = (
"Five months later, on a wet Tuesday in March 1954, a young woman came in alone at about half past "
"six, which is too early for Romans to eat and therefore the only time the place was quiet. She had "
"table nine because every table was free and it was the one nearest the door she had come in by. "
"She had soup and bread and a glass of wine she did not finish, she had a sheaf of typed pages with "
"her which she read while she ate, and she was there for about fifty minutes. The waiter that "
"evening was seventeen and had been working there for three weeks. He did not know who she was. "
"Nobody in Rome knew who she was in March 1954, or rather a great many people were about to and "
"none of them did yet, and the film that would settle the question had not opened in Italy. What he "
"remembered, when he was asked about it forty years later and long after it had become the sort of "
"thing people asked him about, was not her face. It was that she had said thank you to him four "
"times in fifty minutes, which he had found so unusual in a customer that he had mentioned it to "
"the kitchen at the time, and that she had left the pages behind on the chair and he had run out "
"into the street after her with them. She was two streets away, walking fast in the rain without an "
"umbrella, and she took them and thanked him a fifth time and asked whether he had eaten. He had "
"not. He said that he had. He told nobody about that part for thirty years, and said afterward that "
"the reason was not modesty: it was that telling the story meant telling the lie. He was "
"seventeen, and said it because the alternative was letting a customer feel bad for him."
)

S[3] = (
"In June 1959 two men sat at table nine for four hours and made a decision that closed a factory in "
"Terni and put two hundred and six people out of work. They were there so long because they did not "
"want to be overheard, and the corner by the service door is the most private table in any "
"restaurant: the noise covers you and nobody lingers. They ate nothing after the first course, "
"drank a bottle and a half between them, left a normal tip and were perfectly pleasant. The staff "
"had no idea what had been discussed and would not have cared; a long lunch by two men in suits is "
"not an event. The "
"point of including this is not that it was sinister. It is that the largest thing that ever "
"happened at that table, measured by the number of lives it altered, happened in total silence from "
"the room's point of view, and the only reason it is known at all is that one of the two men "
"described the afternoon in a deposition in 1971 and named the restaurant. There is a version of "
"this story where the room somehow registers what is happening in it — where the light changes, or "
"a glass goes over, or somebody at the next table looks up. Nothing of the kind occurred. The "
"kitchen sent out the second course, the service door swung, and two hundred and six people in "
"another province went on with a Tuesday afternoon that they had no reason to think was different "
"from any other. The men were served by the seventeen-year-old, who was by then twenty-two, and who "
"said when he was eventually told what the lunch had been that his only clear memory of it was "
"resenting how long they kept the table."
)

S[4] = (
"There was a proposal of marriage at table nine in 1962 and it was refused. That was on a Sunday in "
"February, at lunch, and the refusal was audible to three other tables and to the waiter, who was by "
"then the same man who had been seventeen in 1954 and who was now twenty-five. He said afterward "
"that the terrible part was not the refusal itself, which was quiet and which the woman clearly "
"found painful to give, but that they then had to sit there and finish, because the food had "
"already been ordered and neither of them could think of a way to leave that was not worse than "
"staying. They were there another fifty minutes. They talked about other things. He brought them "
"coffee that nobody had asked for and did not charge for it, which is the only intervention anybody "
"at that restaurant is recorded as having made in forty years of other people's lives at that "
"table, and he said later that he had not known what else to do with his hands. The couple left "
"separately, ten minutes apart. She came back twice in the following years, with other people, and "
"always sat somewhere else. The man, as far as anybody knows, never came in again. The waiter said "
"that for about two years afterward he could not seat a couple at that table without thinking about "
"it, and that this wore off, and that he was not sure whether the wearing off was a mercy or "
"something worse. What he actually remembered was not either of their faces. It was that the woman "
"ate everything on her plate, carefully, over those fifty minutes, and that he had understood even "
"at twenty-five that she was doing it so he would not have to watch her not eat."
)

S[5] = (
"On an afternoon in 1971 a girl of about nine did her homework at table nine, every weekday for a "
"school year, because her mother worked the till and there was nowhere else to put her. The waiter "
"tested her on her verbs. She hated the table and said so constantly, on the grounds that the "
"service door hit her chair, and she has said since that she can still do the subjunctive faster "
"than anybody she knows and that the two facts are related. She is the only person in this account "
"who spent real time at it — something in the region of six hundred hours, which is more than "
"everybody else in these eight scenes put together — and her memory of it is entirely unremarkable "
"and slightly annoyed. That is worth sitting with for a second. The person with by far the strongest "
"claim on that table has nothing to say about it beyond the draught and the door, and the people "
"who were there for ninety minutes once are the ones who remember the grain of the wood. She is "
"also, incidentally, the only person here who was ever photographed at it, in a snapshot taken by "
"her mother in about 1972 for no reason at all, which survives, and in which the table is almost "
"entirely obscured by a nine-year-old's arms and an exercise book. It is the only image of table "
"nine that is known to exist. Everything else in this account has to be taken on the word of people "
"who were remembering a room. The girl is in her sixties. Asked for atmosphere, she said the "
"room smelled of frying and the waiter had bad teeth, and that she had no memory of any customer "
"at all. When you are nine and doing your verbs, the adults in a restaurant are weather."
)

S[6] = (
"The restaurant nearly closed in 1977. There was a bad two years, and a dispute with the freeholder, "
"and for about four months in the winter of that year it opened only in the evenings, and table "
"nine was stacked with crates of wine because the storeroom had been given up. It is a small detail "
"and it is the reason for a gap: between November 1976 and March 1978 nobody sat there at all. The "
"owner's son, who took over in 1979 and who is the source for most of what is known about the "
"later period, said that his father had considered taking the table out entirely when the crates "
"went back, on the grounds that the room would seat better without it, and had decided against it "
"for a reason that had nothing to do with sentiment: removing it would have meant re-plastering a "
"section of wall behind it that had been damaged in 1968 and never properly repaired. The table "
"stayed because of the wall. Everything that happened at it after 1978 happened because of a "
"plastering job that nobody wanted to pay for. It is worth being blunt about how much of this is "
"like that. The table existed in that corner for forty-five years because of a plan drawn in 1949 "
"by somebody fitting as many covers as possible into an awkward room. It survived 1977 because of "
"damaged plaster. Nobody ever chose it, at any point, for any reason connected to anything that "
"happened at it, and that is true of most of the furniture of most people's lives. The wall, for "
"the record, was damaged by a delivery trolley in April 1968 and still showed the mark when the "
"place closed twenty-six years later. Nobody ever repaired it and nobody ever mentioned it."
)

S[7] = (
"She came back in November 1988. Thirty-four years later, in the evening this time, with three "
"other people, and by then everybody in the room knew exactly who she was and had the sense not to "
"show it. She did not ask for table nine and there is no evidence she recognised it; the party of "
"four was given the corner because it was the only table that would take four at short notice, "
"which is the same reason she had been given it in 1954 and is the least romantic explanation "
"available. The owner's son, who seated her, has been asked many times whether she said anything "
"about having been there before, and has always answered that she did not, and that he did not ask, "
"and that his father would have skinned him if he had. What he does say is that at the end of the "
"evening she thanked each of the three people who had served the table, by name, having got the "
"names from somewhere during the course of the meal without anybody noticing her doing it. The "
"waiter who had been seventeen in 1954 had retired in 1986 and was not there. He heard about the "
"evening the following week, from the son, in the street. He asked one question, which was whether "
"she had been given the corner table, and was told that she had, and he said that was good and "
"changed the subject. The son, who was thirty-one and had not yet heard the 1954 story and would "
"not hear it for another six years, thought nothing of the question at all. When he did hear it, in "
"1994, he went back through what he remembered of that November evening looking for something he "
"had missed, found nothing, and said that this was the correct outcome."
)

S[8] = (
"The trattoria closed in 1994 and the fittings were sold. Table nine went for very little to a "
"dealer who did not know anything about it and who sold it on within a month to a couple furnishing "
"a flat in Monteverde, and as far as anybody has been able to establish it is still in that flat or "
"one like it, in daily use, with no idea attached to it whatsoever. There is no plaque. There was "
"never going to be a plaque; the restaurant was not famous and the table was the bad one by the "
"door. What makes it worth forty years of attention is not that remarkable things happened at it, "
"because remarkable things happen at every table in every restaurant that stays open long enough. "
"It is that at the time, in the room, not one of these occasions looked like anything. Two hundred "
"and six people lost their jobs and the waiter noticed only that the men stayed late. A woman who "
"would be recognised everywhere on earth within a year was a quiet customer who said thank you too "
"often. A woman refused a man and then ate her lunch so that he would not have to sit there "
"watching her not eat it, and the one witness to that was twenty-five and holding a coffee pot he "
"had not been asked for. The only person who could have told you what any of it meant was in the "
"kitchen, or off that week, or seventeen years old and worrying about something else. The man in "
"1953 is still waiting, in the sense that nobody ever found out, and that is the honest proportion "
"of it. This story is a work of fiction. The restaurant, the table, the waiter and every detail in "
"it are invented, created for storytelling and not drawn from any record."
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
