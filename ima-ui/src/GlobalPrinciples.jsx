import React from 'react';

const PRINCIPLES=[
 {k:'Human agency',h:'האדם נשאר בשליטה',p:'אמא מסבירה, מציעה ומסייעת — אך פעולה משמעותית נשארת בידי האדם, עם אפשרות לעצור, לבטל ולתקן.',sources:'Apple · OECD · NIST'},
 {k:'Truth & evidence',h:'אמת לפני הכרזה',p:'הפרדה ברורה בין מה שנבדק, מה ידוע, מה משוער ומה עדיין לא אומת. יכולת אינה מוצגת כחיה בלי ראיה.',sources:'OECD · NIST · IMA'},
 {k:'Privacy by design',h:'פרטיות כבר בתכנון',p:'איסוף מידע מצומצם, הסכמה מובנת, שליטה בזיכרון ושקיפות לגבי השימוש במידע.',sources:'Apple · OECD'},
 {k:'Accessible by default',h:'נגישות היא בסיס',p:'שפה, RTL, מובייל, מקלדת, קול, גודל טקסט, ניגודיות והפחתת תנועה הם חלק מהמוצר ולא תוספת מאוחרת.',sources:'Apple · W3C · GOV.UK'},
 {k:'Clear & familiar',h:'פשוט, מוכר וצפוי',p:'היררכיה ברורה, דפוסי ממשק מוכרים, משוב מיידי ושפה ישירה — בלי להסתיר את הפעולה החשובה.',sources:'Apple · Google Material · Microsoft Fluent'},
 {k:'Safety & resilience',h:'בטוח, ניתן לתיקון',p:'ניטור, בדיקות, גבולות, כשל בטוח, יכולת עקיפה והתאוששות. בעיה נכנסת ללולאת תיקון.',sources:'NIST · OECD · ITU'},
 {k:'Accountability',h:'אחריות ניתנת לבדיקה',p:'לכל יכולת משמעותית יש ראיה, סטטוס, בדיקה חוזרת ודרך לערער או לדווח על בעיה.',sources:'OECD · NIST · ITU'},
 {k:'Continuous learning',h:'משתפרים מהעולם',p:'משוב, בדיקות אמיתיות, מדדים ולקחים מתועדים חוזרים למוצר — בלי להפוך כל משוב אוטומטית לאמת.',sources:'Apple · ITU · modern product practice'}
];

export default function GlobalPrinciples(){
 return <section className="global-principles-section" id="principles">
  <div className="section-head"><span className="eyebrow">GLOBAL PRACTICE → IMA</span><h2>לומדים מהעולם בלי לאבד את הזהות של אמא</h2><p>אמא מאמצת עקרונות מוכחים של מוצר, נגישות, פרטיות, בטיחות וממשל — לא את המותגים עצמם.</p></div>
  <div className="principles-grid">{PRINCIPLES.map(x=><article key={x.k} className="principle-card"><span>{x.k}</span><h3>{x.h}</h3><p>{x.p}</p><small>{x.sources}</small></article>)}</div>
  <div className="principles-rule"><b>כלל ההטמעה של אמא:</b> ללמוד → להשוות → להוכיח → להטמיע → לבדוק בשטח → למדוד → לתקן.</div>
 </section>
}
