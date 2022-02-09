#!/usr/bin/env python

import svgwrite
import subprocess as sp
from operator import itemgetter
import sys
import os

fastafilename = 'query'

# color lookup table to color code by parental sequence
color_palette = {'P4-3E': 'rgb(351,101,112)', 'cpCitrine': 'rgb(352,102,113)', 'KCY-R1-38H': 'rgb(353,103,114)',
                 'KCY-R1-38L': 'rgb(354,104,115)', 'KCY-R1-158A': 'rgb(355,105,116)', 'KCY-R1': 'rgb(356,106,117)',
                 'Blue102': 'rgb(357,107,118)', 'Rtms5': 'rgb(358,108,119)', 'cp-mKate': 'rgb(359,109,120)',
                 'phiYFPv': 'rgb(360,110,121)', 'TurboGFP-V197L': 'rgb(361,111,122)', 'pdae1GFP': 'rgb(362,112,123)',
                 'anm1GFP2': 'rgb(363,113,124)', 'cgigCP': 'rgb(364,114,125)', 'Fpcondchrom': 'rgb(365,115,126)',
                 'cpasCP': 'rgb(366,116,127)', 'HcRed7': 'rgb(367,117,128)', 'HcRed': 'rgb(368,118,129)',
                 'hcriCP': 'rgb(369,119,130)', 'zFP538': 'rgb(370,120,131)', 'ZsYellow1': 'rgb(371,121,132)',
                 'zoan2RFP': 'rgb(372,122,133)', 'zRFP': 'rgb(373,123,134)', 'Fpag_frag': 'rgb(374,124,135)',
                 'mmilCFP': 'rgb(375,125,136)', 'A1a': 'rgb(376,126,137)', 'amilFP593': 'rgb(377,127,138)',
                 'amilFP597': 'rgb(378,128,139)', 'AdRed': 'rgb(379,129,140)', 'AdRed-C148S': 'rgb(380,130,141)',
                 'meffRFP': 'rgb(381,131,142)', 'meffGFP': 'rgb(382,132,143)', 'dhorRFP': 'rgb(383,133,144)',
                 'alajGFP3': 'rgb(384,134,145)', 'efasGFP': 'rgb(385,135,146)', 'pporRFP': 'rgb(386,136,147)',
                 'meffCFP': 'rgb(387,137,148)', 'pporGFP': 'rgb(388,138,149)', 'amFP486': 'rgb(389,139,150)',
                 'amFP495': 'rgb(390,140,151)', 'amFP515': 'rgb(391,141,152)', 'amFP506': 'rgb(392,142,153)',
                 'amCyan1': 'rgb(393,143,154)', 'stylGFP': 'rgb(394,144,155)', 'AQ143': 'rgb(395,145,156)',
                 'ZsGreen': 'rgb(396,146,157)', 'CheGFP1': 'rgb(397,147,158)', 'fcomFP': 'rgb(398,148,159)',
                 'asCP562': 'rgb(399,149,160)', 'asulCP': 'rgb(400,150,161)', 'M355NA': 'rgb(401,151,162)',
                 'dfGFP': 'rgb(402,152,163)', 'Gamillus0.2': 'rgb(403,153,164)', 'Gamillus0.3': 'rgb(404,154,165)',
                 'Gamillus0.1': 'rgb(405,155,166)', 'Gamillus0.4': 'rgb(406,156,167)',
                 'Gamillus0.5': 'rgb(407,157,168)', 'GFPhal': 'rgb(408,158,169)', 'sg25': 'rgb(409,159,170)',
                 'sg50': 'rgb(410,160,171)', 'sg42': 'rgb(411,161,172)', 'sg12': 'rgb(412,162,173)',
                 'sg11': 'rgb(413,163,174)', 'BFPsol': 'rgb(414,164,175)', 'AsRed2': 'rgb(415,165,176)',
                 'KFP1': 'rgb(416,166,177)', 'AQ14': 'rgb(417,167,178)', 'mTangerine': 'rgb(418,168,179)',
                 'mRFP1-Q66C': 'rgb(419,169,180)', 'mHoneydew': 'rgb(420,170,181)', 'mGrape1': 'rgb(421,171,182)',
                 'mRFP1.1': 'rgb(422,172,183)', 'mRFP1': 'rgb(423,173,184)', 'DsRed.T4': 'rgb(424,174,185)',
                 'DsRed.T3': 'rgb(425,175,186)', 'DsRed-Express': 'rgb(426,176,187)', 'mRFP1-Q66S': 'rgb(427,177,188)',
                 'mRFP1-Q66T': 'rgb(428,178,189)', 'DsRed2': 'rgb(429,179,190)', 'psamCFP': 'rgb(430,180,191)',
                 'mmGFP': 'rgb(431,181,192)', 'zGFP': 'rgb(432,182,193)', 'hcriGFP': 'rgb(433,183,194)',
                 'Jred': 'rgb(434,184,195)', 'rrGFP': 'rgb(435,185,196)', 'rrenGFP': 'rgb(436,186,197)',
                 'CheGFP3': 'rgb(437,187,198)', 'CheGFP4': 'rgb(438,188,199)', 'DsRed.M1': 'rgb(439,189,200)',
                 'E2-Red/Green': 'rgb(440,190,201)', 'DsRed-Max': 'rgb(441,191,202)',
                 'DsRed-Express2': 'rgb(442,192,203)', 'E2-Orange': 'rgb(443,193,204)',
                 'E2-Crimson': 'rgb(444,194,205)', 'KillerOrange': 'rgb(445,195,206)', 'A44-KR': 'rgb(446,196,207)',
                 'KillerRed': 'rgb(447,197,208)', 'anm2CP': 'rgb(448,198,209)', 'PlamGFP': 'rgb(449,199,210)',
                 'mKelly1': 'rgb(450,200,211)', 'mKelly2': 'rgb(451,201,212)', 'TurboGFP': 'rgb(452,202,213)',
                 'mKillerOrange': 'rgb(453,203,214)', 'Katushka-9-5': 'rgb(454,204,215)', 'eqFP650': 'rgb(455,205,216)',
                 'eqFP670': 'rgb(456,206,217)', 'Fpaagar': 'rgb(457,207,218)', 'laGFP': 'rgb(458,208,219)',
                 'laRFP': 'rgb(459,209,220)', 'cFP484': 'rgb(460,210,221)', 'mGinger1': 'rgb(461,211,222)',
                 'mGinger2': 'rgb(462,212,223)', 'FPrfl2.3': 'rgb(463,213,224)', 'rfloGFP2': 'rgb(464,214,225)',
                 'Dendra': 'rgb(465,215,226)', 'dendFP': 'rgb(466,216,227)', 'OFP': 'rgb(467,217,228)',
                 'ptilGFP': 'rgb(468,218,229)', 'mGarnet2': 'rgb(469,219,230)', 'mGarnet': 'rgb(470,220,231)',
                 'mRuby': 'rgb(471,221,232)', 'td-RFP639': 'rgb(472,222,233)', 'd-RFP618': 'rgb(473,223,234)',
                 'eqFP611': 'rgb(474,224,235)', 'RFP637': 'rgb(475,225,236)', 'RFP639': 'rgb(476,226,237)',
                 'RFP618': 'rgb(477,227,238)', 'RFP630': 'rgb(478,228,239)', 'td-RFP611': 'rgb(479,229,240)',
                 'RFP611': 'rgb(480,230,241)', 'Dendra2-T69A': 'rgb(481,231,242)', 'Dendra2-M159A': 'rgb(482,232,243)',
                 'Dendra2': 'rgb(483,233,244)', 'NijiFP': 'rgb(484,234,245)', 'moxDendra2': 'rgb(485,235,246)',
                 'gfasGFP': 'rgb(486,236,247)', 'eechGFP2': 'rgb(487,237,248)', 'eechGFP3': 'rgb(488,238,249)',
                 'mVFP1': 'rgb(489,239,250)', 'dVFP': 'rgb(490,240,251)', 'mVFP': 'rgb(491,241,252)',
                 'VFP': 'rgb(492,242,253)', 'echFP': 'rgb(493,243,254)', 'anm1GFP1': 'rgb(494,244,255)',
                 'ppluGFP1': 'rgb(495,245,256)', 'ppluGFP2': 'rgb(496,246,257)', 'pmeaGFP1': 'rgb(497,247,258)',
                 'pmeaGFP2': 'rgb(498,248,259)', 'LanFP1': 'rgb(499,249,260)', 'pmimGFP1': 'rgb(500,250,261)',
                 'pmimGFP2': 'rgb(501,251,262)', 'laesGFP': 'rgb(502,252,263)', 'scubGFP1': 'rgb(503,253,264)',
                 'scubGFP2': 'rgb(504,254,265)', 'hfriFP': 'rgb(505,255,266)', 'DsRed-Timer': 'rgb(506,256,267)',
                 'DsRed': 'rgb(507,257,268)', 'atenFP': 'rgb(508,258,269)', 'echiFP': 'rgb(509,259,270)',
                 'fcFP': 'rgb(510,260,271)', 'mGeos-C': 'rgb(511,261,272)', 'mGeos-E': 'rgb(512,262,273)',
                 'mGeos-F': 'rgb(513,263,274)', 'mEos2': 'rgb(514,264,275)', 'mEos3.2': 'rgb(515,265,276)',
                 'mEos2-NA': 'rgb(516,266,277)', 'mEos3.1': 'rgb(517,267,278)', 'mEos2-A69T': 'rgb(518,268,279)',
                 'mGeos-L': 'rgb(519,269,280)', 'Skylan-NS': 'rgb(520,270,281)', 'mGeos-M': 'rgb(521,271,282)',
                 'mGeos-S': 'rgb(522,272,283)', 'Skylan-S': 'rgb(523,273,284)', 'mEosFP': 'rgb(524,274,285)',
                 'd1EosFP': 'rgb(525,275,286)', 'd2EosFP': 'rgb(526,276,287)', 'IrisFP-M159A': 'rgb(527,277,288)',
                 'EosFP': 'rgb(528,278,289)', 'IrisFP': 'rgb(529,279,290)', 'mIrisFP': 'rgb(530,280,291)',
                 'mEosFP-M159A': 'rgb(531,281,292)', 'mEosFP-F173S': 'rgb(532,282,293)', 'scubRFP': 'rgb(533,283,294)',
                 'rfloRFP': 'rgb(534,284,295)', 'rfloGFP': 'rgb(535,285,296)', 'dis3GFP': 'rgb(536,286,297)',
                 'DspR1': 'rgb(537,287,298)', 'DstC1': 'rgb(538,288,299)', 'FP586': 'rgb(539,289,300)',
                 'dis2RFP': 'rgb(540,290,301)', 'dsFP483': 'rgb(541,291,302)', 'secBFP2': 'rgb(542,292,303)',
                 'TagBFP': 'rgb(543,293,304)', 'cgfTagRFP': 'rgb(544,294,305)', 'TurboRFP': 'rgb(545,295,306)',
                 'tdKatushka2': 'rgb(546,296,307)', 'mLumin': 'rgb(547,297,308)', 'mKate': 'rgb(548,298,309)',
                 'PAmKate': 'rgb(549,299,310)', 'TagRFP': 'rgb(550,300,311)', 'PATagRFP': 'rgb(551,301,312)',
                 'PATagRFP1314': 'rgb(552,302,313)', 'PATagRFP1297': 'rgb(553,303,314)',
                 'LSS-mKate2': 'rgb(554,304,315)', 'LSS-mKate1': 'rgb(555,305,316)', 'TagRFP675': 'rgb(556,306,317)',
                 'eqFP578': 'rgb(557,307,318)', 'TagRFP657': 'rgb(558,308,319)', 'efasCFP': 'rgb(559,309,320)',
                 'TagCFP': 'rgb(560,310,321)', 'TagGFP2': 'rgb(561,311,322)', 'TagGFP': 'rgb(562,312,323)',
                 'spisCP': 'rgb(563,313,324)', 'ccalYFP1': 'rgb(564,314,325)', 'PS-CFP': 'rgb(565,315,326)',
                 'PS-CFP2': 'rgb(566,316,327)', 'aceGFP-G222E-Y220L': 'rgb(567,317,328)', 'aceGFP': 'rgb(568,318,329)',
                 'GFP-151pyTyrCu': 'rgb(569,319,330)', 'GFP-Tyr151pyz': 'rgb(570,320,331)',
                 'GFPxm18': 'rgb(571,321,332)', 'GFPxm162': 'rgb(572,322,333)', 'GFPxm18uv': 'rgb(573,323,334)',
                 'GFPxm161': 'rgb(574,324,335)', 'GFPxm16': 'rgb(575,325,336)', 'GFPxm163': 'rgb(576,326,337)',
                 'GFPxm191uv': 'rgb(577,327,338)', 'GFPxm19': 'rgb(578,328,339)', 'GFPxm181uv': 'rgb(579,329,340)',
                 'GFPxm19uv': 'rgb(580,330,341)', 'ShG24': 'rgb(581,331,342)', 'OFPxm': 'rgb(582,332,343)',
                 'muGFP': 'rgb(583,333,344)', 'usGFP': 'rgb(584,334,345)', 'vsGFP': 'rgb(585,335,346)',
                 'roGFP1-R8': 'rgb(586,336,347)', 'W1C': 'rgb(587,337,348)', 'GFPmut2': 'rgb(588,338,349)',
                 'GFPmut3': 'rgb(589,339,350)', '11': 'rgb(590,340,351)', 'Topaz': 'rgb(591,341,352)',
                 'BFP': 'rgb(592,342,353)', 'P4': 'rgb(593,343,354)', 'W7': 'rgb(594,344,355)',
                 'CFP': 'rgb(595,345,356)', 'W2': 'rgb(596,346,357)', 'avGFP454': 'rgb(597,347,358)',
                 'Sapphire': 'rgb(598,348,359)', 'H9': 'rgb(599,349,360)', 'avGFP': 'rgb(600,350,361)',
                 'Q80R': 'rgb(601,351,362)', 'P11': 'rgb(602,352,363)', 'P9': 'rgb(603,353,364)',
                 '&alpha;GFP': 'rgb(604,354,365)', 'P4-1': 'rgb(605,355,366)', 'deGFP3': 'rgb(606,356,367)',
                 '5B': 'rgb(0,357,368)', '6C': 'rgb(1,358,369)', 'deGFP1': 'rgb(2,359,370)', 'RSGFP3': 'rgb(3,360,371)',
                 'RSGFP1': 'rgb(4,361,372)', 'RSGFP7': 'rgb(5,362,373)', '10B': 'rgb(6,363,374)',
                 'RSGFP2': 'rgb(7,364,375)', 'BFP.A5': 'rgb(8,365,376)', 'Azurite': 'rgb(9,366,377)',
                 'CGFP': 'rgb(10,367,378)', 'eGFP203C': 'rgb(11,368,379)', 'eGFP205C': 'rgb(12,369,380)',
                 'RSGFP4': 'rgb(13,370,381)', 'BFP5': 'rgb(14,371,382)', 'RSGFP6': 'rgb(15,372,383)',
                 'roGFP1-R1': 'rgb(16,373,384)', 'deGFP4': 'rgb(17,374,385)', 'deGFP2': 'rgb(18,375,386)',
                 'roGFP1': 'rgb(19,376,387)', 'roGFP2': 'rgb(20,377,388)', 'YFP3': 'rgb(21,378,389)',
                 'CFP4': 'rgb(22,379,390)', 'Kaede': 'rgb(23,380,391)', 'eechRFP': 'rgb(24,381,392)',
                 'LanYFP': 'rgb(25,382,393)', 'LanFP2': 'rgb(26,383,394)', 'aacuGFP1': 'rgb(27,384,395)',
                 'alajGFP1': 'rgb(28,385,396)', 'PdaC1': 'rgb(29,386,397)', 'ccalOFP1': 'rgb(30,387,398)',
                 'ccalRFP1': 'rgb(31,388,399)', 'ccalGFP1': 'rgb(32,389,400)', 'ccalGFP3': 'rgb(33,390,401)',
                 'cerFP505': 'rgb(34,391,402)', 'obeGFP': 'rgb(35,392,403)', 'obeYFP': 'rgb(36,393,404)',
                 'obeCFP': 'rgb(37,394,405)', 'phiYFP': 'rgb(38,395,406)', 'CheGFP2': 'rgb(39,396,407)',
                 'amilCP604': 'rgb(40,397,408)', 'psupFP': 'rgb(41,398,409)', 'meffCP': 'rgb(42,399,410)',
                 'amilCP': 'rgb(43,400,411)', 'aacuCP': 'rgb(44,401,412)', 'gfasCP': 'rgb(45,402,413)',
                 'amilCP580': 'rgb(46,403,414)', 'apulCP584': 'rgb(47,404,415)', 'gdjiCP': 'rgb(48,405,416)',
                 'gtenCP': 'rgb(49,406,417)', 'stylCP': 'rgb(50,407,418)', 'amilCP586': 'rgb(51,408,419)',
                 'ahyaCP': 'rgb(52,409,420)', 'mRtms5': 'rgb(53,410,421)', 'Ultramarine': 'rgb(54,411,422)',
                 'sympFP': 'rgb(55,412,423)', 'mUkG': 'rgb(56,413,424)', 'fabdGFP': 'rgb(57,414,425)',
                 'mc4': 'rgb(58,415,426)', 'McaG1': 'rgb(59,416,427)', 'McaG1ea': 'rgb(60,417,428)',
                 'MfaG1': 'rgb(61,418,429)', 'mc2': 'rgb(62,419,430)', 'mc6': 'rgb(63,420,431)',
                 'McaG2': 'rgb(64,421,432)', 'Padron(star)': 'rgb(65,422,433)', 'Kohinoor': 'rgb(66,423,434)',
                 'Padron0.9': 'rgb(67,424,435)', 'Padron': 'rgb(68,425,436)', 'ffDronpa': 'rgb(69,426,437)',
                 'bsDronpa': 'rgb(70,427,438)', 'pcDronpa2': 'rgb(71,428,439)', 'pcDronpa': 'rgb(72,429,440)',
                 '22G': 'rgb(73,430,441)', 'rsFastLime': 'rgb(74,431,442)', 'Dronpa-3': 'rgb(75,432,443)',
                 'Dronpa': 'rgb(76,433,444)', 'Dronpa-2': 'rgb(77,434,445)', 'PDM1-4': 'rgb(78,435,446)',
                 'Dronpa-C62S': 'rgb(79,436,447)', 'meleRFP': 'rgb(80,437,448)', 'mAzamiGreen': 'rgb(81,438,449)',
                 'AzamiGreen': 'rgb(82,439,450)', 'KO': 'rgb(83,440,451)', 'KCY': 'rgb(84,441,452)',
                 'KCY-G4219': 'rgb(85,442,453)', 'KCY-G4219-38L': 'rgb(86,443,454)', 'mcFP506': 'rgb(87,444,455)',
                 'mcavFP': 'rgb(88,445,456)', 'sarcGFP': 'rgb(89,446,457)', 'meruFP': 'rgb(90,447,458)',
                 'eforCP': 'rgb(91,448,459)', 'LEA': 'rgb(92,449,460)', 'mc5': 'rgb(93,450,461)',
                 'mcFP503': 'rgb(94,451,462)', 'mcCFP': 'rgb(95,452,463)', 'mcFP497': 'rgb(96,453,464)',
                 'mcavRFP': 'rgb(97,454,465)', 'mc1': 'rgb(98,455,466)', 'mcRFP': 'rgb(99,456,467)',
                 'meleCFP': 'rgb(100,457,468)', 'eechGFP1': 'rgb(101,458,469)', 'KikGR1': 'rgb(102,459,470)',
                 'mKikGR': 'rgb(103,460,471)', 'KikG': 'rgb(104,461,472)', 'afraGFP': 'rgb(105,462,473)',
                 'Katushka': 'rgb(106,463,474)', 'anobGFP': 'rgb(107,464,475)', 'amilFP490': 'rgb(108,465,476)',
                 'anobCFP2': 'rgb(109,466,477)', 'anobCFP1': 'rgb(110,467,478)', 'amilFP497': 'rgb(111,468,479)',
                 'aeurGFP': 'rgb(112,469,480)', 'amilFP484': 'rgb(113,470,481)', 'amilFP504': 'rgb(114,471,482)',
                 'amilFP512': 'rgb(115,472,483)', 'amilFP513': 'rgb(116,473,484)', 'aacuGFP2': 'rgb(117,474,485)',
                 'dhorGFP': 'rgb(118,475,486)', 'apulFP483': 'rgb(119,476,487)', 'FPmcavgr7.7': 'rgb(120,477,488)',
                 'mc3': 'rgb(121,478,489)', 'mcavGFP': 'rgb(122,479,490)', 'cgreGFP': 'rgb(123,480,491)',
                 'dimer2': 'rgb(124,481,492)', 'dimer1': 'rgb(125,482,493)', 'Katushka2S': 'rgb(126,483,494)',
                 'alajGFP2': 'rgb(127,484,495)', 'mTFP0.6': 'rgb(128,485,496)', 'moxEos3.2': 'rgb(129,486,497)',
                 'mEos4b': 'rgb(130,487,498)', 'mEos4a': 'rgb(131,488,499)', 'cgfmKate2': 'rgb(132,489,500)',
                 'mStable': 'rgb(133,490,501)', 'mKate2': 'rgb(134,491,502)', 'mKate2.5': 'rgb(135,492,503)',
                 'FR-1': 'rgb(136,493,504)', 'rsFusionRed3': 'rgb(137,494,505)', 'rsFusionRed2': 'rgb(138,495,506)',
                 'FusionRed': 'rgb(139,496,507)', 'FusionRed-M': 'rgb(140,497,508)', 'rsFusionRed1': 'rgb(141,498,509)',
                 'AcGFP1': 'rgb(142,499,510)', 'mScarlet-I': 'rgb(143,500,511)', 'mRed7Q1S1BM': 'rgb(144,501,512)',
                 'mScarlet-H': 'rgb(145,502,513)', 'mScarlet': 'rgb(146,503,514)', 'Gamillus': 'rgb(147,504,515)',
                 'RDSmCherry1': 'rgb(148,505,516)', 'RDSmCherry0.5': 'rgb(149,506,517)', 'mRojoA': 'rgb(150,507,518)',
                 'mRojoB': 'rgb(151,508,519)', 'mRouge': 'rgb(152,509,520)', 'PAmCherry2': 'rgb(153,510,521)',
                 'PAmCherry3': 'rgb(154,511,522)', 'rsCherryRev1.4': 'rgb(155,512,523)',
                 'mNectarine': 'rgb(156,513,524)', 'mBlueberry1': 'rgb(157,514,525)',
                 'RDSmCherry0.2': 'rgb(158,515,526)', 'RDSmCherry0.1': 'rgb(159,516,527)',
                 'mCherry': 'rgb(160,517,528)', 'rsCherryRev': 'rgb(161,518,529)', 'rsCherry': 'rgb(162,519,530)',
                 'mCherry1.5': 'rgb(163,520,531)', 'mCherry2': 'rgb(164,521,532)', 'PAmCherry1': 'rgb(165,522,533)',
                 'dLanYFP': 'rgb(166,523,534)', 'mNeonGreen': 'rgb(167,524,535)', 'moxNeonGreen': 'rgb(168,525,536)',
                 'tPapaya0.01': 'rgb(169,526,537)', 'dPapaya0.1': 'rgb(170,527,538)', 'TagYFP': 'rgb(171,528,539)',
                 'CyPet': 'rgb(172,529,540)', 'mAmetrine': 'rgb(173,530,541)', 'Clover': 'rgb(174,531,542)',
                 'mClover3': 'rgb(175,532,543)', 'Clover1.5': 'rgb(176,533,544)', 'mClover1.5': 'rgb(177,534,545)',
                 'dClover2': 'rgb(178,535,546)', 'rsFolder': 'rgb(179,536,547)', 'rsFolder2': 'rgb(180,537,548)',
                 'EBFP1.2': 'rgb(181,538,549)', 'EBFP1.5': 'rgb(182,539,550)', 'EBFP2': 'rgb(183,540,551)',
                 'moxBFP': 'rgb(184,541,552)', 'oxBFP': 'rgb(185,542,553)', 'moxCerulean3': 'rgb(186,543,554)',
                 'moxGFP': 'rgb(187,544,555)', 'oxGFP': 'rgb(188,545,556)', 'moxVenus': 'rgb(189,546,557)',
                 'oxVenus': 'rgb(190,547,558)', 'WasCFP': 'rgb(191,548,559)', 'Dreiklang': 'rgb(192,549,560)',
                 'EYFP-Q69K': 'rgb(193,550,561)', 'Citrine': 'rgb(194,551,562)', 'mCitrine': 'rgb(195,552,563)',
                 'SHardonnay': 'rgb(196,553,564)', 'EYFP': 'rgb(197,554,565)', 'yEGFP': 'rgb(198,555,566)',
                 'Clomeleon': 'rgb(199,556,567)', 'T-Sapphire': 'rgb(200,557,568)', 'mT-Sapphire': 'rgb(201,558,569)',
                 'PA-GFP': 'rgb(202,559,570)', 'mPA-GFP': 'rgb(203,560,571)', 'rsEGFP2': 'rgb(204,561,572)',
                 'SEYFP': 'rgb(205,562,573)', 'SGFP2(T65G)': 'rgb(206,563,574)', 'SBFP1': 'rgb(207,564,575)',
                 'SBFP2': 'rgb(208,565,576)', 'mCerulean2.N(T65S)': 'rgb(209,566,577)',
                 'mCerulean3': 'rgb(210,567,578)', 'mTurquoise2': 'rgb(211,568,579)',
                 'mTurquoise2-G': 'rgb(212,569,580)', 'mTurquoise-146G': 'rgb(213,570,581)',
                 'mTurquoise-DR': 'rgb(214,571,582)', 'mTurquoise': 'rgb(215,572,583)',
                 'Turquoise-GL': 'rgb(216,573,584)', 'mTurquoise-GL': 'rgb(217,574,585)',
                 'mTurquoise-GV': 'rgb(218,575,586)', 'mTurquoise-RA': 'rgb(219,576,587)',
                 'mTurquoise-146S': 'rgb(220,577,588)', 'Aquamarine': 'rgb(221,578,589)', 'EBFP': 'rgb(222,579,590)',
                 'SCFP1': 'rgb(223,580,591)', 'mCerulean.B2': 'rgb(224,581,592)', 'mCerulean.B': 'rgb(225,582,593)',
                 'mCerulean2.N': 'rgb(226,583,594)', 'mCerulean2': 'rgb(227,584,595)',
                 'mCerulean.B24': 'rgb(228,585,596)', 'SCFP3B': 'rgb(229,586,597)', 'Cerulean': 'rgb(230,587,598)',
                 'mCerulean': 'rgb(231,588,599)', 'mCerulean2.D3': 'rgb(232,589,600)', 'D10': 'rgb(233,590,601)',
                 'SCFP3A': 'rgb(234,591,602)', 'SCFP2': 'rgb(235,592,603)', 'ECFP': 'rgb(236,593,604)',
                 'mECFP': 'rgb(237,594,605)', 'ECGFP': 'rgb(238,595,606)', 'SGFP1': 'rgb(239,596,0)',
                 'rsEGFP': 'rgb(240,597,1)', 'iq-mEmerald': 'rgb(241,598,2)', 'Emerald': 'rgb(242,599,3)',
                 'mEmerald': 'rgb(243,600,4)', 'SGFP2(206A)': 'rgb(244,601,5)', 'SGFP2': 'rgb(245,602,6)',
                 'SGFP2(E222Q)': 'rgb(246,603,7)', 'EGFP': 'rgb(247,604,8)', 'mEGFP': 'rgb(248,605,9)',
                 'cfSGFP2': 'rgb(249,606,10)', 'SPOON': 'rgb(250,0,11)', 'EYFP-F46L': 'rgb(251,1,12)',
                 'Venus': 'rgb(252,2,13)', 'mVenus': 'rgb(253,3,14)', 'SYFP2': 'rgb(254,4,15)', 'YPet': 'rgb(255,5,16)',
                 'Citrine2': 'rgb(256,6,17)', 'Sirius': 'rgb(257,7,18)', 'mKalama1': 'rgb(258,8,19)',
                 'mTagBFP2': 'rgb(259,9,20)', 'Maroon0.1': 'rgb(260,10,21)', 'Neptune': 'rgb(261,11,22)',
                 'mNeptune': 'rgb(262,12,23)', 'mNeptune2': 'rgb(263,13,24)', 'mBeRFP': 'rgb(264,14,25)',
                 'TagRFP-T': 'rgb(265,15,26)', 'rsTagRFP': 'rgb(266,16,27)', 'mNeptune684': 'rgb(267,17,28)',
                 'mNeptune681': 'rgb(268,18,29)', 'mCarmine': 'rgb(269,19,30)', 'mCardinal': 'rgb(270,20,31)',
                 'mMaroon1': 'rgb(271,21,32)', 'mNeptune2.5': 'rgb(272,22,33)', 'mRuby2': 'rgb(273,23,34)',
                 'mRuby3': 'rgb(274,24,35)', 'mCyRFP1': 'rgb(275,25,36)', 'CyOFP1': 'rgb(276,26,37)',
                 'CyRFP1': 'rgb(277,27,38)', 'mApple': 'rgb(278,28,39)', 'pHuji': 'rgb(279,29,40)',
                 'mRFP1.5': 'rgb(280,30,41)', 'PSmOrange2': 'rgb(281,31,42)', 'mOrange2': 'rgb(282,32,43)',
                 'mOrange': 'rgb(283,33,44)', 'LSSmOrange': 'rgb(284,34,45)', 'mRFP1.4': 'rgb(285,35,46)',
                 'mOFP.T.8': 'rgb(286,36,47)', 'mOFP.T.12': 'rgb(287,37,48)', 'mStrawberry': 'rgb(288,38,49)',
                 'PSmOrange': 'rgb(289,39,50)', 'mGrape3': 'rgb(290,40,51)', 'mBanana': 'rgb(291,41,52)',
                 'mRFP1.3': 'rgb(292,42,53)', 'mGrape2': 'rgb(293,43,54)', 'mBlueberry2': 'rgb(294,44,55)',
                 'mClavGR1.1': 'rgb(295,45,56)', 'mClavGR1.8': 'rgb(296,46,57)', 'mClavGR2': 'rgb(297,47,58)',
                 'mMaple': 'rgb(298,48,59)', 'dClavGR1.6': 'rgb(299,49,60)', 'mMaple2': 'rgb(300,50,61)',
                 'mMaple3': 'rgb(301,51,62)', 'moxMaple3': 'rgb(302,52,63)', 'mTFP0.7': 'rgb(303,53,64)',
                 'mTFP1-Y67H': 'rgb(304,54,65)', 'mTFP1-Y67W': 'rgb(305,55,66)', 'G3': 'rgb(306,56,67)',
                 'mTFP0.9': 'rgb(307,57,68)', 'mTFP0.8': 'rgb(308,58,69)', 'mTFP1': 'rgb(309,59,70)',
                 'G1': 'rgb(310,60,71)', 'G2': 'rgb(311,61,72)', 'mWasabi': 'rgb(312,62,73)',
                 'mTFP0.4': 'rgb(313,63,74)', 'dTFP0.1': 'rgb(314,64,75)', 'mTFP0.3': 'rgb(315,65,76)',
                 'dTFP0.2': 'rgb(316,66,77)', 'mTFP0.5': 'rgb(317,67,78)', 'mClavGR1': 'rgb(318,68,79)',
                 'mRed7': 'rgb(319,69,80)', 'mRed7Q1S1': 'rgb(320,70,81)', 'mRed7Q1': 'rgb(321,71,82)',
                 'mPlum': 'rgb(322,72,83)', 'mPlum-E16P': 'rgb(323,73,84)', 'dTomato': 'rgb(324,74,85)',
                 'mRaspberry': 'rgb(325,75,86)', 'mRFP1.2': 'rgb(326,76,87)', 'mPapaya0.3': 'rgb(327,77,88)',
                 'mPapaya0.6': 'rgb(328,78,89)', 'mPapaya': 'rgb(329,79,90)', 'mPapaya0.7': 'rgb(330,80,91)',
                 'NowGFP': 'rgb(331,81,92)', 'dKeima': 'rgb(332,82,93)', 'tKeima': 'rgb(333,83,94)',
                 'dKeima570': 'rgb(334,84,95)', 'mKeima': 'rgb(335,85,96)', 'mKG': 'rgb(336,86,97)',
                 'mK-GO': 'rgb(337,87,98)', 'mKO&kappa;': 'rgb(338,88,99)', 'mKO2': 'rgb(339,89,100)',
                 'mKO': 'rgb(340,90,101)', 'MiCy': 'rgb(341,91,102)', 'mMiCy': 'rgb(342,92,103)',
                 'asFP499': 'rgb(343,93,104)', 'cgigGFP': 'rgb(344,94,105)', 'hmGFP': 'rgb(345,95,106)',
                 'HcRed-Tandem': 'rgb(346,96,107)', 'aceGFP-h': 'rgb(347,97,108)', '(3-F)Tyr-EGFP': 'rgb(348,98,109)',
                 'cEGFP': 'rgb(349,99,110)'}


def fasta_length_parser(fastafilename):
    seq_name = []
    seq_length = []
    # current_gene = ""   # Start with an empty string, just in case
    genes = {}  # Make an empty dictionary of genes
    try:
        fh = open(fastafilename, 'r')
    except IOError:
        print('Could not find file with filename %s' % (fastafilename))
        result = 'Please verify that your filename is correct and try again.'
        return result
    for lineInd, line in enumerate(fh.readlines()):
        if lineInd == 0:
            if not line[0] == '>':
                print('File does not conform to FASTA format.')
                result = 'Please try again with FASTA formatted file.'
                fh.close()
                return result
            else:
                pass
        else:
            pass
        line = line.strip()  # Clear out leading/trailing whitespace
        line = line.upper()  # Deals with whatever case the
        # sequence is by making it all upper case
        if len(line) > 0 and line[0] == ">":  # This one is a new gene
            seq_name.append(line[1:])
        # genes[current_gene] = ""
        else:  # Add onto the current gene
            seq_length.append(len(line))
    fh.close()

    seq_info = seq_name, seq_length
    return seq_info

barcode_list = []
global_seq_blocks_kept = []
def shuffled_blocks_analysis(fasta_file):
    program = 'blastp'
    queryseq = fasta_file  # fasta_file #input fasta chimera sequence (AA seq)
    database = 'FP_DB_full.db'
    eval = '1e-6'
    outfmt = '6'  # output format
    # run the blast search as a process and capture the output
    proc = sp.Popen([program, '-query', queryseq, '-db', database, '-evalue', eval, '-use_sw_tback', '-outfmt', outfmt],
                    stdout=sp.PIPE)
    output = proc.communicate()
    outlist = str(output[0]).split('\n')[:-1]
    seq_blocks = []

    for line in range(len(outlist)):
        out_line = outlist[line].split('\t')
        seq_name = out_line[0]
        if seq_name not in barcode_list:
            barcode_list.append(seq_name)
        seq_index=barcode_list.index(seq_name)
        seq_blocks.append([out_line[1], int(out_line[3]), int(out_line[6]), int(out_line[7]), seq_index,float(out_line[10])])
    # [parent_name,  alignment length (sequence overlap), start of alignment in query, end of alignment in query, barcode index]

    seq_blocks = sorted(seq_blocks, key=lambda x: (x[4], x[1]))
    print(barcode_list)
    blocks_to_filter = []

    for i in range(len(barcode_list)):
        for bigblock_index in range(len(seq_blocks)):
            if seq_blocks[bigblock_index][4] != i:
                continue
            start = seq_blocks[bigblock_index][2]
            end = seq_blocks[bigblock_index][3]
            for smallblock_index in range(len(seq_blocks)):
                if smallblock_index == bigblock_index:
                    continue
                if seq_blocks[smallblock_index][4] != i:
                    continue
                if start == seq_blocks[smallblock_index][2] and end == seq_blocks[smallblock_index][3]: # if outer and inner blocks are same size
                    if seq_blocks[smallblock_index][5] < seq_blocks[bigblock_index][5]: # if inner block has lower e value
                        if seq_blocks[smallblock_index] not in blocks_to_filter:
                            blocks_to_filter.append(seq_blocks[bigblock_index]) # add the outer block to blocks_to_filter
                    else:
                        if seq_blocks[smallblock_index] not in blocks_to_filter:
                            blocks_to_filter.append(seq_blocks[smallblock_index]) # add the inner block to blocks_to_filter
                elif start <= seq_blocks[smallblock_index][2] and end >= seq_blocks[smallblock_index][3]: # does this get triggered too (if they are both equal)
                    if seq_blocks[smallblock_index] not in blocks_to_filter:
                        blocks_to_filter.append(seq_blocks[smallblock_index])
                elif start <= seq_blocks[smallblock_index][2] and end == seq_blocks[smallblock_index][3]:
                    if seq_blocks[smallblock_index] not in blocks_to_filter:
                        blocks_to_filter.append(seq_blocks[smallblock_index])
                elif start == seq_blocks[smallblock_index][2] and end >= seq_blocks[smallblock_index][3]:
                    if seq_blocks[smallblock_index] not in blocks_to_filter:
                        blocks_to_filter.append(seq_blocks[smallblock_index])
                else:
                    continue
# if two blocks match exactly, take the one with the best e-value

        # create a filtered blocks list by subtracting out blocks from the filtered list ???? WHAT IS THIS ????
    seq_blocks_kept = [x for x in seq_blocks if x not in blocks_to_filter]

    # sort blocks from 5' to 3' to prepare for resolving overlaps
    seq_blocks_kept = sorted(seq_blocks_kept, key=lambda x: (x[4], x[2]))

    return seq_blocks_kept

    # loop through the blocks (making sure to stop at the last block)
    # if block A ends after the start of block B, update the start/end of each block to be the average of the overlap
    # also update the length of the block (used for making the figure)
def write_svg(barcode_seq_blocks_filtered, barcode_ID, seq_length):
    for block in range(len(barcode_seq_block_filtered)):
        # end = seq_blocks_filtered[block][3]
        if block < len(barcode_seq_block_filtered) - 1:
            if barcode_seq_blocks_filtered[block][3] > barcode_seq_blocks_filtered[block + 1][2]:
                junction_position = (barcode_seq_blocks_filtered[block][3] + barcode_seq_blocks_filtered[block + 1][2]) / 2
                barcode_seq_blocks_filtered[block][3] = junction_position - 1
                barcode_seq_blocks_filtered[block][1] = barcode_seq_blocks_filtered[block][3] - barcode_seq_blocks_filtered[block][2] + 1
                barcode_seq_blocks_filtered[block + 1][2] = junction_position
                barcode_seq_blocks_filtered[block + 1][1] = barcode_seq_blocks_filtered[block + 1][3] - barcode_seq_blocks_filtered[block + 1][2] + 1

        # initialize the svg file with a filename and resolution
    svg_document = svgwrite.Drawing(filename=barcode_ID + "_v0.5.svg",
                                    size=(str(seq_length + 100) + "px", "48px"))

    # add a black bar to represent the full length gene
    svg_document.add(svg_document.rect(insert=(100, 15),
                                       size=(str(seq_length) + "px", "16px"),
                                       fill="black"))

    # draw a rectangle of the correct size and shape for each sequence block
    offset = 0
    for block in range(len(barcode_seq_block_filtered)):
        svg_document.add(svg_document.rect(insert=(barcode_seq_block_filtered[block][2] + 100, offset),
                                           size=(str(barcode_seq_block_filtered[block][1]) + 'px', "48px"),
                                           stroke_width="1",
                                           stroke="black",
                                           fill=color_palette[barcode_seq_block_filtered[block][0]]))
    # offset += 12

    svg_document.add(svg_document.text(barcode_ID, insert=(5, 30)))

    svg_document.save()

cwdfiles = os.listdir('.')

seq_name_array = []
seq_length_array = []
cwdfile = 'query.fasta'

seq_info = fasta_length_parser(cwdfile)
seq_name_array = seq_info[0]
seq_length_array = seq_info[1]
global_seq_blocks_kept = shuffled_blocks_analysis(cwdfile)


for i in range(len(barcode_list)):
    barcode_seq_block_filtered = []
    for j in range(len(global_seq_blocks_kept)):
        if global_seq_blocks_kept[j][4] == i:
            barcode_seq_block_filtered.append(global_seq_blocks_kept[j])
    write_svg(barcode_seq_block_filtered, seq_name_array[i], seq_length_array[i])
