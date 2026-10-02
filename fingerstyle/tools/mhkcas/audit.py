# Print every note of the .tg with its chord and flag non-chord tones (!)
import zipfile, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
T=[64,59,55,50,45,40]; Q=2882880; M=4*Q; E8=Q//2
NM='C C# D D# E F F# G G# A A# B'.split()
x=zipfile.ZipFile(os.path.join(HERE, 'mhkcas_capo6.tg')).read('content.xml').decode()
CH={'G':'G B D','D/F#':'D F# A','Em7':'E G B D','Cmaj7':'C E G B','D':'D F# A','G/E7':None,'E7':'E G# B D',
    'Am7':'A C E G','D7':'D F# A C','Bm7':'B D F# A','D#7':'D# G A# C#','Cm':'C D# G','B7':'B D# F# A'}
PLAN={2:[(0,'G')],3:[(0,'D/F#')],4:[(0,'Em7')],5:[(0,'Em7')],6:[(0,'Cmaj7')],7:[(0,'D')],8:[(0,'G'),(4,'E7')],9:[(0,'Am7')],
 10:[(0,'D')],11:[(0,'D7')],12:[(0,'Bm7'),(4,'Em7')],13:[(0,'E7')],14:[(0,'Am7')],15:[(0,'Am7')],16:[(0,'D')],17:[(0,'D')],
 18:[(0,'Cmaj7'),(4,'Cm')],19:[(0,'Cm')],20:[(0,'Bm7')],21:[(0,'Em7'),(6,'E7')],22:[(0,'Am7')],23:[(0,'Am7')],24:[(0,'D')]}
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
