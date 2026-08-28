from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Exact live backup before modification.
b=Path('backups/index-before-forged-v4-2026-08-27.html')
b.parent.mkdir(parents=True,exist_ok=True)
b.write_text(s)

# Expand Rugged + Field menu.
pat=r'<optgroup label="Rugged \+ Field">\s*<option value="rugged">Rugged Handheld</option>\s*</optgroup>'
grp='''<optgroup label="Rugged + Field">
          <option value="rugged">Rugged Handheld — Olive Drab</option>
          <option value="ruggedWoodland">Woodland Camo</option>
          <option value="ruggedDesert">Desert Camo</option>
          <option value="ruggedUrban">Urban Camo</option>
          <option value="ruggedNavy">Digital Navy</option>
          <option value="ruggedPixelWood">Pixel Woodland</option>
          <option value="ruggedPixelDesert">Pixel Desert</option>
          <option value="ruggedOcp">OCP-Inspired</option>
          <option value="ruggedBlack">Black Camo</option>
        </optgroup>'''
s,n=re.subn(pat,grp,s,count=1)
if n!=1: raise SystemExit('Rugged optgroup anchor missing')

# Add theme palette records.
anchor='    oldradio:{'
cfg='''    ruggedWoodland:{accent:'#7f8b63',light:'#aeb898',dark:'#333b28',rgb:'127,139,99',themeColor:'#303729',selected:'#071008'},
    ruggedDesert:{accent:'#b5a27a',light:'#d1c49f',dark:'#66563d',rgb:'181,162,122',themeColor:'#554936',selected:'#151109'},
    ruggedUrban:{accent:'#8d9695',light:'#c3c9c8',dark:'#3b4141',rgb:'141,150,149',themeColor:'#2e3434',selected:'#080a0a'},
    ruggedNavy:{accent:'#718497',light:'#a7b4c0',dark:'#283441',rgb:'113,132,151',themeColor:'#1d2731',selected:'#071018'},
    ruggedPixelWood:{accent:'#788460',light:'#a4ad8c',dark:'#303727',rgb:'120,132,96',themeColor:'#2b3226',selected:'#071008'},
    ruggedPixelDesert:{accent:'#b4a17e',light:'#d0c3a3',dark:'#65563e',rgb:'180,161,126',themeColor:'#514735',selected:'#151109'},
    ruggedOcp:{accent:'#93906a',light:'#bab58c',dark:'#4b4a31',rgb:'147,144,106',themeColor:'#3c3d2c',selected:'#0d0d08'},
    ruggedBlack:{accent:'#6e7772',light:'#9aa19e',dark:'#171b19',rgb:'110,119,114',themeColor:'#101312',selected:'#eef2ef'},
'''
if anchor not in s: raise SystemExit('Theme config anchor missing')
s=s.replace(anchor,cfg+anchor,1)

old="const signatureThemes=['steampunk','artdeco','arcade','synthwave','atomic','oldradio','rugged'];"
new="const signatureThemes=['steampunk','artdeco','arcade','synthwave','atomic','oldradio','rugged','ruggedWoodland','ruggedDesert','ruggedUrban','ruggedNavy','ruggedPixelWood','ruggedPixelDesert','ruggedOcp','ruggedBlack'];"
if old not in s: raise SystemExit('Signature theme anchor missing')
s=s.replace(old,new,1)

css=r'''
    /* Rugged v3 cleanup: sharper ribs, olive-drab base, no duplicate FIELD TIMER label. */
    body.theme-rugged{background:radial-gradient(ellipse at 50% -8%,rgba(255,255,255,.055),transparent 43%),linear-gradient(155deg,#51583a 0%,#41492f 43%,#303621 100%)!important}
    body[class*="theme-rugged"] .stage::before{content:none!important}
    body.theme-rugged::before,body.theme-rugged::after,body[class*="theme-rugged"]::before,body[class*="theme-rugged"]::after{width:12px!important;background:repeating-linear-gradient(0deg,#131712 0 8px,#313a2b 8px 13px,#515b43 13px 15px,#1b2118 15px 23px)!important;box-shadow:inset 1px 0 0 rgba(255,255,255,.05),inset -2px 0 0 rgba(0,0,0,.55)!important;filter:none!important;opacity:1!important}
    body[class*="theme-rugged"] .stage{border:2px solid #10130e;background:linear-gradient(180deg,rgba(255,255,255,.028),transparent 18%),linear-gradient(180deg,rgba(25,31,23,.97),rgba(11,15,11,.98));box-shadow:inset 0 0 0 2px rgba(150,160,130,.08),inset 0 -8px 16px rgba(0,0,0,.42),0 2px 0 rgba(107,118,86,.58),0 6px 0 #151a12,0 10px 18px rgba(0,0,0,.35)}
    body[class*="theme-rugged"] .dial{border:5px solid #090b08;background:radial-gradient(circle at 48% 38%,rgba(110,125,95,.08),transparent 43%),radial-gradient(circle,#10140f 0 58%,#070907 76%)}
    body[class*="theme-rugged"] .steel-btn,body[class*="theme-rugged"] .mode-tab{border-color:#020302;background:radial-gradient(ellipse at 50% 15%,rgba(255,255,255,.07),transparent 38%),linear-gradient(180deg,#222622 0%,#111411 48%,#070907 100%);color:#eef2eb}
    body[class*="theme-rugged"] .panel{border-color:rgba(18,23,16,.92);background:linear-gradient(180deg,rgba(255,255,255,.025),rgba(0,0,0,.12)),rgba(46,55,39,.95)}

    /* Original camouflage artwork; field-inspired rather than copied official patterns. */
    body.theme-ruggedWoodland{background:radial-gradient(ellipse at 18% 15%,#1d2b18 0 8%,transparent 9%),radial-gradient(ellipse at 70% 20%,#53623d 0 11%,transparent 12%),radial-gradient(ellipse at 34% 46%,#22271b 0 12%,transparent 13%),radial-gradient(ellipse at 82% 58%,#6c7351 0 10%,transparent 11%),radial-gradient(ellipse at 48% 78%,#182119 0 13%,transparent 14%),linear-gradient(145deg,#3d472f,#727454);background-size:180px 150px,210px 170px,170px 145px,220px 160px,200px 175px,auto}
    body.theme-ruggedDesert{background:radial-gradient(ellipse at 20% 18%,#8d7754 0 9%,transparent 10%),radial-gradient(ellipse at 72% 23%,#d0bb8b 0 12%,transparent 13%),radial-gradient(ellipse at 38% 55%,#725f44 0 10%,transparent 11%),radial-gradient(ellipse at 82% 68%,#b79b6a 0 11%,transparent 12%),linear-gradient(145deg,#a48b63,#c5ae81);background-size:190px 155px,225px 180px,180px 150px,230px 180px,auto}
    body.theme-ruggedUrban{background:radial-gradient(ellipse at 18% 18%,#1a1e1d 0 10%,transparent 11%),radial-gradient(ellipse at 68% 22%,#6c7372 0 12%,transparent 13%),radial-gradient(ellipse at 35% 58%,#343b3a 0 12%,transparent 13%),radial-gradient(ellipse at 82% 70%,#909695 0 9%,transparent 10%),linear-gradient(145deg,#292e2e,#5f6766);background-size:190px 160px,220px 175px,175px 150px,225px 180px,auto}
    body.theme-ruggedNavy{background-color:#26323d;background-image:linear-gradient(45deg,#18212a 25%,transparent 25%,transparent 75%,#18212a 75%),linear-gradient(45deg,#435566 25%,transparent 25%,transparent 75%,#435566 75%),linear-gradient(45deg,transparent 42%,#6f7d88 42% 58%,transparent 58%);background-size:24px 24px,24px 24px,32px 32px;background-position:0 0,12px 12px,5px 9px}
    body.theme-ruggedPixelWood{background-color:#394230;background-image:linear-gradient(90deg,transparent 50%,#1f291d 50%),linear-gradient(0deg,transparent 50%,#66704f 50%),linear-gradient(90deg,transparent 50%,rgba(121,127,86,.8) 50%);background-size:26px 18px,18px 26px,44px 30px;background-position:0 0,6px 4px,11px 8px}
    body.theme-ruggedPixelDesert{background-color:#aa956d;background-image:linear-gradient(90deg,transparent 50%,#766447 50%),linear-gradient(0deg,transparent 50%,#d0bb8d 50%),linear-gradient(90deg,transparent 50%,rgba(142,119,82,.85) 50%);background-size:26px 18px,18px 26px,44px 30px;background-position:0 0,6px 4px,11px 8px}
    body.theme-ruggedOcp{background:radial-gradient(ellipse at 15% 18%,#5f6845 0 8%,transparent 9%),radial-gradient(ellipse at 65% 23%,#a79e73 0 10%,transparent 11%),radial-gradient(ellipse at 38% 55%,#7b704d 0 11%,transparent 12%),radial-gradient(ellipse at 84% 67%,#c2b98c 0 9%,transparent 10%),linear-gradient(140deg,#636749,#99916a);background-size:180px 145px,220px 170px,190px 150px,225px 175px,auto}
    body.theme-ruggedBlack{background:radial-gradient(ellipse at 18% 18%,#050706 0 10%,transparent 11%),radial-gradient(ellipse at 72% 28%,#252a27 0 12%,transparent 13%),radial-gradient(ellipse at 38% 58%,#111513 0 12%,transparent 13%),radial-gradient(ellipse at 82% 72%,#3b413e 0 10%,transparent 11%),linear-gradient(145deg,#111412,#282d2a);background-size:190px 160px,220px 175px,175px 150px,225px 180px,auto}

    /* Rugged v4 forged/rubber refinement. */
    body[class*="theme-rugged"] .app{position:relative;isolation:isolate}
    body[class*="theme-rugged"] .app::before,body[class*="theme-rugged"] .app::after{content:"";position:fixed;top:86px;bottom:20px;width:2px;z-index:0;pointer-events:none;background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(0,0,0,.55) 18%,rgba(255,255,255,.03) 55%,rgba(0,0,0,.62));box-shadow:0 0 0 1px rgba(0,0,0,.24),1px 0 0 rgba(255,255,255,.035);opacity:.72}
    body[class*="theme-rugged"] .app::before{left:20px}body[class*="theme-rugged"] .app::after{right:20px}
    body[class*="theme-rugged"] .brand{position:relative}body[class*="theme-rugged"] .theme-bar{position:relative}
    body[class*="theme-rugged"] .brand::before,body[class*="theme-rugged"] .brand::after,body[class*="theme-rugged"] .theme-bar::before,body[class*="theme-rugged"] .theme-bar::after{content:"";position:absolute;width:8px;height:8px;border-radius:50%;pointer-events:none;background:linear-gradient(45deg,transparent 44%,rgba(0,0,0,.75) 45% 55%,transparent 56%),radial-gradient(circle at 35% 30%,rgba(255,255,255,.45) 0 7%,#7c847c 10% 25%,#343a35 28% 56%,#111412 60% 100%);box-shadow:inset 0 0 0 1px rgba(255,255,255,.07),0 1px 2px rgba(0,0,0,.75);opacity:.9;z-index:4}
    body[class*="theme-rugged"] .brand::before{left:8px;top:7px}body[class*="theme-rugged"] .brand::after{right:8px;top:7px}body[class*="theme-rugged"] .theme-bar::before{left:7px;bottom:8px}body[class*="theme-rugged"] .theme-bar::after{right:7px;bottom:8px}
    body[class*="theme-rugged"] .mode-tabs,body[class*="theme-rugged"] .stage,body[class*="theme-rugged"] .panel,body[class*="theme-rugged"] .main-controls{position:relative}
    body[class*="theme-rugged"] .mode-tabs{border-radius:18px;padding:4px;background:linear-gradient(180deg,rgba(255,255,255,.025),transparent 16%),rgba(7,10,8,.72);box-shadow:inset 0 3px 7px rgba(0,0,0,.70),inset 0 -1px 0 rgba(255,255,255,.035),0 1px 0 rgba(132,145,116,.20)}
    body[class*="theme-rugged"] .panel{outline:1px solid rgba(0,0,0,.45);outline-offset:3px;box-shadow:inset 0 1px 0 rgba(255,255,255,.04),inset 0 -6px 12px rgba(0,0,0,.18),0 0 0 3px rgba(13,17,12,.50),0 5px 0 rgba(9,12,8,.65),0 10px 18px rgba(0,0,0,.25)}
    body[class*="theme-rugged"] .main-controls{border-radius:18px;padding:4px;background:rgba(10,13,10,.28);box-shadow:inset 0 2px 6px rgba(0,0,0,.42),inset 0 -1px 0 rgba(255,255,255,.025)}
    body[class*="theme-rugged"] .dial{box-shadow:inset 0 0 0 2px rgba(122,136,111,.18),inset 0 0 0 7px #070907,inset 0 0 22px rgba(0,0,0,.86),inset 0 3px 3px rgba(255,255,255,.025),0 2px 0 rgba(112,124,95,.50),0 6px 0 #10140f,0 11px 18px rgba(0,0,0,.48)!important}
    body[class*="theme-rugged"] .dial::before{content:"";position:absolute;inset:-12px;border-radius:50%;pointer-events:none;border:2px solid rgba(18,23,16,.95);box-shadow:inset 0 1px 0 rgba(255,255,255,.055),0 0 0 3px rgba(75,88,66,.28),0 4px 7px rgba(0,0,0,.38)}
    body[class*="theme-rugged"] .steel-btn,body[class*="theme-rugged"] .mode-tab,body[class*="theme-rugged"] .main-btn{border-radius:13px;outline:1px solid rgba(0,0,0,.58);outline-offset:2px;box-shadow:inset 0 1px 1px rgba(255,255,255,.07),inset 0 -5px 8px rgba(0,0,0,.72),0 0 0 2px rgba(41,49,38,.40),0 4px 0 rgba(4,6,4,.95),0 7px 10px rgba(0,0,0,.30)}
    body[class*="theme-rugged"] .steel-btn:active,body[class*="theme-rugged"] .mode-tab:active,body[class*="theme-rugged"] .main-btn:active{transform:translateY(2px);box-shadow:inset 0 3px 6px rgba(0,0,0,.78),0 0 0 2px rgba(31,37,29,.45),0 2px 0 rgba(4,6,4,.95)}
    body[class*="theme-rugged"]::before,body[class*="theme-rugged"]::after{width:14px!important;background:linear-gradient(90deg,rgba(255,255,255,.04),transparent 34%,rgba(0,0,0,.30) 78%),repeating-linear-gradient(0deg,#111511 0 7px,#2c3528 7px 11px,#596249 11px 13px,#1a2018 13px 21px)!important;box-shadow:inset 1px 0 0 rgba(255,255,255,.05),inset -3px 0 4px rgba(0,0,0,.65)!important}
    body.theme-ruggedDesert .brand::before,body.theme-ruggedDesert .brand::after,body.theme-ruggedPixelDesert .brand::before,body.theme-ruggedPixelDesert .brand::after{filter:sepia(.35) brightness(1.10)}
    body.theme-ruggedUrban .brand::before,body.theme-ruggedUrban .brand::after,body.theme-ruggedBlack .brand::before,body.theme-ruggedBlack .brand::after{filter:brightness(.68)}
'''

if '</style>' not in s: raise SystemExit('Style close missing')
s=s.replace('</style>',css+'\n  </style>',1)
p.write_text(s)
