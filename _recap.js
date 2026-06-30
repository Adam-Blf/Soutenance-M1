const { chromium } = require('playwright');
const path=require('path'); const SCR=path.join(__dirname,'assets','screens');
(async()=>{
  const b=await chromium.launch(); const pg=await b.newPage({deviceScaleFactor:1.25});
  await pg.setViewportSize({width:1600,height:900});
  await pg.goto('http://localhost:8502',{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
  // attendre que le contenu Streamlit soit rendu (titre / texte visible)
  await pg.waitForTimeout(20000);
  await pg.screenshot({path:path.join(SCR,'iapero-speakeasy-live.png')});
  console.log('-> iapero-speakeasy-live.png');
  await pg.evaluate(()=>window.scrollTo(0,400)); await pg.waitForTimeout(1500);
  await pg.screenshot({path:path.join(SCR,'iapero-app-live.png')});
  console.log('-> iapero-app-live.png');
  await b.close();
})().catch(e=>{console.error(e.message);process.exit(1)});
