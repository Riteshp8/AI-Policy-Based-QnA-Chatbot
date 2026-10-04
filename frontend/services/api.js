/* Real FastAPI client. The UI still runs on the mock data below until pages call `api.*` */
const API_URL='/api';let TOKEN=null;
async function request(path,opts={}){const fd=opts.body instanceof FormData;const h={...(fd?{}:{'Content-Type':'application/json'}),...(TOKEN?{Authorization:'Bearer '+TOKEN}:{})};
const r=await fetch(API_URL+path,{...opts,headers:h,body:opts.body&&!fd?JSON.stringify(opts.body):opts.body});
if(!r.ok)throw new Error((await r.json().catch(()=>({}))).detail||r.statusText);return r.status===204?null:r.json()}
const api={login:(email,password)=>request('/auth/login',{method:'POST',body:{email,password}}).then(d=>(TOKEN=d.access_token,d)),
signup:b=>request('/auth/signup',{method:'POST',body:b}).then(d=>(TOKEN=d.access_token,d)),
policies:()=>request('/policies'),
uploadPolicy:file=>{const f=new FormData();f.append('file',file);return request('/policies/upload',{method:'POST',body:f})},
deletePolicy:id=>request('/policies/'+id,{method:'DELETE'}),
ask:(question,chat_id)=>request('/chat/ask',{method:'POST',body:{question,chat_id}}),
chats:()=>request('/chat'),deleteChat:id=>request('/chat/'+id,{method:'DELETE'})};
/* ---- Mock data (remove once wired) ---- */
/* ===== Mock data layer. Replace each fn below with fetch() calls to FastAPI:
   POST /auth/login, POST /auth/signup, GET /policies, POST /policies/upload, DELETE /policies/{id},
   POST /chat/ask  -> {answer, sources:[{document,section,page,score}]}, GET /chats ===== */
const ago=n=>new Date(Date.now()-n*864e5);
let S={user:null,view:'dashboard',mode:'login',policies:[
{id:1,name:'HR Leave Policy 2026',date:ago(40),status:'Active',pages:24,desc:'Annual, sick, parental and carry-forward leave rules for all employees.'},
{id:2,name:'Remote Work Policy',date:ago(28),status:'Active',pages:12,desc:'Eligibility, approvals, core hours and equipment for hybrid and remote work.'},
{id:3,name:'IT Security Policy',date:ago(17),status:'Active',pages:31,desc:'Passwords, MFA, device handling and incident reporting.'},
{id:4,name:'Expense Reimbursement Policy',date:ago(6),status:'Active',pages:15,desc:'Travel, meals and claim submission limits and approvals.'}],
chats:[],cur:null,typing:false,q:'',adminQ:'',adminF:'all',upl:null,open:false,modal:null};
const KB=[
{k:['sick','medical'],a:'You get 12 paid sick days per year. A medical certificate is required for absences longer than 2 consecutive days.',d:'HR Leave Policy 2026',s:'Section 3.5 – Sick Leave',p:8,c:90},
{k:['leave','vacation','pto','holiday','carry'],a:'Full-time employees receive 24 days of paid annual leave per year, accrued monthly. Up to 10 unused days can be carried forward to the next year.',d:'HR Leave Policy 2026',s:'Section 3.2 – Annual Leave',p:6,c:94},
{k:['remote','home','wfh','hybrid','core hours'],a:'Employees may work remotely up to 3 days per week with manager approval. Core hours of 11:00–16:00 local time apply on remote days.',d:'Remote Work Policy',s:'Section 2.1 – Eligibility',p:4,c:91},
{k:['expense','reimburse','travel','claim','receipt'],a:'Submit expense claims within 30 days with receipts attached. Claims above ₹10,000 need director approval.',d:'Expense Reimbursement Policy',s:'Section 4.3 – Claims',p:9,c:88},
{k:['password','security','vpn','mfa','device'],a:'Passwords must be at least 12 characters, rotated every 90 days, with MFA enabled on all company accounts. Use the VPN on public networks.',d:'IT Security Policy',s:'Section 5.1 – Access Control',p:12,c:92}];
const SUGG=['How many leave days do I get?','Can I work from home?','How do I claim travel expenses?','What is the password policy?'];
S.chats=[{id:1,title:'How many leave days do I get?',date:ago(2),msgs:[{r:'u',t:'How many leave days do I get?'},{r:'a',...KB[1],t:KB[1].a}]},{id:2,title:'Can I work from home?',date:ago(5),msgs:[{r:'u',t:'Can I work from home?'},{r:'a',...KB[2],t:KB[2].a}]}];
const ask=q=>{q=q.toLowerCase();const act=n=>S.policies.some(p=>p.name===n&&p.status==='Active');return KB.find(e=>e.k.some(k=>q.includes(k))&&act(e.d))||null};
