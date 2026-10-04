/* App shell + bootstrap */
function render(){const r=$('#root');if(!S.user){r.innerHTML=Login();return}
const adm=S.user.role==='Admin',N=[['dashboard','home','Dashboard'],['chat','plus','New Chat'],['history','hist','Chat History'],['policies','file','Available Policies'],...(adm?[['admin','shield','Admin Panel']]:[]),['profile','user','Profile']];
r.innerHTML=`<div id="app">${Sidebar(N)}<main>${Navbar()}${view()}</main></div>`;
const m=$('.msgs');if(m)m.scrollTop=m.scrollHeight}
function go(v){S.view=v;S.open=false;if(v==='chat'){S.cur=null}render()}
function logout(){S.user=null;S.cur=null;S.open=false;render()}
function view(){return({dashboard:Dashboard,chat:Chat,history:ChatHistory,policies:Policies,admin:AdminDashboard,profile:Profile})[S.view]()}
render();
