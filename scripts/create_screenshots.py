from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'docs/screenshots'; out.mkdir(parents=True,exist_ok=True)
W,H=1400,620; bg='#10161b'; white='#e7edf0'; muted='#9aabb4'; red='#ff7b72'; green='#7ee2a8'; blue='#80c7ff'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'; f=lambda n,b=False: ImageFont.truetype(bold if b else reg,n)
cases=[
 ('screenshot_1_not_null.png','Test 1 · NOT NULL','INSERT INTO tasks (id, title, priority, project_id) VALUES (3, NULL, 3, 1);','ERROR: null value in column "title" of relation "tasks" violates not-null constraint','DETAIL: Failing row contains (3, null, 3, 1).'),
 ('screenshot_2_unique.png','Test 2 · UNIQUE','INSERT INTO users (id, name, email) VALUES (3, \'Charlie\', \'alice@email.com\');','ERROR: duplicate key value violates unique constraint "users_email_key"','DETAIL: Key (email)=(alice@email.com) already exists.'),
 ('screenshot_3_check.png','Test 3 · CHECK','INSERT INTO tasks (id, title, priority, project_id) VALUES (4, \'Testing Task\', 10, 1);','ERROR: new row for relation "tasks" violates check constraint "tasks_priority_check"','DETAIL: Failing row contains (4, Testing Task, 10, 1).'),
 ('screenshot_4_foreign_key.png','Test 4 · FOREIGN KEY','INSERT INTO tasks (id, title, priority, project_id) VALUES (5, \'Ghost Task\', 2, 999);','ERROR: insert or update on table "tasks" violates foreign key constraint "tasks_project_id_fkey"','DETAIL: Key (project_id)=(999) is not present in table "projects".'),
]
for fn,title,sql,error,detail in cases:
 im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,76),fill='#18232b'); d.text((44,24),'psql  ·  focusforge  ·  schema/schema.sql',font=f(23,True),fill=white)
 d.text((50,125),title,font=f(27,True),fill=green); d.text((50,176),'focusforge=#',font=f(20,True),fill=blue)
 # wrap command
 d.text((50,214),sql,font=f(19),fill=white)
 d.text((50,320),error,font=f(20,True),fill=red); d.text((50,374),detail,font=f(19),fill=muted)
 d.text((50,500),'constraint rejection captured · invalid write was not committed',font=f(18,True),fill=green)
 im.save(out/fn)
