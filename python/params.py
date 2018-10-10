from fields import Fq, Fq2

# Fields
q = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
r = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001

# Curve Params
b = 4

# G1
g1_x = Fq(3685416753713387016781088315183077757961620795782546409894578378688607592378376318836054947676345821548104185464507, q)
g1_y = Fq(1339506544944476473020471379941921221584933875938349620426543736416511423956333506472724655353366534992391756441569, q)

# G2
g2_x0 = Fq(352701069587466618187139116011060144890029952792775240219908644239793785735715026873347600343865175952761926303160, q)
g2_x1 = Fq(3059144344244213709971259814753781636986470325476647558659373206291635324768958432433509563104347017837885763365758, q)
g2_y0 = Fq(1985150602287291935568054521177171638300868978215655730859378665066344726373823718423869104263333984641494340347905, q)
g2_y1 = Fq(927553665492332455747201965776037880757740193453592970025027978793976877002675564980949289727957565575433344219582, q)
g2_x = Fq2(g2_x0, g2_x1)
g2_y = Fq2(g2_y0, g2_y1)


# BLS Params
BLS_x = 0xd201000000010000
BLS_negative = True

# Frobenius map coefficients
# Fq(-1)**(((q**0) - 1) / 2), Fq(-1)**(((q**1) - 1) / 2)
FROB_FQ2 = (Fq(4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559786, q), Fq(1, q))
# tuple(Fq2.all_one_poly(q) ** (((q ** i) - 1) // 3) for i in range(0, 6))
FROB_FQ6_C1 = (Fq2(1, 1),
               Fq2(Fq(0, q), Fq(4002409555221667392624310435006688643935503118305586438271171395842971157480381377015405980053539358417135540939436, q)),
               Fq2(Fq(793479390729215512621379701633421447060886740281060493010456487427281649075476305620758731620350, q), Fq(0, q)),
               Fq2(Fq(0, q), Fq(1, q)),
               Fq2(Fq(4002409555221667392624310435006688643935503118305586438271171395842971157480381377015405980053539358417135540939436, q), Fq(0, q)),
               Fq2(Fq(0, q), Fq(793479390729215512621379701633421447060886740281060493010456487427281649075476305620758731620350, q)))
# tuple(Fq2.all_one_poly(q) ** (((2*q ** i) - 2) // 3) for i in range(0, 6))
FROB_FQ6_C2 = (Fq2(Fq(1, q), Fq(1, q)),
               Fq2(Fq(4002409555221667392624310435006688643935503118305586438271171395842971157480381377015405980053539358417135540939437, q), Fq(0, q)),
               Fq2(Fq(4002409555221667392624310435006688643935503118305586438271171395842971157480381377015405980053539358417135540939436, q), Fq(0, q)),
               Fq2(Fq(4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559786, q), Fq(0, q)),
               Fq2(Fq(793479390729215512621379701633421447060886740281060493010456487427281649075476305620758731620350, q), Fq(0, q)),
               Fq2(Fq(793479390729215512621379701633421447060886740281060493010456487427281649075476305620758731620351, q), Fq(0, q)))
# tuple(Fq2.all_one_poly(q) ** (((q ** i) - 1) // 6) for i in range(0, 12))
FROB_FQ12_C1 = (Fq2(Fq(1, q), Fq(1, q)),
                Fq2(Fq(3850754370037169011952147076051364057158807420970682438676050522613628423219637725072182697113062777891589506424760, q), Fq(151655185184498381465642749684540099398075398968325446656007613510403227271200139370504932015952886146304766135027, q)),
                Fq2(Fq(793479390729215512621379701633421447060886740281060493010456487427281649075476305620758731620351, q), Fq(0, q)),
                Fq2(Fq(2973677408986561043442465346520108879172042883009249989176415018091420807192182638567116318576472649347015917690530, q), Fq(1028732146235106349975324479215795277384839936929757896155643118032610843298655225875571310552543014690878354869257, q)),
                Fq2(Fq(793479390729215512621379701633421447060886740281060493010456487427281649075476305620758731620350, q), Fq(0, q)),
                Fq2(Fq(3125332594171059424908108096204648978570118281977575435832422631601824034463382777937621250592425535493320683825557, q), Fq(877076961050607968509681729531255177986764537961432449499635504522207616027455086505066378536590128544573588734230, q)),
                Fq2(Fq(4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559786, q), Fq(0, q)),
                Fq2(Fq(151655185184498381465642749684540099398075398968325446656007613510403227271200139370504932015952886146304766135027, q), Fq(3850754370037169011952147076051364057158807420970682438676050522613628423219637725072182697113062777891589506424760, q)),
                Fq2(Fq(4002409555221667392624310435006688643935503118305586438271171395842971157480381377015405980053539358417135540939436, q), Fq(0, q)),
                Fq2(Fq(1028732146235106349975324479215795277384839936929757896155643118032610843298655225875571310552543014690878354869257, q), Fq(2973677408986561043442465346520108879172042883009249989176415018091420807192182638567116318576472649347015917690530, q)),
                Fq2(Fq(4002409555221667392624310435006688643935503118305586438271171395842971157480381377015405980053539358417135540939437, q), Fq(0, q)),
                Fq2(Fq(877076961050607968509681729531255177986764537961432449499635504522207616027455086505066378536590128544573588734230, q), Fq(3125332594171059424908108096204648978570118281977575435832422631601824034463382777937621250592425535493320683825557, q)))
