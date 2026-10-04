# Print every note of the .tg with its chord and flag non-chord tones (!)
import zipfile, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
T=[64,59,55,50,45,40]; Q=2882880; M=4*Q; E8=Q//2
NM='C C# D D# E F F# G G# A A# B'.split()
x=zipfile.ZipFile(os.path.join(HERE, 'mhkcas_capo1.tg')).read('content.xml').decode()
CH={'C':'C E G','G/B':'G B D','Am7':'A C E G','Fmaj7':'F A C E','G':'G B D','A7':'A C# E G',
    'Dm7':'D F A C','G7':'G B D F','Em7':'E G B D','Fm':'F G# C'}
PLAN={2:[(0,'C')],3:[(0,'G/B')],4:[(0,'Am7')],5:[(0,'Am7')],6:[(0,'Fmaj7')],7:[(0,'G')],8:[(0,'C'),(4,'A7')],9:[(0,'Dm7')],
 10:[(0,'G')],11:[(0,'G7')],12:[(0,'Em7'),(4,'Am7')],13:[(0,'A7')],14:[(0,'Dm7')],15:[(0,'Dm7')],16:[(0,'G')],17:[(0,'G')],
 18:[(0,'Fmaj7'),(4,'Fm')],19:[(0,'Fm')],20:[(0,'Em7')],21:[(0,'Am7'),(6,'A7')],22:[(0,'Dm7')],23:[(0,'Dm7')],24:[(0,'G')]}
def chord_at(m,t):
    c=None
    for p,n in PLAN.get(m,[]):
        if p<=t: c=n
    return c
ms=re.findall(r'<TGMeasure>(.*?)</TGMeasure>',x,re.S)
DV={'1':8,'2':4,'4':2,'8':1}
for mi,mx in enumerate(ms):
    m=mi+1; lines=[]
    for bt in re.findall(r'<TGBeat>(.*?)</TGBeat>',mx,re.S):
        t=(int(re.search(r'<preciseStart>(\d+)',bt).group(1))-Q-mi*M)//E8
        for vi,v in enumerate(re.findall(r'<voice([^>]*)>(.*?)</voice>',bt,re.S)):
            if 'empty="true"' in v[0]: continue
            d=re.search(r'<duration( dotted="dotted")? value="(\d+)"',v[1]); ln=DV[d.group(2)]*(1.5 if d.group(1) else 1)
            ns=re.findall(r'<note string="(\d)"( tiedNote="true")? value="(\d+)" velocity="(\d+)"(/>|>(.*?)</note>)',v[1])
            if not ns: continue
            c=chord_at(m,t); tones=CH[c].split() if c else []
            out=[]
            for i,(s,tie,f,vel,_,fx) in enumerate(ns):
                s=int(s); f=int(f)
                if 'deadNote' in fx: out.append(f's{s}X'); continue
                p=T[s-1]+f; nm=NM[p%12]
                role='M' if (vi==0 and i==0) else ('B' if vi==1 else 'h')
                flag='' if (nm in tones or role=='M') else '!'
                out.append(f"{role}:s{s}f{f}={nm}{p//12-1}{flag}{'~' if tie else ''}{'h' if 'hammer' in (fx or '') else ''}")
            lines.append(f"  t{t} v{vi} len{ln:g} [{c}] "+' '.join(out))
    print(f"M{m}"); print('\n'.join(lines))
