(() => {
  const TOTAL = 54, PER_PAGE = 6, PAGES = Math.ceil(TOTAL / PER_PAGE);
  const users = ["aria.k","leo_the_wanderer","mika.codes","sofia.arts","noah.fit","zoe.eats","ravi.snaps","emma.design","kai.surf","lina.books"];
  const emojis = ["🌅","🏔️","🍜","🎨","🚴","📚","🌊","🎸","🌸","☕","🚀","🦊","🏙️","🍓","🎧"];
  const palettes = [["#6d5efc","#ff5fa2"],["#00c6ff","#0072ff"],["#f7971e","#ffd200"],["#11998e","#38ef7d"],["#ee0979","#ff6a00"],["#654ea3","#eaafc8"],["#2193b0","#6dd5ed"],["#fc5c7d","#6a82fb"]];
  const captions = ["Golden hour never disappoints.","Weekend reset ✨","Found this hidden gem today.","Making things, one day at a time.","Good vibes only.","Can't stop thinking about this view.","Small moments, big memories.","New project loading…"];
  const commentTexts = ["Love this! 😍","Absolutely stunning","Where is this?","Need to go there ASAP","Great shot!","This made my day","So good 🔥","Wow, the colors!","Goals.","Saving this for later","Incredible vibes","Can you share the recipe?","Obsessed 🙌","Take me with you!"];

  const rnd = s => () => (s = (s * 16807) % 2147483647) / 2147483647;
  const posts = Array.from({ length: TOTAL }, (_, i) => {
    const r = rnd(i + 7), pick = a => a[Math.floor(r() * a.length)];
    return {
      id: i + 1, user: pick(users), emoji: pick(emojis), pal: pick(palettes), caption: pick(captions),
      likes: 20 + Math.floor(r() * 980), hours: 1 + Math.floor(r() * 47),
      comments: Array.from({ length: 5 + Math.floor(r() * 8) }, () => ({ u: pick(users), t: pick(commentTexts) }))
    };
  });

  const feed = document.getElementById("feed"), pager = document.getElementById("pager"),
        meta = document.getElementById("meta"), bar = document.getElementById("progress");
  let page = Number(new URLSearchParams(location.search).get("page")) || 1;
  page = Math.min(Math.max(page, 1), PAGES);

  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    const card = e.target;
    card.style.transitionDelay = (card.dataset.i % 3) * 90 + "ms";
    card.classList.add("in");
    card.querySelectorAll(".comment").forEach((c, k) => c.style.animationDelay = 300 + k * 120 + "ms");
    io.unobserve(card);
  }), { threshold: 0.15 });

  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function cardHTML(p, i) {
    return `<article class="card" data-i="${i}" data-id="${p.id}">
      <div class="card__head">
        <div class="avatar" style="background:linear-gradient(135deg,${p.pal[0]},${p.pal[1]})">${p.user[0].toUpperCase()}</div>
        <div><div class="card__user">${p.user}</div><div class="card__time">${p.hours}h ago · Post #${p.id}</div></div>
      </div>
      <div class="card__media" style="background:linear-gradient(135deg,${p.pal[0]},${p.pal[1]})"><span>${p.emoji}</span></div>
      <div class="card__actions">
        <button class="icon-btn like" aria-label="Like" aria-pressed="false">♡</button>
        <button class="icon-btn" aria-label="Comment">💬</button>
      </div>
      <div class="card__likes"><span class="count">${p.likes}</span> likes</div>
      <p class="card__caption"><b>${p.user}</b>${esc(p.caption)}</p>
      <div class="comments" tabindex="0" aria-label="Comments">
        ${p.comments.map(c => `<div class="comment"><b>${c.u}</b>${esc(c.t)}</div>`).join("")}
      </div>
    </article>`;
  }

  function pagerHTML() {
    const nums = [];
    for (let n = 1; n <= PAGES; n++) if (n === 1 || n === PAGES || Math.abs(n - page) <= 1) nums.push(n);
    let out = `<button data-p="${page - 1}" ${page === 1 ? "disabled" : ""} aria-label="Previous page">‹</button>`, last = 0;
    nums.forEach(n => {
      if (n - last > 1) out += `<span class="gap">…</span>`;
      out += `<button data-p="${n}" class="${n === page ? "active" : ""}" ${n === page ? 'aria-current="page"' : ""}>${n}</button>`;
      last = n;
    });
    return out + `<button data-p="${page + 1}" ${page === PAGES ? "disabled" : ""} aria-label="Next page">›</button>`;
  }

  function render() {
    const start = (page - 1) * PER_PAGE, slice = posts.slice(start, start + PER_PAGE);
    feed.innerHTML = slice.map(cardHTML).join("");
    feed.querySelectorAll(".card").forEach(c => io.observe(c));
    pager.innerHTML = pagerHTML();
    meta.textContent = `Showing ${start + 1}–${start + slice.length} of ${TOTAL} · Page ${page}/${PAGES}`;
    history.replaceState(null, "", `?page=${page}`);
  }

  pager.addEventListener("click", e => {
    const b = e.target.closest("button[data-p]");
    if (!b || b.disabled) return;
    page = Number(b.dataset.p);
    render();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  feed.addEventListener("click", e => {
    const b = e.target.closest(".like");
    if (!b) return;
    const on = b.classList.toggle("liked");
    b.textContent = on ? "♥" : "♡";
    b.setAttribute("aria-pressed", on);
    const n = b.closest(".card").querySelector(".count");
    n.textContent = +n.textContent + (on ? 1 : -1);
  });

  addEventListener("scroll", () => {
    const h = document.documentElement;
    bar.style.width = (h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight)) * 100 + "%";
  }, { passive: true });

  render();
})();
