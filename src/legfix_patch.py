# --- Travel times keep the original legs: a flight or booked transfer is never replaced by a guess,
# and a guess between two stops comes from their positions on the original route. Damaged plans repair themselves on load.
_m = re.search(r"^const DAYS=(\[.*?\]);$", S, re.M)
assert _m, "DAYS"
S = rep(S, "const fillPos=l=>{", "const ODAYS=" + _m.group(1) + r""";
const OLEG={},OPOS=ODAYS.map(()=>({}));
ODAYS.forEach((d,di)=>{let p={walk:0,car:0,train:0};d.items.forEach((it,k)=>{OPOS[di][it.title]=p;const nx=d.items[k+1];if(it.leg){OLEG[di+'|'+it.title+'|'+it.leg.to]=it.leg;p=addV(p,legV(it.leg))}else if(nx)OLEG[di+'|'+it.title+'|'+nx.title]=0})});
const oDay=l=>{let best=-1,bn=0;OPOS.forEach((m,di)=>{const n=l.filter(it=>m[it.title]).length;if(n>bn){bn=n;best=di}});return bn>=Math.min(3,l.length)?best:-1};
const fillPos=l=>{const od=oDay(l);if(od>=0)l.forEach(it=>{const p=OPOS[od][it.title];if(p){it.p={...p};it.pe=false}});l._od=od;""")
S = rep(S, "if(!nx)it.leg=null;else if(!it.leg||it.leg.to!==nx.title)it.leg=it.p&&nx.p&&!it.pe&&!nx.pe?posLeg(it,nx,dm):estLeg(it,nx,dm);",
  r"""const ok=nx&&l._od>=0?l._od+'|'+it.title+'|'+nx.title:'',ol=ok?OLEG[ok]:null;
      if(!nx||ol===0)it.leg=null;else if(ol){if(!it.leg||it.leg.est||it.leg.to!==nx.title){const m=it.leg&&it.leg.to===nx.title&&!it.leg.est?it.leg.mode:ol.mode;it.leg={...clone(ol),mode:m}}}
      else if(!it.leg||it.leg.to!==nx.title||it.leg.est){const keep=it.leg&&it.leg.to===nx.title?it.leg.mode:null;
        it.leg=it.p&&nx.p&&!it.pe&&!nx.pe?posLeg(it,nx,dm):estLeg(it,nx,dm);if(keep&&it.leg.mode!=='flight')it.leg.mode=keep}""")
# Repair plans damaged by the old reorder (e.g. the flight turned into a 16-minute train) as soon as they load.
S = rep(S, "this.setState({sync:'shared',days:d&&Array.isArray(d.days)?clone(d.days):clone(DAYS),draft:d?d.draft||false:false})},warn);",
  r"""const days=d&&Array.isArray(d.days)?clone(d.days):clone(DAYS),before=JSON.stringify(days);days.forEach(x=>this.relink(x.items));
      this.setState({sync:'shared',days,draft:d?d.draft||false:false});if(d&&JSON.stringify(days)!==before)this.savePlan()},warn);""")
