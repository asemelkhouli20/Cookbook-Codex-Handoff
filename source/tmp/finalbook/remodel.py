from pathlib import Path
p=Path('tmp/finalbook/chapters.py')
s=p.read_text()
s=s.replace("from batchnotes import notes","""from batchnotes import notes
art=grid('a3d0',4,4)
exec(Path('tmp/finalbook/visualguides.py').read_text())
def page(dest,title,ac=GREEN):
 rect(0,0,W,H,PAPER);c.bookmarkPage(dest)
 level=1 if dest.startswith('r') and dest[1:].isdigit() else 0
 if dest in ('pasta','chicken','beef','roast','week','boxes'):level=1
 c.addOutlineEntry(title,dest,level)
 for k in range(30):rect(k*15,720+(k%2)*5,15,5,ac)
""")
s=s.replace(s[s.index('# Preserve the introductory'):s.index('def chapter(j):')],'starter()\n')
s=s.replace(s[s.index("back=source["):],"guides()\nc.save()\n")
start=s.index('  im=actions[key]')
end=s.index('  t(78,y-16',start)
s=s[:start]+"""  storyboard={
   0:[icons['N'],act[0],art[12]],1:[art[2],art[9],new[1]],2:[art[1],act[3],art[9]],
   3:[art[1],icons['E'],new[3]],4:[art[1],art[2],new[4]],5:[art[1],act[3],new[5]],
   6:[icons['S'],art[5],new[6]],7:[art[3],art[6],art[2]],8:[act[10],art[7],new[8]],
   9:[art[1],art[8],new[9]],10:[art[14],art[8],new[10]],11:[icons['L'],art[8],new[11]],
   12:[burg[2],burg[3],new[12]],13:[art[8],art[3],new[13]],14:[art[4],art[2],new[14]],
   15:[art[1],act[14],new[15]],16:[icons['A'],act[14],new[16]],17:[art[3],icons['X'],new[17]],
   18:[art[3],new[18],art[9]],19:[art[2],art[6],new[19]],20:[art[1],art[3],art[9]],
   21:[art[14],art[3],new[21]],22:[art[4],art[2],new[22]],23:[art[4],art[7],new[23]],
   24:[bird[0],bird[3],bird[1]],25:[burg[2],burg[3],burg[0]],26:[icons['N'],new[26]]}
  im=storyboard[i][k];image(im,20,y-bh+5,49,bh-10)
"""+s[end:]
s=s.replace("  t(25,pos,lab,8.5,'B',ac);pos=lines(79,pos,txt,339,size,leading)-6","""  rowimgs={'PREP':art[10],'SERVE':(art[14] if 'reheat' in txt.lower() else new[i]),'KEEP':icons['N'],'STORE':art[13] if rice else art[12]}
  row_h=len(simpleSplit(txt,'S',size,339))*leading
  image(rowimgs[lab],20,pos+6-min(row_h,34),49,min(row_h,34))
  pos=lines(79,pos,txt,339,size,leading)-6""")
# Short labels can be printed on top of the explanatory text column without increasing page density.
s=s.replace("if i==24:c.linkRect('Whole chicken oven guide','roast',(78,329,418,392),thickness=0)","")
s=s.replace("if i==24 and y-height>66:","if i==24 and y-height>62:")
s=s.replace("c.setTitle", "c.setTitle")
Path('tmp/finalbook/illustrated.py').write_text(s)
