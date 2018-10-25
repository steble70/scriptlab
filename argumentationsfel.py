#!\usr\bin\env python

#argumentationsfel.py version 0.1
#(C) 2018 av Stefan

#Valår
#Lägg filen i autostart mappen i Windows 10 (C:\Users\DITT ANVÄNDAR NAMN\
#AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup) så startas
#filen (och dekrypteras) automatiskt varje gång du loggar in och du får veta
#mer om hur politikerna ljuger för dig (exemplen nedan är tagna från Wikipedia
#artikeln "argumentationsfel"). Programmet är ett försök att efterlikna
#Linux/Unix programmet "fortune".

import random
import time
import argparse
import base64

def argumentationsfel():
    print()
    fk = '''RmVsYWt0aWcga29tYmluYXRpb24NCiAgICBBdHQgdHbDpSBmZW5vbWVuIGbDtnJ
    la29tbWVyIHZhciBmw7ZyIHNpZyBiZXR5ZGVyIGludGUgbWVkIG7DtmR2w6RuZGlnaGV0IG
    F0dA0KICAgIGRlIGbDtnJla29tbWVyIHRpbGxzYW1tYW5zLg0KDQogICAgRXhlbXBlbDoNCi
    AgICAtIFZpc3NhIGzDpG5kZXIgaGFyIGVuIGt1bmcuDQogICAgLSBWaXNzYSBsw6RuZGVyIG
    hhciBlbiBwcmVzaWRlbnQuDQogICAgLSBBbGx0c8OlIGhhciB2aXNzYSBsw6RuZGVyIGVuIG
    t1bmcgb2NoIGVuIHByZXNpZGVudC4='''

    sf = '''U3lsbG9naXN0aXNrYSBmZWwNCiAgICBFbiBzeWxsb2dpc20ga2FuIGRpcmVrdCBq
    w6RtZsO2cmFzIG1lZCBlbiBzbHV0bGVkbmluZ3NyZWdlbCwgZGV0IHZpbGwgc8OkZ2ENCiAg
    ICBldHQgc8OkdHQgYXR0IGZyw6VuIHR2w6UgcHJlbWlzc2VyIGRyYSBlbiBzbHV0c2F0cy4g
    QmVncmVwcGV0IGjDpHJzdGFtbWFyIGZyw6VuDQogICAgQXJpc3RvdGVsZXMgb2NoIGhhbnMg
    c3lsbG9naXN0aWsgcsOka25hcyBzb20gZW4gYXYgZGV0IGV4YWt0YSB0w6Rua2FuZGV0cw0K
    ICAgIHN0w7Zyc3RhIHRyaXVtZmVyLg0KDQogICAgRXg6DQogICAgLSBBbGxhIGZvbGllaGF0
    dGFyKiDDpHIga27DpHBwZ8O2a2FyLg0KICAgIC0gQWxsYSBrbsOkcHBnw7ZrYXIgw6RyIGtv
    bnN0aWdhLg0KICAgIC0gQWxsYSBmb2xpZWhhdHRhciDDpHIga29uc3RpZ2EgKHLDpHR0KS4N
    CiAgICAtIEFsbGEga29uc3RpZ2Egw6RyIGZvbGllaGF0dGFyIChmZWwpLg0KDQogICAgKkVu
    IGZvbGllaGF0dCDDpHIgZW4gcGVyc29uIHNvbSB0cm9yIHDDpSBrb25zdGlnYSBrb25zcGly
    YXRpb250ZW9yaWVyLg=='''

    oi = '''T212w6RuZCBpbXBsaWthdGlvbg0KICAgIEV0dCBteWNrZXQgdmFubGlndCBhcmd1
    bWVudGF0aW9uc2ZlbCDDpHIgYXR0IGJsYW5kYSBpaG9wIGFudGVjZWRlbnRlbiBvY2gNCiAg
    ICBrb25zZWt2ZW50ZW4gaSBlbiBpbXBsaWthdGlvbi4NCg0KICAgIEV4Og0KICAgIC0gT20g
    R3VkIGZpbm5zIGthbiBHdWQgc2thcGEgbcOkbm5pc2tvci4NCiAgICAtIE3DpG5uaXNrb3Ig
    ZmlubnMuDQogICAgLSBBbGx0c8OlIGZpbm5zIEd1ZC4='''

    ot = '''T3JzYWsvdGlkc3NhbWJhbmQNCiAgICBQb3N0IGhvYywgcHJvcHRlciBob2MgKGVm
    dGVyIGRldHRhLCBww6UgZ3J1bmQgYXYgZGV0dGEpLCBhdHQgZsO2cnbDpHhsYSBldHQNCiAg
    ICB0aWRzc2FtYmFuZCBtZWQgZXR0IG9yc2Frc3NhbWJhbmQuDQoNCiAgICBFeDogUsOkdnN2
    YW5zZXh0cmFrdCBib3RhciBmw7Zya3lsbmluZy4gSmFnIGhhZGUgdmFyaXQgZ2Vub21mw7Zy
    a3lsZCBpIMO2dmVyDQogICAgICAgIGVuIHZlY2thLCBtZW4gc8OlIMOldCBqYWcgcsOkdnN2
    YW5zZXh0cmFrdCBvY2ggYmxldiBmcmlzayBww6UgdHJlIGRhZ2FyLg=='''

    ds = '''RGVsbmluZyBvY2ggc2FtbWFuc8OkdHRuaW5nIChrb21wb3NpdGlvbikNCiAgICBB
    dHQgaMOkdmRhIGF0dCBkZXQgc29tIGfDpGxsZXIgZGVsYXJuYSBhdiBlbiBoZWxoZXQgb2Nr
    c8OlIGfDpGxsZXIgaGVsaGV0ZW4NCiAgICBvY2ggdmljZSB2ZXJzYS4NCg0KICAgIEV4Og0K
    ICAgIC0gTcOkbm5pc2tvciBoYXIgbWVkdmV0YW5kZS4NCiAgICAtIEVuIGZvdCDDpHIgZW4g
    ZGVsIGF2IGVuIG3DpG5uaXNrYS4NCiAgICAtIEFsbHRzw6UgaGFyIGVuIGZvdCBtZWR2ZXRh
    bmRlLg0KDQogICAgZWxsZXINCg0KICAgIC0gQWxsYSBzb20gcsO2c3RhdCBww6UgTWlsasO2
    cGFydGlldCDDpHIgZsO2ciBkZXJhcyBtaWxqw7Zwb2xpdGlrLg0KICAgIC0gOTAlIGhhciBp
    bnRlIHLDtnN0YXQgcMOlIE1pbGrDtnBhcnRpZXQsIGFsbHRzw6Ugw6RyIDkwJSBlbW90IE1p
    bGrDtnBhcnRpZXRzDQogICAgICBtaWxqw7Zwb2xpdGlrLg=='''

    io = '''SWNrZSByZXByZXNlbnRhdGl2dCB1cnZhbA0KICAgIFZpc2FyIHNpZyBvZnRhIGkg
    Zm9ybSBhdiBhbmVrZG90aXNrIGJldmlzZsO2cmluZy4NCg0KICAgIEV4OiBKYWcga8Okbm5l
    ciBtw6VuZ2EgZ2FtbGEgbcOkbm5pc2tvciBzb20gcsO2a2VyLCBhbGx0c8OlIGthbiBkZXQg
    aW50ZQ0KICAgICAgICBzdMOkbW1hIGF0dCByw7ZrYXJlIGTDtnIgaSBmw7ZydGlkIQ=='''

    ka = '''S29uc2VrdmVuc2FyZ3VtZW50DQogICAgS29uc2VrdmVuc2FyZ3VtZW50IHN0w7Zk
    ZXIgc2lnIHDDpSBhdHQgZGVuIHRlcyBtYW4gc3TDtmRlciBzaWcgcMOlLCBlbGxlciB0cm8N
    CiAgICBww6UgdGVzZW5zIHNhbm5pbmdzaGFsdCwgaW5uZWLDpHIgZ29kYSBrb25zZWt2ZW5z
    ZXIuIEV0dCB2YXJkYWdsaWd0IG5hbW4gcMOlDQogICAgZGV0dGEgYXJndW1lbnRhdGlvbnNm
    ZWwgw6RyICLDtm5za2V0w6Rua2FuZGUiLg0KDQogICAgRXg6DQogICAgLSBWaSB2aWxsIGtv
    bW1hIHRpbGwgaGltbWVscmlrZXQgZWZ0ZXIgZGV0dGEgbGl2Lg0KICAgIC0gQWxsdHPDpSBm
    aW5ucyBoaW1tZWxyaWtldC4='''

    pa = '''UGVyc29uYW5ncmVwcCAtIGFyZ3VtZW50dW0gYWQgaG9taW5lbSAodmFubGlndCBp
    bm9tIHBvbGl0aWtlbikNCg0KICAgIEV4OiBFbiB0am9ja2lzIHNvbSBkdSBza2EgaW50ZSBz
    dMOlIG9jaCBtb3JhbGlzZXJhIMO2dmVyIHZhZCB2aSDDpHRlci4='''

    ta = '''VHUgcXVvcXVlLWFyZ3VtZW50ICh2YW5saWd0IGlub20gcG9saXRpa2VuKQ0KDQog
    ICAgRXg6IFZhcmbDtnIgc2thIGphZyBwbG9ja2EgdW5kYW4gbWluIGRpc2s/IEbDtnJyYSB2
    ZWNrYW4gaGFkZSBkdSBlbiBtYXNzYQ0KICAgICAgICBkaXNrIGZyYW1tZSE='''

    fa = '''Rm9sa2V0cyBhcmd1bWVudCAtIGFyZ3VtZW50dW0gYWQgcG9wdWx1bQ0KDQogICAg
    RXg6IFR2w6UgbWlsamFyZGVyIG3DpG5uaXNrb3Iga2FuIGludGUgaGEgZmVsIC0gS3Jpc3Rl
    bmRvbWVuIMOkciBzYW5uLg=='''

    at = '''QXVrdG9yaXRldHN0cm8gQXJndW1lbnR1bSBhZCB2ZXJlY3VuZGlhbSAoYXJndW1l
    bnQgdGlsbCB2w7ZyZG5hZCkNCg0KICAgIEV4OiAiRmVtIGzDpGthcmUgc2tyZXYgcMOlIERO
    LWRlYmF0dCBhdHQgbGFnZsO2cnNsYWdldCB2YXIgZMOlbGlndCIgLSBBbGx0c8OlDQogICAg
    ICAgIMOkciBsYWdmw7Zyc2xhZ2V0IGTDpWxpZ3QuIMOEdmVuIG9tIGxhZ2bDtnJzbGFnZXQg
    aGFuZGxhciBvbSBiaS1vZGxpbmcsIGbDtnINCiAgICAgICAgdmlsa2V0IG1lZGljaW5za2Eg
    a3Vuc2thcGVyIMOkciBpcnJlbGV2YW50YS4='''

    ga = '''R3VpbHQgYnkgYXNzb2NpYXRpb24NCg0KICAgIEV4Og0KICAgIC0gUGV0ZXIgcsO2
    a2VyIHBpcGEuDQogICAgLSBQZXRlciBsasO2ZyBmw7ZyIG1pZy4NCiAgICAtIEFsbGEgc29t
    IHLDtmtlciBwaXBhIGxqdWdlci4='''

    ha = '''SG9ub3VyIGJ5IGFzc29jaWF0aW9uDQoNCiAgICBFeDoNCiAgICAtIE1vZGVyIFRl
    cmVzYSB2YXIga2F0b2xpayBvY2ggZW4gZ29kIG3DpG5uaXNrYS4NCiAgICAtIEFsbHRzw6Ug
    w6RyIGFsbGEga2F0b2xpa2VyIGdvZGEu'''

    tv = '''VHbDpSBmZWwgZ8O2ciBldHQgcsOkdHQgKHZhbmxpZ3QgYmxhbmQgcG9saXRpa2Vy
    KQ0KICAgIEF0dCBww6VwZWthIGV0dCBwcm9ibGVtIGhvcyBtb3RzdMOlbmRhcmVucyAoZWxs
    ZXIgZW4gdHJlZGplIHBhcnRzKQ0KICAgIHN0w6VuZHB1bmt0IGkgc3TDpGxsZXQgZsO2ciBh
    dHQgYmVtw7Z0YSBldHQgcHJvYmxlbSBob3MgZGVuIGVnbmEuDQoNCiAgICBFeDogRHUga2xh
    bmRyYXIgbWlnIGbDtnIgYXR0IGphZyBoYXIgc3R1bGl0IHR1c2VuIGtyb25vciwgbWVuIGRl
    dCBmaW5ucw0KICAgICAgICBhbmRyYSBzb20gc3R1bGl0IHRpbyBnw6VuZ2VyIHPDpSBteWNr
    ZXQu'''

    ko = '''S29tcGVuc2F0aW9uIC0gYmVsw7ZuaW5nIGVsbGVyIHN0cmFmZg0KDQogICAgRXg6
    IFBvbCBQb3QgYmVvcmRyYWRlIG1hc3Ntb3JkIC0gQWxsdHPDpSBmw7ZydGrDpG5hciBoYW4g
    aW50ZSBhdHQgZmlubmFzDQogICAgICAgIG1lZCBpIHVwcHNsYWdzdmVya2VuLg=='''

    hg = '''SGFsbWd1YmJlICh2YW5saWcgYmxhbmQgcG9saXRpa2VyKQ0KICAgIEVuIGhhbG1n
    dWJiZSAoZW5nLiBzdHJhdyBtYW4pIMOkciBlbiBrYXJpa2F0eXIgYXYgbW90c3TDpW5kYXJl
    bnMgc3TDpW5kcHVua3QsDQogICAgc29tIGRldCDDpHIgbMOkdHRhcmUgYXR0IGFuZ3JpcGEg
    w6RuIGRlbiB2ZXJrbGlnYSBzdMOlbmRwdW5rdGVuLg0KDQogICAgRXg6IEtyaXN0bmEgZGVi
    YXR0w7ZyZXIgw6RyIGtvbnNlcnZhdGl2YSBvY2ggdmlsbCBhbGx0c8OlIHRvdGFsZsO2cmJq
    dWRhIGFib3J0LA0KICAgICAgICBiaW5kYSBrdmlubm9yIHZpZCBzcGlzZW4gb2NoIHN0w6Ru
    Z2EgbmVyIGhlbGEgc2FtaMOkbGxldCBww6Ugc8O2bmRhZ2FybmEu'''

    an = '''w4VsZGVyIG9jaCBueWhldA0KICAgIEF0dCBmw7ZyZXNwcsOla2EvbW90YXJiZXRh
    IG7DpWdvdCBiYXJhIGbDtnIgYXR0IGRldCDDpHIgdW5ndCBlbGxlciBnYW1tYWx0LA0KICAg
    IGkgZGUgZmFsbCBkw6Ugw6VsZGVybiDDpHIgaXJyZWxldmFudC4NCg0KICAgIEV4Og0KICAg
    IC0gUHJvc3RpdHV0aW9uIMOkciB2w6RybGRlbnMgw6RsZHN0YSB5cmtlLg0KICAgIC0gQWxs
    dHPDpSBza2EgcHJvc3RpdHV0aW9uIHRpbGzDpXRhcy4='''

    fb = '''RnLDpW52YXJvbiBhdiBiZXZpcw0KDQogICAgRXg6DQogICAgLSBWZXRlbnNrYXBl
    biBoYXIgYWxkcmlnIGJldmlzYXQgYXR0IHJ5bWR2YXJlbHNlciBpbnRlIGJlc8O2a2VyIGpv
    cmRlbi4NCiAgICAtIEFsbHRzw6UgbGV2ZXIgcnltZHZhcmVsc2VybmEgbWl0dCBpYmxhbmQg
    b3NzLg=='''

    ob = '''T212w6RuZCBiZXZpc2LDtnJkYQ0KDQogICAgRXg6IEphc8OlIGR1IMOkciBlbW90
    IGRlbiBow6RyIHJlZm9ybWVuIHZpIGbDtnJlc2xhZ2l0LiBOw6UsIGJldmlzYSBkw6UgdmFy
    ZsO2cg0KICAgICAgICBkZW4gw6RyIGTDpWxpZy4='''

    fm = '''RnLDpW52YXJvbiBhdiBtb3Rhcmd1bWVudA0KDQogICAgRXg6DQogICAgLSBFZnRl
    ciBmeXJhIHRpbW1hciBoYXIgaGFuIGludGUga29tbWl0IG1lZCBuw6Vnb3Qgc3Zhci4NCiAg
    ICAtIEFsbHRzw6UgaGFyIGphZyByw6R0dC4='''

    sa = '''U3ZhcnR2aXQgYXJndW1lbnRhdGlvbg0KDQogICAgRXg6DQogICAgLSBEdSB2aWxs
    IGludGUgYXR0IHbDpWxkdMOka3RzbcOkbiBza2EgYXZyw6R0dGFzLg0KICAgIC0gQWxsdHPD
    pSB2aWxsIGR1IGF0dCB2w6VsZHTDpGt0c23DpG4gc2thIGfDpSBmcmlhLg=='''

    sp = '''U2x1dHRhbmRlIHBsYW4gKGdpbHRpZ3QgYXJndW1lbnQgb20gaGVsYSBrZWRqYW4g
    aMOlbGxlcikNCg0KICAgIEV4Og0KICAgIC0gQXR0IGbDtnJianVkYSBhZmZpc2NoZXJpbmcg
    cMOlIGVsc2vDpXAgw6RyIGLDtnJqYW4gdGlsbCBjZW5zdXIuDQogICAgLSBDZW5zdXIgbGVk
    ZXIgdGlsbCBmw7ZydHJ5Y2sgb2NoIGbDtnJ0cnljayDDpHIgZXR0IGvDpG5uZXRlY2tlbiBw
    w6UgZGlrdGF0dXIuDQogICAgLSBEaWt0YXR1ciBsZWRlciB0aWxsIGZhdHRpZ2RvbSBvY2gg
    c3bDpGx0IGbDtnIgZm9sa2V0LiBBbGx0c8OlIG3DpXN0ZSBtYW4gZsOlDQogICAgICBzw6R0
    dGEgYWZmaXNjaGVyIHDDpSBlbHNrw6VwLg=='''

    ad = '''QW5wYXNzbmluZyBhdiBkZWZpbml0aW9uL0FkIGhvYw0KDQogICAgRXg6DQogICAg
    LSBBOiBBbGxhIGZlbWluaXN0ZXIgw6RyIHNvY2lhbGlzdGVyLg0KICAgIC0gQjogTWVuIEJp
    cmdpdHRhIE9obHNzb24gw6RyIHbDpGwgaW50ZSBzb2NpYWxpc3Q/DQogICAgLSBBOiBOZWos
    IG1lbiBob24gw6RyIGluZ2VuIHJpa3RpZyBmZW1pbmlzdC4='''

    sl = '''U3ZhZyBsaWtuZWxzZQ0KDQogICAgRXg6DQogICAgLSBKb3JkZW4gw6RyIHNvbSBl
    biBrdmlubmEsIG9jaCBpbmR1c3RyaWVsbCBleHBsb2F0ZXJpbmcgw6RyIHNvbSB2w6VsZHTD
    pGt0Lg0KICAgIC0gVsOlbGR0w6RrdCBww6Uga3Zpbm5vciDDpHIgZmVsLg0KICAgIC0gQWxs
    dHPDpSDDpHIgZXhwbG9hdGVyaW5nIGF2IGpvcmRlbiBmZWwu'''

    lf = '''TGVkYW5kZSBmcsOlZ2EvcHJlc3VwcG9zaXRpb24va29tcGxleCBmcsOlZ2ENCg0K
    ICAgIEV4Og0KICAgIC0gSGFyIGR1IHNsdXRhdCBzbMOlIGRpbiBmcnU/DQogICAgLSDDhHIg
    ZHUgZHVtIGVsbGVyIHNwZWxhciBkdT8NCiAgICAtIEVya8Okbm5lciBkdSBhdHQgZHUgc3Rh
    bCBjeWtlbG4/'''

    ma = '''TWFydHlyYXJndW1lbnQgKHZhbmxpZ3QgYmxhbmQgU0QgcG9saXRpa2VyKQ0KDQog
    ICAgRXg6IEphZyB0w6Rua2VyIGludGUgYmVzdmFyYSBkaW5hIGFyZ3VtZW50IGVmdGVyc29t
    IGphZyBibGlyIHVwcHLDtnJkIG9jaA0KICAgICAgICBuZWRzbGFnZW4gw7Z2ZXIgZGl0dCBz
    w6R0dCBhdHQgZGViYXR0ZXJhLg=='''

    aa = '''QXJndW1lbnR1bSBhZCBuYXVzZWFtDQoNCiAgICBFeDoNCiAgICAtIEd1ZCBmaW5u
    cy4NCiAgICAtIEd1ZCBmaW5ucy4NCiAgICAtIEd1ZCBmaW5ucy4NCg0KICAgIEFsbHRzw6Ug
    ZmlubnMgR3VkLg=='''


    argFel = [fk, sf, oi, ot, ds, io, ka, pa, ta, fa, at, ga, ha, tv,
              ko, hg, an, fb, ob, fm, sa, sp, ad, sl, lf, ma, aa]
    pick_argFel = random.choice(argFel)
    
    return pick_argFel


def main():
    parser = argparse.ArgumentParser(description='Argumentationsfel version 0.1')
    args = parser.parse_args()
    dekryptera = base64.b64decode(argumentationsfel()).decode('UTF-8', 'ignore')
    print(dekryptera)
    time.sleep(20)


if __name__ == '__main__':
    main()
