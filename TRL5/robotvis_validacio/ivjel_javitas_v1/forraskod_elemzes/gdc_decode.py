import struct, sys
TOK = ("EMPTY IDENTIFIER CONSTANT self BUILT_IN_TYPE BUILT_IN_FUNC in == != < <= > >= and or not + - * / % << >> = += -= *= /= %= <<= >>= &= |= ^= & | ^ ~ "
       "if elif else for while break continue pass return match func class class_name extends is onready tool static export setget const var as void enum preload assert yield signal breakpoint "
       "remote sync master slave puppet remotesync mastersync puppetsync [ ] { } ( ) , ; . ? : $ -> NEWLINE PI TAU _ INF NAN ERROR EOF CURSOR").split()
TYPES = "Nil bool int float String Vector2 Rect2 Vector3 Transform2D Plane Quat AABB Basis Transform Color NodePath RID Object Dictionary Array PoolByteArray PoolIntArray PoolRealArray PoolStringArray PoolVector2Array PoolVector3Array PoolColorArray".split()
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def decode(path):
    b=open(path,'rb').read(); assert b[:4]==b'GDSC'
    ver,nid,ncon,nline,ntok=struct.unpack_from('<5I',b,4); o=24
    ids=[]
    for _ in range(nid):
        L=u32(b,o); o+=4; s=bytes(c^0xb6 for c in b[o:o+L]); o+=L; ids.append(s.split(b'\0')[0].decode('utf8','replace'))
    cons=[]
    for _ in range(ncon):
        t=u32(b,o); o+=4; base=t&0xffff; f64=t>>16&1
        if base==0: cons.append('null')
        elif base==1: cons.append('true' if u32(b,o) else 'false'); o+=4
        elif base==2:
            if f64: cons.append(str(struct.unpack_from('<q',b,o)[0])); o+=8
            else: cons.append(str(struct.unpack_from('<i',b,o)[0])); o+=4
        elif base==3:
            if f64: cons.append(repr(struct.unpack_from('<d',b,o)[0])); o+=8
            else: cons.append(repr(round(struct.unpack_from('<f',b,o)[0],6))); o+=4
        elif base==4:
            L=u32(b,o); o+=4; s=b[o:o+L].decode('utf8','replace'); o+=(L+3)//4*4; cons.append(repr(s))
        else: cons.append(f'<const type {base}>'); break
    lines={}
    for _ in range(nline):
        ti,ln=struct.unpack_from('<II',b,o); o+=8; lines[ti]=ln
    out=[]; cur=''
    for i in range(ntok):
        if b[o]&0x80: v=u32(b,o)^0x80; o+=4
        else: v=b[o]; o+=1
        t=v&0xff; p=v>>8; t=t+8 if t>=68 else t  # Pandemonium: no remote/sync/master/... tokens
        name=TOK[t] if t<len(TOK) else f'?{t}'
        if name=='NEWLINE': out.append(cur); cur='\t'*p; continue
        if name=='IDENTIFIER': s=ids[p]
        elif name=='CONSTANT': s=cons[p]
        elif name=='BUILT_IN_TYPE': s=TYPES[p] if p<len(TYPES) else f'type{p}'
        elif name=='BUILT_IN_FUNC': s=f'builtin{p}'
        elif name in ('EOF',): break
        else: s=name
        if cur and not cur.endswith(('\t','(','[','.')) and s not in (')',']',',','.','(',':','[') and not cur.endswith(' ')  : cur+=' '
        cur+=s
    out.append(cur)
    return ver,'\n'.join(out)
if __name__=='__main__':
    v,t=decode(sys.argv[1]); print('# GDSC version',v); print(t)
