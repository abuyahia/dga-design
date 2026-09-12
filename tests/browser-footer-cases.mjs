import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runFooter({send,evaluate,wait,root}) {
 const results=[];
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const direction of ['rtl','ltr']) for(const theme of ['default','dark']) for(const width of [320,375,599,600,768,1327,1600]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:1200,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/footer/showcases',direction+'-'+theme+(width<600?'-mobile':'')+'.html')).href});await wait(120);
  await evaluate('document.fonts.ready.then(()=>true)');
  const checks=await evaluate(`(() => {
   const footer=document.querySelector('.ds-footer'),content=footer.querySelector('.ds-footer__content'),nav=footer.querySelector('.ds-footer__navigation'),groups=[...nav.children],tools=footer.querySelector('.ds-footer__tools'),legal=footer.querySelector('.ds-footer__legal'),logos=footer.querySelector('.ds-footer__logos'),button=footer.querySelector('.btn'),heading=footer.querySelector('h2'),link=footer.querySelector('.link');
   const s=e=>getComputedStyle(e),r=e=>e.getBoundingClientRect(),dark=${theme==='dark'},mobile=innerWidth<600;
   return {referenceHeight:innerWidth===1327?r(footer).height===(document.documentElement.dir==='rtl'?468:484):innerWidth===599?r(footer).height===(document.documentElement.dir==='ltr'&&!dark?1100:1026):true,fits:document.documentElement.scrollWidth<=innerWidth,background:s(footer).backgroundColor===(dark?'rgb(7, 77, 49)':'rgb(243, 244, 246)'),container:r(content).width===Math.min(innerWidth-64,1280),padding:s(content).paddingTop==='40px'&&s(content).paddingBottom==='24px',heading:r(heading).height===32&&s(heading).fontSize==='16px'&&s(heading).fontWeight==='500'&&s(heading).lineHeight==='24px',border:s(heading).borderBottomColor===(dark?'rgba(255, 255, 255, 0.3)':'rgb(210, 214, 219)'),link:s(link).fontSize==='14px'&&s(link).lineHeight==='20px'&&s(link).color===(dark?'rgb(255, 255, 255)':'rgb(56, 66, 80)'),linkGap:s(footer.querySelector('.ds-footer__links')).gap==='8px',button:r(button).width===32&&r(button).height===32,buttonBorder:s(button).borderTopWidth==='1px'&&s(button).borderTopColor===(dark?'rgba(255, 255, 255, 0.3)':'rgb(210, 214, 219)'),direction:document.documentElement.dir==='rtl'?r(groups[0]).right>r(groups[1]).right:r(groups[0]).left<r(groups[1]).left,responsive:mobile?s(nav).gridTemplateColumns.split(' ').length===2&&r(tools).top>r(groups[4]).bottom&&s(legal).flexDirection==='column':s(legal).flexDirection==='row',logoOpacity:s(logos).opacity==='0.7',images:[...footer.querySelectorAll('img')].every(e=>e.complete&&e.naturalWidth>0),names:[...footer.querySelectorAll('.btn')].every(e=>!!e.getAttribute('aria-label')),legalUnderline:s(footer.querySelector('.ds-footer__legal-links .link')).textDecorationLine==='underline'};
  })()`);
  results.push({direction,theme,width,checks,pass:Object.values(checks).every(Boolean)});
  await evaluate(`document.querySelector('.ds-footer .btn').focus()`);
  const focused=await evaluate(`(()=>{const s=getComputedStyle(document.activeElement);return s.borderTopWidth==='2px'&&s.borderTopColor===${JSON.stringify(theme==='dark'?'rgb(255, 255, 255)':'rgb(0, 0, 0)')}})()`);
  results.push({name:'Focus border',direction,theme,width,pass:focused,actual:await evaluate(`(()=>{const s=getComputedStyle(document.activeElement);return {tag:document.activeElement.outerHTML,border:s.borderTopWidth,color:s.borderTopColor}})()`)});
 }
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/footer/showcases/index.html')).href});await wait(150);
 results.push({name:'Nav links false preserves legal content',pass:await evaluate(`(()=>{const f=[...document.querySelectorAll('.ds-footer')].at(-1);return !f.querySelector('.ds-footer__navigation')&&!!f.querySelector('.ds-footer__copyright')&&!!f.querySelector('.ds-footer__logos')})()`)});
 return results;
}
