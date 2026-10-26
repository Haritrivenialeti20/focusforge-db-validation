from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
OUT=Path('video_frames'); OUT.mkdir(exist_ok=True)
W,H=1280,720; bg='#f5f7f4'; ink='#17222b'; muted='#6e7c83'; green='#18764b'; red='#a34343'; mint='#c9f0d7'; line='#dce4df'; white='#fff'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; f=lambda n,b=False,m=False: ImageFont.truetype(mono if m else (bold if b else reg),n)
def base(k,t,s=''):
 im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im); d.rectangle((0,0,W,74),fill=white); d.rectangle((52,24,92,61),fill=ink); d.text((61,31),'FF',font=f(12,True),fill=white); d.text((112,28),'FOCUSFORGE DATABASE VALIDATION',font=f(14,True),fill=ink); d.text((58,120),k.upper(),font=f(13,True),fill=green); d.text((58,157),t,font=f(40,True)); d.text((60,216),s,font=f(18),fill=muted); return im,d
def save(im,n): im.save(OUT/f'{n:02d}.png')
im,d=base('Challenge 5','Make invalid data impossible','Database constraints protect FocusForge even when the API is bypassed.')
d.rounded_rectangle((70,310,1210,585),radius=20,fill=white,outline=line,width=2)
for x,h,b in [(110,'NOT NULL','required fields'),(440,'UNIQUE','identity'),(770,'CHECK + FK','valid domain + parent')]:
 d.ellipse((x,370,x+62,432),fill=mint); d.text((x+18,387),'✓',font=f(28,True),fill=green); d.text((x,465),h,font=f(18,True),fill=ink); d.text((x,503),b,font=f(15),fill=muted)
save(im,1)
im,d=base('Broken baseline','The original schema accepted anything','Names, emails, priorities, and project references had no database-level protection.')
for y,h,b in [(305,'tasks.title = NULL','unidentifiable work'),(395,'email = alice@email.com again','duplicate login identity'),(485,'priority = 10 or project_id = 999','invalid domain and orphan task')]:
 d.rounded_rectangle((78,y,1200,y+60),radius=11,fill=white,outline=line,width=2); d.text((105,y+19),h,font=f(16,True),fill=red); d.text((650,y+19),b,font=f(16),fill=ink)
save(im,2)
im,d=base('Schema fix','Four constraints at the database boundary','The valid sample data remains unchanged; invalid writes now fail before storage.')
for y,h,b in [(300,'users','name NOT NULL · email NOT NULL UNIQUE'),(390,'projects','project_name NOT NULL'),(480,'tasks','title NOT NULL · priority CHECK 1–5 · project_id FK')]:
 d.rounded_rectangle((78,y,1200,y+60),radius=11,fill=white,outline=line,width=2); d.text((105,y+19),h,font=f(17,True),fill=green); d.text((390,y+19),b,font=f(16),fill=ink)
save(im,3)
im,d=base('Rejection evidence','Each invalid write is rejected','The four artifacts show the expected constraint violation for every test.')
shots=['screenshot_1_not_null.png','screenshot_2_unique.png','screenshot_3_check.png','screenshot_4_foreign_key.png']
for i,fn in enumerate(shots):
 x=90+(i%2)*585; y=300+(i//2)*135; d.rounded_rectangle((x,y,x+520,y+98),radius=12,fill=white,outline=line,width=2); d.text((x+24,y+20),['NOT NULL','UNIQUE','CHECK','FOREIGN KEY'][i],font=f(17,True),fill=red); d.text((x+24,y+58),'PostgreSQL error captured',font=f(14),fill=muted)
save(im,4)
im,d=base('Verification','Valid data passes; invalid data fails','The harness rebuilds a fresh constrained database for each rejection test.')
for i,(h,b) in enumerate([('2 users · 2 projects · 2 tasks','valid sample accepted'),('NULL title','NOT NULL rejected'),('duplicate email','UNIQUE rejected'),('priority 10 · project 999','CHECK + FOREIGN KEY rejected')]):
 y=292+i*68; d.ellipse((100,y,135,y+35),fill=mint); d.text((111,y+7),'✓',font=f(15,True),fill=green); d.text((175,y+4),h,font=f(17,True),fill=ink); d.text((700,y+4),b,font=f(15),fill=green)
save(im,5)
im,d=base('Delivery','Correctness lives in the database','FocusForge now rejects invalid writes from every path, not only from the API.')
d.rounded_rectangle((70,320,1210,560),radius=20,fill=ink)
for i,(a,b) in enumerate([('4 constraints','required, unique, valid, related'),('4 tests','each rejection isolated'),('1 schema','PostgreSQL-ready integrity boundary')]):
 y=360+i*58; d.text((110,y),a,font=f(20,True),fill=mint); d.text((620,y),b,font=f(19),fill=white)
d.text((70,640),'FocusForge · Challenge 5 · DB-Level Validation',font=f(15,True),fill=green); save(im,6)
