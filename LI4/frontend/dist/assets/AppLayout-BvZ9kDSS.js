import{G as U,H as M,s as $,g as T,o as p,h as V,a as e,b as _,i as q,c as m,F as N,l as L,j as d,p as H,t as v,T as D,I,_ as O,e as W,d as B,J as E,r as P,m as F}from"./index-BfxmCC4D.js";import{u as G}from"./useAuth-VFWmr4_0.js";/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const z=s=>s==="";/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const R=(...s)=>s.filter((t,a,o)=>!!t&&t.trim()!==""&&o.indexOf(t)===a).join(" ").trim();/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const A=s=>s.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Z=s=>s.replace(/^([A-Z])|[\s-_]+(\w)/g,(t,a,o)=>o?o.toUpperCase():a.toLowerCase());/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const J=s=>{const t=Z(s);return t.charAt(0).toUpperCase()+t.slice(1)};/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */var y={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const X=Symbol("lucide-icons");function K(){return U(X,{})}/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Q=({name:s,iconNode:t,absoluteStrokeWidth:a,"absolute-stroke-width":o,strokeWidth:i,"stroke-width":c,size:u,color:g,...x},{slots:k})=>{const{size:n,color:C,strokeWidth:b=2,absoluteStrokeWidth:f=!1,class:l=""}=K(),S=$(()=>{const w=z(a)||z(o)||a===!0||o===!0||f===!0,j=i||c||b||y["stroke-width"];return w?Number(j)*24/Number(u??n??y.width):j});return M("svg",{...y,...x,width:u??n??y.width,height:u??n??y.height,stroke:g??C??y.stroke,"stroke-width":S.value,class:R("lucide",l,...s?[`lucide-${A(J(s))}-icon`,`lucide-${A(s)}`]:["lucide-icon"])},[...t.map(w=>M(...w)),...k.default?[k.default()]:[]])};/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const r=(s,t)=>(a,{slots:o,attrs:i})=>M(Q,{...i,...a,iconNode:t,name:s},o.default?{default:o.default}:void 0);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Y=[["path",{d:"M3 3v16a2 2 0 0 0 2 2h16",key:"c24i48"}],["path",{d:"M18 17V9",key:"2bz60n"}],["path",{d:"M13 17V5",key:"1frdt8"}],["path",{d:"M8 17v-3",key:"17ska0"}]],ee=r("chart-column",Y);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const te=[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["circle",{cx:"12",cy:"10",r:"3",key:"ilqhr7"}],["path",{d:"M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662",key:"154egf"}]],se=r("circle-user",te);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ae=[["rect",{width:"8",height:"4",x:"8",y:"2",rx:"1",ry:"1",key:"tgr4d6"}],["path",{d:"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2",key:"116196"}],["path",{d:"M12 11h4",key:"1jrz19"}],["path",{d:"M12 16h4",key:"n85exb"}],["path",{d:"M8 11h.01",key:"1dfujw"}],["path",{d:"M8 16h.01",key:"18s6g9"}]],oe=r("clipboard-list",ae);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ne=[["line",{x1:"12",x2:"12",y1:"2",y2:"22",key:"7eqyqh"}],["path",{d:"M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6",key:"1b0p4s"}]],ie=r("dollar-sign",ne);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const re=[["rect",{width:"7",height:"9",x:"3",y:"3",rx:"1",key:"10lvy0"}],["rect",{width:"7",height:"5",x:"14",y:"3",rx:"1",key:"16une8"}],["rect",{width:"7",height:"9",x:"14",y:"12",rx:"1",key:"1hutg5"}],["rect",{width:"7",height:"5",x:"3",y:"16",rx:"1",key:"ldoo1y"}]],ce=r("layout-dashboard",re);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const le=[["path",{d:"m16 17 5-5-5-5",key:"1bji2h"}],["path",{d:"M21 12H9",key:"dn1m92"}],["path",{d:"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4",key:"1uf3rs"}]],de=r("log-out",le);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ue=[["path",{d:"M4 5h16",key:"1tepv9"}],["path",{d:"M4 12h16",key:"1lakjw"}],["path",{d:"M4 19h16",key:"1djgab"}]],he=r("menu",ue);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const pe=[["path",{d:"M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z",key:"1a0edw"}],["path",{d:"M12 22V12",key:"d0xqtd"}],["polyline",{points:"3.29 7 12 12 20.71 7",key:"ousv84"}],["path",{d:"m7.5 4.27 9 5.15",key:"1c824w"}]],ke=r("package",pe);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ye=[["path",{d:"m21 21-4.34-4.34",key:"14j7rj"}],["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}]],Pe=r("search",ye);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const _e=[["path",{d:"M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2",key:"wrbu53"}],["path",{d:"M15 18H9",key:"1lyqi6"}],["path",{d:"M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14",key:"lysw3i"}],["circle",{cx:"17",cy:"18",r:"2",key:"332jqn"}],["circle",{cx:"7",cy:"18",r:"2",key:"19iecd"}]],ve=r("truck",_e);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const me=[["path",{d:"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2",key:"1yyitq"}],["path",{d:"M16 3.128a4 4 0 0 1 0 7.744",key:"16gr8j"}],["path",{d:"M22 21v-2a4 4 0 0 0-3-3.87",key:"kshegd"}],["circle",{cx:"9",cy:"7",r:"4",key:"nufk8"}]],be=r("users",me);/**
 * @license @lucide/vue v1.16.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const fe=[["path",{d:"M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z",key:"1ngwbx"}]],ge=r("wrench",fe),h=T([]);let xe=0;function Ce(){function s(a,o="error",i=4e3){const c=xe++;h.value=[...h.value,{id:c,message:a,type:o}],setTimeout(()=>{h.value=h.value.filter(u=>u.id!==c)},i)}function t(a){h.value=h.value.filter(o=>o.id!==a)}return{toasts:h,toast:s,dismiss:t}}const we={class:"toast-container"},Me=["onClick"],$e={__name:"ToastContainer",setup(s){const{toasts:t,dismiss:a}=Ce();return(o,i)=>(p(),V(I,{to:"body"},[e("div",we,[_(D,{name:"toast"},{default:q(()=>[(p(!0),m(N,null,L(d(t),c=>(p(),m("div",{key:c.id,class:H(["toast",c.type]),onClick:u=>d(a)(c.id)},v(c.message),11,Me))),128))]),_:1})])]))}},Ne={class:"layout"},Se={class:"sidebar-brand"},je={class:"brand-icon"},ze={class:"sidebar-nav"},Ae={class:"nav-icon"},Te={class:"sidebar-footer"},Ve={class:"user-info"},qe={class:"user-avatar"},Le={class:"user-name"},He={class:"user-role"},Ue={class:"main-wrap"},De={class:"topbar"},Ie={class:"topbar-title"},Oe={class:"main-content"},We={__name:"AppLayout",setup(s){const{currentUser:t,logout:a}=G(),o=E(),i=T(!1),c=[{path:"/dashboard",icon:ce,label:"Dashboard"},{path:"/clientes",icon:be,label:"Clientes"},{path:"/equipamentos",icon:ve,label:"Equipamentos"},{path:"/ordens-servico",icon:oe,label:"Ordens de Serviço"},{path:"/stock",icon:ke,label:"Stock & Peças"},{path:"/faturacao",icon:ie,label:"Faturação"},{path:"/relatorios",icon:ee,label:"Relatórios"},{path:"/utilizadores",icon:se,label:"Utilizadores"}],u={"/dashboard":"Dashboard","/clientes":"Clientes","/equipamentos":"Equipamentos","/ordens-servico":"Ordens de Serviço","/stock":"Stock & Peças","/faturacao":"Faturação","/relatorios":"Relatórios","/utilizadores":"Utilizadores"},g=$(()=>u[o.path]||""),x=$(()=>t.value?t.value.name.split(" ").map(k=>k[0]).slice(0,2).join(""):"?");return(k,n)=>{var b,f;const C=P("router-link");return p(),m(N,null,[e("div",Ne,[e("aside",{class:H(["sidebar",{open:i.value}])},[e("div",Se,[e("div",je,[_(d(ge),{size:22})]),n[4]||(n[4]=e("div",null,[e("div",{class:"brand-name"},"TrotiFix"),e("div",{class:"brand-sub"},"Gestão de Oficina")],-1))]),e("nav",ze,[(p(),m(N,null,L(c,l=>_(C,{key:l.path,to:l.path,class:"nav-item",onClick:n[0]||(n[0]=S=>i.value=!1)},{default:q(()=>[e("span",Ae,[(p(),V(F(l.icon),{size:18}))]),e("span",null,v(l.label),1)]),_:2},1032,["to"])),64))]),e("div",Te,[e("div",Ve,[e("div",qe,v(x.value),1),e("div",null,[e("div",Le,v((b=d(t))==null?void 0:b.name),1),e("div",He,v((f=d(t))==null?void 0:f.perfil),1)])]),e("button",{class:"logout-btn",onClick:n[1]||(n[1]=(...l)=>d(a)&&d(a)(...l)),title:"Sair"},[_(d(de),{size:18})])])],2),i.value?(p(),m("div",{key:0,class:"sidebar-overlay",onClick:n[2]||(n[2]=l=>i.value=!1)})):W("",!0),e("div",Ue,[e("header",De,[e("button",{class:"menu-btn",onClick:n[3]||(n[3]=l=>i.value=!i.value)},[_(d(he),{size:20})]),e("div",Ie,v(g.value),1)]),e("main",Oe,[B(k.$slots,"default",{},void 0)])])]),_($e)],64)}}},Fe=O(We,[["__scopeId","data-v-0faa4965"]]);export{Fe as A,oe as C,ie as D,ke as P,Pe as S,be as U,ge as W,ee as a,r as c,Ce as u};
