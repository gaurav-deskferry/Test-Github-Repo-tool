const raw = [
["Midnight Drive","Nova Lane","Neon Streets","3:42"],["Golden Hour","Aria Bloom","Sunset Tapes","3:15"],
["Ocean Eyes Remix","Kai Waves","Blue Depth","4:01"],["Electric Heart","The Voltage","Circuit","2:58"],
["Paper Planes","Juno Park","Origami","3:30"],["Static Dreams","Nova Lane","Neon Streets","4:12"],
["Velvet Sky","Aria Bloom","Sunset Tapes","3:47"],["Run It Back","MC Ember","Heatwave","2:44"],
["Moonlit Road","Kai Waves","Blue Depth","3:55"],["Afterglow","The Voltage","Circuit","3:21"],
["Cherry Cola","Juno Park","Origami","2:39"],["Skyline","MC Ember","Heatwave","3:08"],
["Lost in Tokyo","Nova Lane","Neon Streets","4:30"],["Slow Burn","Aria Bloom","Sunset Tapes","3:59"],
["Echoes","Kai Waves","Blue Depth","5:02"],["Wildfire","The Voltage","Circuit","3:17"],
["Daydream","Juno Park","Origami","3:44"],["Gravity","MC Ember","Heatwave","3:26"],
["Northern Lights","Nova Lane","Neon Streets","4:05"],["Last Call","Aria Bloom","Sunset Tapes","3:12"]
].map(([title,artist,album,time],i)=>({id:i,title,artist,album,time,hue:(i*47)%360}));

const grad = s => `linear-gradient(135deg,hsl(${s.hue} 70% 45%),hsl(${(s.hue+60)%360} 70% 25%))`;
const $ = id => document.getElementById(id);
let current = -1, playing = false;

const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.style.transitionDelay = (e.target.dataset.d||0)+'ms'; e.target.classList.add('in'); io.unobserve(e.target); }
}), {threshold:.12});
const watch = (el,d=0) => { el.dataset.d = d; io.observe(el); };

function card(s,d,sub){
  const c = document.createElement('div'); c.className='card';
  c.innerHTML = `<div class="cover" style="background:${grad(s)}"></div><h3></h3><p></p><button class="pbtn" aria-label="Play">▶</button>`;
  c.querySelector('h3').textContent = sub?s.album:s.title;
  c.querySelector('p').textContent = s.artist;
  c.onclick = () => play(s.id);
  $(sub?'albumsRow':'trendingRow').append(c); watch(c,d);
}
raw.slice(0,10).forEach((s,i)=>card(s,i*70,false));
[...new Map(raw.map(s=>[s.album,s])).values()].forEach((s,i)=>card(s,i*70,true));

function renderList(q=''){
  const ol = $('songList'); ol.innerHTML='';
  const list = raw.filter(s=>(s.title+s.artist+s.album).toLowerCase().includes(q.toLowerCase()));
  $('empty').hidden = list.length>0;
  list.forEach((s,i)=>{
    const li = document.createElement('li'); li.className='song'+(s.id===current?' playing':'');
    li.innerHTML = `<span>${i+1}</span><div class="t"><div class="mini" style="background:${grad(s)}"></div><div><span class="n"></span><small></small></div></div><span class="al"></span><span>${s.time}</span>`;
    li.querySelector('.n').textContent = s.title; li.querySelector('small').textContent = s.artist; li.querySelector('.al').textContent = s.album;
    li.onclick = () => play(s.id);
    ol.append(li); watch(li,(i%8)*50);
  });
}
$('search').addEventListener('input',e=>renderList(e.target.value));

function play(id){
  current = id; playing = true; const s = raw[id];
  $('pTitle').textContent = s.title; $('pArtist').textContent = s.artist; $('pArt').style.background = grad(s);
  const p = document.querySelector('.player'); p.classList.remove('on','paused'); void p.offsetWidth; p.classList.add('on');
  sync(); renderList($('search').value);
}
function sync(){ $('play').textContent = playing?'⏸':'▶'; document.querySelector('.player').classList.toggle('paused',!playing); }
$('play').onclick = () => { if(current<0) return play(0); playing=!playing; sync(); };
$('next').onclick = () => play((current+1)%raw.length);
$('prev').onclick = () => play((current-1+raw.length)%raw.length);

document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
const h = new Date().getHours(); $('greet').textContent = h<12?'morning':h<18?'afternoon':'evening';

const links=[...document.querySelectorAll('.sidebar nav a')];
addEventListener('scroll',()=>{
  const max = document.documentElement.scrollHeight-innerHeight;
  $('progress').style.width = (max>0?scrollY/max*100:0)+'%';
  let act=links[0];
  links.forEach(a=>{const t=document.querySelector(a.getAttribute('href')); if(t&&t.getBoundingClientRect().top<innerHeight*.4) act=a;});
  links.forEach(a=>a.classList.toggle('active',a===act));
},{passive:true});
renderList();
