import ctypes as ct
P=ct.c_void_p;I=ct.c_int;F=ct.c_double;S=ct.c_char_p
def bind(lib,name,ret,*args):
 f=getattr(ct.CDLL(lib),name);f.restype=ret;f.argtypes=args;return f
def ca(n,r,*a):return bind('libcairo.so.2','cairo_'+n,r,*a)
def pa(n,r,*a):return bind('libpango-1.0.so.0','pango_'+n,r,*a)
pdf=ca('pdf_surface_create',P,S,F,F);create=ca('create',P,P);color=ca('set_source_rgb',None,P,F,F,F);mov=ca('move_to',None,P,F,F);showpage=ca('show_page',None,P);finish=ca('surface_finish',None,P)
lay=bind('libpangocairo-1.0.so.0','pango_cairo_create_layout',P,P);show=bind('libpangocairo-1.0.so.0','pango_cairo_show_layout',None,P,P)
desc=pa('font_description_from_string',P,S);fs=pa('font_description_set_absolute_size',None,P,F);sf=pa('layout_set_font_description',None,P,P);width=pa('layout_set_width',None,P,I);text_=pa('layout_set_text',None,P,S,I);align_=pa('layout_set_alignment',None,P,I);direction=pa('context_set_base_dir',None,P,I);auto=pa('layout_set_auto_dir',None,P,I);ctx=pa('layout_get_context',P,P);getsz=pa('layout_get_size',None,P,ct.POINTER(I),ct.POINTER(I))
surf=pdf(b'tmp/ar/text.pdf',450,890);cr=create(surf);layout=lay(cr);direction(ctx(layout),1);auto(layout,0);fonts=[desc(b'DejaVu Sans'),desc(b'DejaVu Sans Bold')]
def put(x,y,X,Y,s,size,b,c,alignment):
 text_(layout,s.encode(),-1);width(layout,int((X-x)*1024));align_(layout,1 if alignment=='center' else 2);w=I();h=I()
 while True:
  fs(fonts[b],size*1024);sf(layout,fonts[b]);getsz(layout,ct.byref(w),ct.byref(h))
  if h.value/1024<=Y-y or size<=6:break
  size-=.25
 color(cr,*c);mov(cr,x,y+(Y-y-h.value/1024)/2);show(cr,layout)
 return size
