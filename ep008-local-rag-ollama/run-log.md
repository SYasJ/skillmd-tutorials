# Run log — ep008 (real runs, 2026-10-29 ~18:20–18:45 UTC)

Mac, Ollama 0.30.11, llama3.2:3b + nomic-embed-text, Python venv with ollama 0.6.3 + pypdf 6.21.4.
Output copied from the terminal recordings, unedited except removed spinner characters and terminal control codes. "seconds" = wall time of the whole command. `ollama run` redraws a word when it wraps, so the doubled fragments at line ends (th / the) come from removing those redraw codes.

## r2-norag-tacheles · No RAG: model alone (ollama run)

`ollama run llama3.2:3b "Who built the TACHELES payload on Artemis II, and what does it test?"` · 31.01 s

```
I cannot verify who built the TACHELES payload on the Artemis II mission. However, I can tell you that th
the TACHELES (Technological Adaptation of CubeSats for Habitat Exploration) is a scientific payload desig
designed to test technologies for future lunar or planetary habitats.

The TACHELES payload was launched aboard the Space Launch System (SLS) rocket and the Orion spacecraft on
on the Artemis II mission. The mission aimed to send astronauts on a flyby around the Moon and return the
them safely to Earth, while also testing various systems and technologies that will be necessary for futu
future human missions to the lunar surface.

The TACHELES payload is designed to test several key technologies, including:

1. Radiation protection: The payload includes a radiation shield made of water and liquid hydrogen to pro
protect astronauts from harmful space radiation.
2. In-situ resource utilization (ISRU): The payload tests an ISRU system that can extract resources such 
as lunar regolith and water ice for future missions.
3. Advanced life support systems: The payload includes a small, closed-loop life support system that can 
recycle air, water, and waste to sustain astronauts on long-duration missions.

Overall, the TACHELES payload is designed to test critical technologies for future human missions to the 
Moon and beyond.
```

## r1-norag · No RAG: model alone

`ollama run llama3.2:3b "How many radiation sensors covered the Orion spacecraft on Artemis I?"` · 15.3 s

```
I cannot verify how many radiation sensors were used in the Orion spacecraft during the Artemis I mission
mission.
```

## r3-index-tacheles · v1: first run, builds the index

`python rag.py artemis-ii-reference-guide.pdf "Who built the TACHELES payload on Artemis II, and what does it test?"` · 142.52 s

```
indexed 525 chunks in 122 s
According to page 78 of the context, TACHALES was developed by the German Aerospace Center (DLR). It tests key in-space technologies, including electrical components.

sources: p.117, p.86, p.78, p.126  (19.0 s)
```

## r4-sensors · v1: half answer (mistake 1)

`python rag.py artemis-ii-reference-guide.pdf "How many radiation sensors covered the Orion spacecraft on Artemis I?"` · 13.78 s

```
5,600 (page 15)

sources: p.15, p.15, p.15, p.15  (12.9 s)
```

## r5-launchdate · v1: not in the PDF

`python rag.py artemis-ii-reference-guide.pdf "On what date did Artemis II actually launch?"` · 17.4 s

```
I don't know.

The context doesn't mention a specific launch date for Artemis II, only that it was part of the test flight on Nov. 16, 2022, and that the completion date is December 2019, which seems to refer to the completion of development or testing rather than a launch date.

sources: p.120, p.75, p.43, p.10  (16.7 s)
```

## r6-sensors-fixed · v2 (quote prompt): first try

`python rag.py artemis-ii-reference-guide.pdf "How many radiation sensors covered the Orion spacecraft on Artemis I?"` · 17.66 s

```
There were 5,600 passive and 34 active radiation sensors.

[page 15]

Note: There is no specific page number quoted in the original text, so I didn't include a page number in the quote.

sources: p.15, p.15, p.15, p.15  (16.8 s)
```

## r7-tacheles-fixed · v2: TACHELES

`python rag.py artemis-ii-reference-guide.pdf "Who built the TACHELES payload on Artemis II, and what does it test?"` · 41.59 s

```
The TACHELES payload was built by the German Aerospace Center (DLR) and it tests demonstrating key in-space technologies, including electrical components, for future lunar logistics vehicles and operations.

 Sentence used: "Space Weather CubeSat-1 Developer Saudi Space Agency (SSA) Mission Measure various aspects of space weather" is not directly quoted but [page 78] describes the TACHELES payload as: SLS > Secondary Payloads ARTEMIS II REFERENCE GUIDE 2026 Secondary Payloads Artemis II will fly four CubeSat payloads roughly twice the size of the Artemis I CubeSats. Each fits into a volume measuring 14.4 inches (36.6 centimeters) x 9.4 inches (23.9 centimeters) x 8.8 inches (22.4 centimeters), not to exceed 57.3 pounds (26 kilograms). ATENEA Developer Argentina National Space Activities Commission (CONAE) Mission Investigate radiation shielding, orbital design optimization, and long-range communications TACHELES Developer German Aerospace Center (DLR) Mission Demonstrate key in-space technologies, including electrical components, for future lunar logistics vehicles and operations Space Weather CubeSat-1 Developer Saudi Space Agency (SSA) Mission Measure various aspects of space weather 

Page number: 78

sources: p.117, p.86, p.78, p.126  (40.8 s)
```

## r8-sensors-again · v2: second try

`python rag.py artemis-ii-reference-guide.pdf "How many radiation sensors covered the Orion spacecraft on Artemis I?"` · 7.84 s

```
There were 5,600 passive and 34 active radiation sensors covering the Orion spacecraft.

Quote:
"Radiation Sensors Inside Orion During the uncrewed Artemis I mission, Orion was blanketed in 5,600 passive and 34 active radiation sensors." (Page 15)

sources: p.15, p.15, p.15, p.15  (7.0 s)
```

## r9-prefix-index · v3 (nomic prefixes): index rebuilt

`python rag.py artemis-ii-reference-guide.pdf "Who built the TACHELES payload on Artemis II, and what does it test?"` · 164.86 s

```
indexed 525 chunks in 127 s
The TACHELES payload was developed by the German Aerospace Center (DLR).

[page 78] Secondary Payloads ARTEMIS II REFERENCE GUIDE 2026 Secondary Payloads Artemis II will fly four CubeSat payloads roughly twice the size of the Artemis I CubeSats. Each fits into a volume measuring 14.4 inches (36.6 centimeters) x 9.4 inches (23.9 centimeters) x 8.8 inches (22.4 centimeters), not to exceed 57.3 pounds (26 kilograms). ATENEA Developer Argentina National Space Activities Commission (CONAE) Mission Investigate radiation shielding, orbital design optimization, and long-range communications TACHELES Developer German Aerospace Center (DLR) Mission Demonstrate key in-space technologies, including electrical components, for future lunar logistics vehicles and operations

sources: p.115, p.10, p.58, p.78  (36.5 s)
```

## r10-keyword · final (keyword boost)

`python rag.py artemis-ii-reference-guide.pdf "Who built the TACHELES payload on Artemis II, and what does it test?"` · 19.0 s

```
The TACHELES payload was developed by the German Aerospace Center (DLR). It tests the effects of space environment on electrical components.

[page 17]

sources: p.78, p.19, p.29, p.17  (18.1 s)
```

## r11-sensors-final · final

`python rag.py artemis-ii-reference-guide.pdf "How many radiation sensors covered the Orion spacecraft on Artemis I?"` · 11.54 s

```
There were 5,600 passive and 34 active radiation sensors covering the Orion spacecraft during the uncrewed Artemis I mission.

[page 15] Radiation Sensors Inside Orion During the uncrewed Artemis I mission, Orion was blanketed in 5,600 passive and 34 active radiation sensors.

sources: p.15, p.15, p.15, p.113  (10.8 s)
```

## r12-launch-final · final: not in the PDF

`python rag.py artemis-ii-reference-guide.pdf "On what date did Artemis II actually launch?"` · 12.36 s

```
The date when Artemis II was supposed to occur is not mentioned in the context.

I don't know.

sources: p.120, p.43, p.10, p.82  (11.6 s)
```
