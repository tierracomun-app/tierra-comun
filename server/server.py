"""Tierra Común server: static files + /api/chat. No logs of chat content are stored.
NOTE: OPTIONAL. The app no longer needs this server; the default assistant runs offline in the browser. Paid LLM mode only if you set LLM_API_KEY yourself (any OpenAI-compatible endpoint, including a free local Ollama: LLM_BASE_URL=http://localhost:11434/v1).
Env: LLM_API_KEY (or OPENAI_API_KEY), LLM_BASE_URL (default https://api.openai.com/v1), LLM_MODEL (default gpt-4o-mini), PORT (8643)."""
import json,os,re,glob,unicodedata,urllib.request
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY=os.environ.get('LLM_API_KEY') or os.environ.get('OPENAI_API_KEY')
BASE=os.environ.get('LLM_BASE_URL','https://api.openai.com/v1').rstrip('/');MODEL=os.environ.get('LLM_MODEL','gpt-4o-mini')
SYS=open(os.path.join(ROOT,'server','system_prompt.txt'),encoding='utf-8').read()
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
STOP=set('que como hago si me mi en el la los las de del un una y o a por para con es hay se lo what do i if my the a in of to is'.split())
SYN={'detiene':'ice detenido derechos silencio','redada':'ice','desplazamiento':'desplazado desplazados seguridad','masivo':'desplazados','abogado':'abogado pro bono','trabajo':'permiso ead laborales','salud':'emergencia emtala','escuela':'educacion','familia':'familia plan family','notario':'notarios','plazo':'1 año asilo'}
DOCS=[]
for f in glob.glob(os.path.join(ROOT,'data','**','*.json'),recursive=True):
  d=json.load(open(f,encoding='utf-8'))
  for s in d.get('sections',[]) if isinstance(d,dict) else []:
    for L in ('es','en'): DOCS.append({'lang':L,'t':s[L]['t'],'b':s[L]['b'],'src':s['src'],'file':os.path.relpath(f,ROOT)})
def search(q,lang,k=3):
  w=[x for x in re.findall(r'\w+',norm(q)) if x not in STOP]
  w+=sum((SYN[x].split() for x in list(w) if x in SYN),[])
  sc=[]
  for d in DOCS:
    if d['lang']!=lang: continue
    tw=re.findall(r'\w+',norm(d['t']+' '+d['b']));tt=set(re.findall(r'\w+',norm(d['t']))); s=sum(tw.count(x)*(3 if x in tt else 1) for x in set(w) if len(x)>2)
    if s>=2: sc.append((s,d))
  return [d for s,d in sorted(sc,key=lambda x:-x[0])[:k]]
def llm(q,hits,lang):
  ctx='\n\n'.join(f"[{i+1}] {h['t']}: {h['b']} Fuentes: "+'; '.join(f'{a} {u}' for a,u in h['src']) for i,h in enumerate(hits)) or '(sin fragmentos)'
  body={'model':MODEL,'temperature':0.2,'messages':[{'role':'system','content':SYS},{'role':'user','content':f'FRAGMENTOS VERIFICADOS:\n{ctx}\n\nPREGUNTA ({lang}): {q}'}]}
  r=urllib.request.Request(BASE+'/chat/completions',json.dumps(body).encode(),{'Content-Type':'application/json','Authorization':'Bearer '+KEY})
  return json.load(urllib.request.urlopen(r,timeout=60))['choices'][0]['message']['content']
HELP={'es':'Ayuda legal gratuita: lista pro bono de EOIR (https://www.justice.gov/eoir/list-pro-bono-legal-service-providers) o ACNUR (https://help.unhcr.org/). No soy abogado; esto no es asesoría legal.','en':'Free legal help: EOIR pro bono list (https://www.justice.gov/eoir/list-pro-bono-legal-service-providers) or UNHCR (https://help.unhcr.org/). I am not a lawyer; this is not legal advice.'}
class H(SimpleHTTPRequestHandler):
  def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
  def log_message(s,*a): pass  # no request logs (privacy)
  def do_POST(s):
    if s.path!='/api/chat': return s.send_error(404)
    try: j=json.loads(s.rfile.read(min(int(s.headers.get('Content-Length',0)),4000)));q=str(j.get('q',''))[:1000];lang='en' if j.get('lang')=='en' else 'es'
    except Exception: return s.send_error(400)
    hits=search(q,lang);out={'mode':'ai' if KEY else 'demo','sources':[{'t':h['t'],'src':h['src']} for h in hits],'help':HELP[lang]}
    if KEY:
      try: out['answer']=llm(q,hits,lang)
      except Exception as e: out['mode']='demo';out['error']='LLM no disponible'
    if 'answer' not in out:
      out['answer']=('\n\n'.join(f"«{h['b']}» — {h['t']}" for h in hits) if hits else ('No encontré información verificada sobre eso.' if lang=='es' else 'No verified information found on that.'))
    b=json.dumps(out,ensure_ascii=False).encode();s.send_response(200);s.send_header('Content-Type','application/json; charset=utf-8');s.send_header('Content-Length',len(b));s.end_headers();s.wfile.write(b)
if __name__=='__main__': ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT',8643))),H).serve_forever()
