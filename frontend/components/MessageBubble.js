function MessageBubble(m){if(m.r==='u')return `<div class="m u"><div class="bub">${esc(m.t)}</div></div>`;
if(m.nf)return `<div class="m a"><div class="av">${I('spark')}</div><div class="bub nf"><b style="display:flex;gap:6px;align-items:center">${I('alert')}Not found in policies</b><p style="margin:6px 0 0">I couldn't find this information in the available policy documents. Try rephrasing, or contact your HR or policy owner.</p></div></div>`;
return `<div class="m a"><div class="av">${I('spark')}</div><div class="bub"><div>${esc(m.t)}</div>${SourceCard(m)}</div></div>`}
