import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runFigma({send,evaluate,wait,root}) {
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/navigation-header/showcases/index.html')).href});await wait(300);
 await evaluate('document.fonts.ready.then(()=>true)');
 return evaluate(`(() => {
 const out=[], transparent='rgba(0, 0, 0, 0)';
 for(const e of document.querySelectorAll('[data-part]')) {
 const s=getComputedStyle(e),indicator=getComputedStyle(e,'::after'),ring=getComputedStyle(e,'::before');
 const state=e.dataset.previewState,selected=e.dataset.selected==='true',part=e.dataset.part;
 let bg=transparent,bar=transparent;
 if(selected) {bg=({default:'rgb(27, 131, 84)',hovered:'rgb(22, 106, 69)',pressed:'rgb(16, 70, 49)',focused:part==='action'?'rgb(20, 87, 58)':'rgb(27, 131, 84)',disabled:transparent})[state];bar=state==='disabled'?'rgb(229, 231, 235)':'rgb(84, 192, 138)';}
 else {if(state==='hovered'){bg='rgb(243, 244, 246)';bar='rgb(157, 164, 174)';} if(state==='pressed'){bg='rgb(229, 231, 235)';bar='rgb(31, 42, 55)';}}
 const checks={height:e.getBoundingClientRect().height===72,background:s.backgroundColor===bg,indicator:indicator.backgroundColor===bar&&indicator.height==='6px',weight:s.fontWeight===(selected?'600':'500'),padding:s.paddingTop==='8px'&&s.paddingLeft==='16px',gap:s.gap==='4px',radius:s.borderRadius==='4px',focus:state!=='focused'||ring.borderTopWidth==='2px',assets:[...e.querySelectorAll('img')].every(i=>i.complete&&i.naturalWidth>0)};
 out.push({part,layout:e.dataset.layout,state,selected,direction:e.closest('[dir]').dir,checks,pass:Object.values(checks).every(Boolean),actual:{background:s.backgroundColor,indicator:indicator.backgroundColor,width:e.getBoundingClientRect().width}});
 }
 for(const e of document.querySelectorAll('.submenu-board .nav-header__submenu-item')) {
 const s=getComputedStyle(e),state=e.dataset.previewState,dark=e.classList.contains('nav-header__submenu-item--on-color');
 const bg=state==='hovered'?(dark?'rgba(255, 255, 255, 0.2)':'rgb(243, 244, 246)'):state==='pressed'?(dark?'rgba(255, 255, 255, 0.4)':'rgb(229, 231, 235)'):transparent;
 const checks={height:e.getBoundingClientRect().height===64,radius:s.borderRadius==='8px',background:s.backgroundColor===bg,gap:s.gap==='16px',focus:state!=='focused'||s.boxShadow.includes(dark?'rgb(255, 255, 255)':'rgb(22, 22, 22)')};
 out.push({part:'submenu',state,dark,checks,pass:Object.values(checks).every(Boolean)});
 }
 return out;
 })()`);
}
