
<script>
(function(){
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var prog=document.getElementById('prog'),navA=document.querySelectorAll('#nav a');
  var heads=[].slice.call(document.querySelectorAll('.ch[id]'));
  function onScroll(){var h=document.documentElement;var p=h.scrollTop/(h.scrollHeight-h.clientHeight);prog.style.width=(p*100)+'%';
    var cur='top';for(var i=0;i<heads.length;i++){if(heads[i].getBoundingClientRect().top<window.innerHeight*.45)cur=heads[i].id}
    if(cur==='c4')cur='c3';navA.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+cur)});}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  var glow=document.getElementById('glow'),gx=0,gy=0,tx=0,ty=0,moved=false;
  window.addEventListener('mousemove',function(e){tx=e.clientX;ty=e.clientY;if(!moved){moved=true;document.body.classList.add('has-mouse')}});
  (function loop(){gx+=(tx-gx)*.08;gy+=(ty-gy)*.08;glow.style.transform='translate('+gx+'px,'+gy+'px)';requestAnimationFrame(loop)})();
  var counted=new WeakSet();
  function count(el){if(counted.has(el))return;counted.add(el);var t=parseInt(el.getAttribute('data-count'),10),p=el.getAttribute('data-prefix')||'',s=el.getAttribute('data-suffix')||'';if(reduce){el.textContent=p+t.toLocaleString()+s;return}var t0=null,d=1100;function step(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/d);k=1-Math.pow(1-k,3);el.textContent=p+Math.round(t*k).toLocaleString()+s;if(k<1)requestAnimationFrame(step)}requestAnimationFrame(step)}
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;en.target.classList.add('in');en.target.querySelectorAll('[data-count]').forEach(count);if(en.target.hasAttribute('data-count'))count(en.target);io.unobserve(en.target)})},{threshold:.18,rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll('.rv,[data-count]').forEach(function(el){io.observe(el)});
  } else {document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});document.querySelectorAll('[data-count]').forEach(count)}
  document.querySelectorAll('.fig').forEach(function(f){var svg=f.querySelector('.ich');if(!svg)return;var ro=f.querySelector('.readout');var rt=ro.querySelector('.rt'),rl=ro.querySelector('.rl'),rs=ro.querySelector('.rs');var def={t:rt.textContent,l:rl.textContent,s:rs.textContent};var pinned=null;
    function set(m){rt.textContent=m.t;rl.textContent=m.l;rs.textContent=m.s}
    function hot(b){svg.classList.add('hovering');svg.querySelectorAll('.bar.hot').forEach(function(x){x.classList.remove('hot')});b.classList.add('hot');set(JSON.parse(b.getAttribute('data-meta')))}
    svg.querySelectorAll('.bar').forEach(function(b){
      b.addEventListener('mouseenter',function(){if(!pinned)hot(b)});
      b.addEventListener('click',function(e){e.stopPropagation();if(pinned===b){pinned=null;svg.classList.remove('hovering');b.classList.remove('hot');set(def)}else{pinned=b;hot(b)}});
    });
    svg.addEventListener('mouseleave',function(){if(pinned)return;svg.classList.remove('hovering');svg.querySelectorAll('.bar.hot').forEach(function(x){x.classList.remove('hot')});set(def)});
  });
  document.querySelectorAll('.story').forEach(function(s){function tog(){s.classList.toggle('open')}s.addEventListener('click',tog);s.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();tog()}})});
  var spot=document.getElementById('spot');
  if(spot){var f={};['rank','name','handle','net60','net30','last','days','pers','angle'].forEach(function(k){f[k]=document.getElementById('s-'+k)});var cur=null,ft=null;
    function show(r){if(cur)cur.classList.remove('on');cur=r;r.classList.add('on');var d=r.dataset;f.rank.textContent=d.rank;f.name.textContent=d.name;f.handle.textContent=d.handle;f.net60.textContent=d.net60;f.net30.textContent=d.net30;f.last.textContent=d.last;f.days.innerHTML=d.days+'<small style="font-size:.5em"> days</small>';f.pers.textContent=d.pers;f.angle.textContent=d.angle;spot.classList.add('flash');clearTimeout(ft);ft=setTimeout(function(){spot.classList.remove('flash')},350)}
    var rows=document.querySelectorAll('.whales .lr[data-name]');rows.forEach(function(r){r.addEventListener('mouseenter',function(){show(r)});r.addEventListener('click',function(){show(r)});r.addEventListener('focus',function(){show(r)})});if(rows[0])rows[0].classList.add('on');}
})();
</script>
