function Chat(){const ms=S.cur?S.cur.msgs:[];return `<div class="chat"><div class="chead"><div class="av">${I('spark')}</div><div style="flex:1"><b>Policy Assistant</b><small>Online · answers from uploaded policies</small></div><button class="btn ghost sm" onclick="clearChat()">${I('clr')}Clear chat</button></div>${ChatWindow(ms)}${ChatInput(ms)}</div>`}
function send(q){if(S.typing)return;S.view='chat';if(!S.cur){S.cur={id:Date.now(),title:q,date:new Date(),msgs:[]};S.chats.unshift(S.cur)}
S.cur.msgs.push({r:'u',t:q});S.typing=true;render();const c=S.cur;
setTimeout(()=>{const h=ask(q);c.msgs.push(h?{r:'a',...h,t:h.a}:{r:'a',nf:1,t:''});S.typing=false;if(S.view==='chat'&&S.cur===c){render();$('#qi')?.focus()}},1100)}
function clearChat(){if(S.cur){S.chats=S.chats.filter(c=>c!==S.cur);S.cur=null}render();toast('Chat cleared')}
function openChat(id){S.cur=S.chats.find(c=>c.id===id);S.view='chat';render()}
