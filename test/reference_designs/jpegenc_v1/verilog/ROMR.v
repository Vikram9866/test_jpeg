// File: ROMR.v
// Generated by MyHDL 0.9dev
// Date: Wed Oct 29 21:29:29 2014


`timescale 1ns/10ps

module ROMR (
    addr,
    clk,
    datao
);


input [7:0] addr;
input clk;
output [15:0] datao;
reg [15:0] datao;

reg [7:0] raddr;





always @(posedge clk) begin: ROMR_RTL_ADDR
    raddr <= addr;
end


always @(raddr) begin: ROMR_RTL_OUT
    case (raddr)
        0: datao = 0;
        1: datao = 65535;
        2: datao = 32768;
        3: datao = 21845;
        4: datao = 16384;
        5: datao = 13107;
        6: datao = 10923;
        7: datao = 9362;
        8: datao = 8192;
        9: datao = 7282;
        10: datao = 6554;
        11: datao = 5958;
        12: datao = 5461;
        13: datao = 5041;
        14: datao = 4681;
        15: datao = 4369;
        16: datao = 4096;
        17: datao = 3855;
        18: datao = 3641;
        19: datao = 3449;
        20: datao = 3277;
        21: datao = 3121;
        22: datao = 2979;
        23: datao = 2849;
        24: datao = 2731;
        25: datao = 2621;
        26: datao = 2521;
        27: datao = 2427;
        28: datao = 2341;
        29: datao = 2260;
        30: datao = 2185;
        31: datao = 2114;
        32: datao = 2048;
        33: datao = 1986;
        34: datao = 1928;
        35: datao = 1872;
        36: datao = 1820;
        37: datao = 1771;
        38: datao = 1725;
        39: datao = 1680;
        40: datao = 1638;
        41: datao = 1598;
        42: datao = 1560;
        43: datao = 1524;
        44: datao = 1489;
        45: datao = 1456;
        46: datao = 1425;
        47: datao = 1394;
        48: datao = 1365;
        49: datao = 1337;
        50: datao = 1311;
        51: datao = 1285;
        52: datao = 1260;
        53: datao = 1237;
        54: datao = 1214;
        55: datao = 1192;
        56: datao = 1170;
        57: datao = 1150;
        58: datao = 1130;
        59: datao = 1111;
        60: datao = 1092;
        61: datao = 1074;
        62: datao = 1057;
        63: datao = 1040;
        64: datao = 1024;
        65: datao = 1008;
        66: datao = 993;
        67: datao = 978;
        68: datao = 964;
        69: datao = 950;
        70: datao = 936;
        71: datao = 923;
        72: datao = 910;
        73: datao = 898;
        74: datao = 886;
        75: datao = 874;
        76: datao = 862;
        77: datao = 851;
        78: datao = 840;
        79: datao = 830;
        80: datao = 819;
        81: datao = 809;
        82: datao = 799;
        83: datao = 790;
        84: datao = 780;
        85: datao = 771;
        86: datao = 762;
        87: datao = 753;
        88: datao = 745;
        89: datao = 736;
        90: datao = 728;
        91: datao = 720;
        92: datao = 712;
        93: datao = 705;
        94: datao = 697;
        95: datao = 690;
        96: datao = 683;
        97: datao = 676;
        98: datao = 669;
        99: datao = 662;
        100: datao = 655;
        101: datao = 649;
        102: datao = 643;
        103: datao = 636;
        104: datao = 630;
        105: datao = 624;
        106: datao = 618;
        107: datao = 612;
        108: datao = 607;
        109: datao = 601;
        110: datao = 596;
        111: datao = 590;
        112: datao = 585;
        113: datao = 580;
        114: datao = 575;
        115: datao = 570;
        116: datao = 565;
        117: datao = 560;
        118: datao = 555;
        119: datao = 551;
        120: datao = 546;
        121: datao = 542;
        122: datao = 537;
        123: datao = 533;
        124: datao = 529;
        125: datao = 524;
        126: datao = 520;
        127: datao = 516;
        128: datao = 512;
        129: datao = 508;
        130: datao = 504;
        131: datao = 500;
        132: datao = 496;
        133: datao = 493;
        134: datao = 489;
        135: datao = 485;
        136: datao = 482;
        137: datao = 478;
        138: datao = 475;
        139: datao = 471;
        140: datao = 468;
        141: datao = 465;
        142: datao = 462;
        143: datao = 458;
        144: datao = 455;
        145: datao = 452;
        146: datao = 449;
        147: datao = 446;
        148: datao = 443;
        149: datao = 440;
        150: datao = 437;
        151: datao = 434;
        152: datao = 431;
        153: datao = 428;
        154: datao = 426;
        155: datao = 423;
        156: datao = 420;
        157: datao = 417;
        158: datao = 415;
        159: datao = 412;
        160: datao = 410;
        161: datao = 407;
        162: datao = 405;
        163: datao = 402;
        164: datao = 400;
        165: datao = 397;
        166: datao = 395;
        167: datao = 392;
        168: datao = 390;
        169: datao = 388;
        170: datao = 386;
        171: datao = 383;
        172: datao = 381;
        173: datao = 379;
        174: datao = 377;
        175: datao = 374;
        176: datao = 372;
        177: datao = 370;
        178: datao = 368;
        179: datao = 366;
        180: datao = 364;
        181: datao = 362;
        182: datao = 360;
        183: datao = 358;
        184: datao = 356;
        185: datao = 354;
        186: datao = 352;
        187: datao = 350;
        188: datao = 349;
        189: datao = 347;
        190: datao = 345;
        191: datao = 343;
        192: datao = 341;
        193: datao = 340;
        194: datao = 338;
        195: datao = 336;
        196: datao = 334;
        197: datao = 333;
        198: datao = 331;
        199: datao = 329;
        200: datao = 328;
        201: datao = 326;
        202: datao = 324;
        203: datao = 323;
        204: datao = 321;
        205: datao = 320;
        206: datao = 318;
        207: datao = 317;
        208: datao = 315;
        209: datao = 314;
        210: datao = 312;
        211: datao = 311;
        212: datao = 309;
        213: datao = 308;
        214: datao = 306;
        215: datao = 305;
        216: datao = 303;
        217: datao = 302;
        218: datao = 301;
        219: datao = 299;
        220: datao = 298;
        221: datao = 297;
        222: datao = 295;
        223: datao = 294;
        224: datao = 293;
        225: datao = 291;
        226: datao = 290;
        227: datao = 289;
        228: datao = 287;
        229: datao = 286;
        230: datao = 285;
        231: datao = 284;
        232: datao = 282;
        233: datao = 281;
        234: datao = 280;
        235: datao = 279;
        236: datao = 278;
        237: datao = 277;
        238: datao = 275;
        239: datao = 274;
        240: datao = 273;
        241: datao = 272;
        242: datao = 271;
        243: datao = 270;
        244: datao = 269;
        245: datao = 267;
        246: datao = 266;
        247: datao = 265;
        248: datao = 264;
        249: datao = 263;
        250: datao = 262;
        251: datao = 261;
        252: datao = 260;
        253: datao = 259;
        254: datao = 258;
        default: datao = 257;
    endcase
end

endmodule
