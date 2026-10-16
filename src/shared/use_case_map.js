(function(){
  var q=document.getElementById('q'),sec=document.getElementById('sec'),sort=document.getElementById('sort'),
      count=document.getElementById('count'),empty=document.getElementById('empty'),
      rail=document.querySelectorAll('.rail a'),kb=document.querySelectorAll('#kind button'),
      tb=document.querySelectorAll('#tierf button'),kind='',tier='',TOTAL=__TOTAL__;
  document.querySelectorAll('.cards').forEach(function(c){c._orig=[].slice.call(c.children)});
  function apply(){
    var term=q.value.trim().toLowerCase(),shown=0;
    document.querySelectorAll('.cards').forEach(function(c){
      var kids=c._orig.slice();
      if(sort.value==='value')kids.sort(function(a,b){return b.dataset.v-a.dataset.v});
      kids.forEach(function(k){c.appendChild(k)});
    });
    document.querySelectorAll('.section').forEach(function(s,i){
      var n=0,inSec=!sec.value||sec.value===s.id;
      s.querySelectorAll('.proc').forEach(function(p){
        var m=0;
        p.querySelectorAll('.card').forEach(function(c){
          var ok=inSec&&(!kind||c.dataset.k===kind)&&(!tier||c.dataset.t===tier)&&(!term||c.dataset.q.indexOf(term)>-1);
          c.hidden=!ok;if(ok)m++;
        });
        p.hidden=!m;n+=m;
      });
      s.hidden=!n;shown+=n;
      var t=+s.dataset.total,meta=s.querySelector('.meta');
      if(!meta._o)meta._o=meta.textContent;
      meta.textContent=n===t?meta._o:s.dataset.meta+' · '+n+' of '+t+' use cases';
      rail[i].querySelector('i').textContent=n;rail[i].classList.toggle('dim',!n);
    });
    count.textContent=shown===TOTAL?'Showing all '+TOTAL+' use cases':'Showing '+shown+' of '+TOTAL+' use cases';
    empty.hidden=!!shown;
  }
  function seg(btns,set){btns.forEach(function(b){b.addEventListener('click',function(){
    set(b.dataset.k!==undefined?b.dataset.k:b.dataset.t);btns.forEach(function(x){x.setAttribute('aria-pressed',x===b)});apply();
  })})}
  q.addEventListener('input',apply);sort.addEventListener('change',apply);
  sec.addEventListener('change',function(){apply();window.scrollTo({top:document.querySelector('.bar').offsetTop})});
  seg(kb,function(v){kind=v});seg(tb,function(v){tier=v});
  apply();
})();
