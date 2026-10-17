// Baaz Leathers: Coco Dune MOF ad. Inlined by build.py into index.html (9:16) and feed/index.html (4:5).
// All timing comes from the voiceover: each line's start and length are fixed below.
(function () {
  const root = document.querySelector("[data-composition-id]");
  const W = 1080, H = +root.dataset.height;
  const vertical = H > 1500;
  // Product zone centre (px) and where headline / caption sit, per format.
  const ZONE_Y = vertical ? 925 : 668;

  // Voiceover lines: [start s, duration s, caption chunks]
  const VO = [
    [0.25, 2.379, ["You've seen it.", "Now take a closer look."]],
    [2.75, 3.707, ["Real cowhide suede,", "cut and stitched by hand in KP."]],
    [6.58, 2.355, ["On a light foam sole", "you barely feel."]],
    [9.05, 2.337, ["With soft memory foam underfoot."]],
    [11.51, 3.556, ["Sizes 40 to 46,", "with easy size exchange."]],
    [15.19, 3.876, ["Free delivery and cash on delivery,", "anywhere in Pakistan."]],
    [19.27, 2.345, ["Coco Dune. By Baaz Leathers."]],
  ];

  // Scenes: photo, on-screen headline, camera move from A to B (cx, cy = focus
  // point as a fraction of the 1512x2016 photo; z = 1 fills the frame width).
  const SCENES = [
    { t: 0.0,   img: "07", head: "Take a closer look.",                             A: [0.50, 0.50, 1.00], B: [0.52, 0.51, 1.16] },
    { t: 2.65,  img: "08", head: "Cowhide suede. Stitched by hand.",                A: [0.44, 0.34, 1.28], B: [0.56, 0.42, 1.38] },
    { t: 6.48,  img: "06", head: "About 300 grams a chappal.",                      A: [0.36, 0.47, 1.65], B: [0.62, 0.47, 1.65] },
    { t: 8.95,  img: "05", head: "Memory foam insole.",                             A: [0.50, 0.40, 1.30], B: [0.50, 0.38, 1.85] },
    { t: 11.41, img: "10", head: "Sizes 40 to 46. Easy exchange within 15 days.",   A: [0.52, 0.50, 1.00], B: [0.66, 0.46, 1.32] },
    { t: 15.09, img: "07", head: "Free delivery. Cash on delivery.",                A: [0.50, 0.50, 1.22], B: [0.50, 0.50, 1.00] },
  ];
  const END = 19.17, TOTAL = 22.0, XF = 0.3; // end card start, length, dip length
  // Cuts dip briefly through cream (out, then in) so two shots of the product never
  // overlap as a double exposure.

  const photos = document.getElementById("photos");
  const heads = document.getElementById("heads");
  SCENES.forEach((s, i) => {
    const wrap = document.createElement("div");
    wrap.className = "photo"; wrap.id = "ph-" + i;
    wrap.innerHTML = `<img id="img-${i}" src="assets/photos/${s.img}.jpg" alt="">`;
    photos.appendChild(wrap);
    const h = document.createElement("div");
    h.className = "head"; h.id = "hd-" + i; h.textContent = s.head;
    heads.appendChild(h);
  });
  const caps = document.getElementById("caps");
  const CAPS = [];
  VO.forEach(([st, d, chunks], li) => {
    const chars = chunks.reduce((a, c) => a + c.length, 0);
    let t = st;
    chunks.forEach((c, k) => {
      const dur = d * (c.length / chars);
      const el = document.createElement("div");
      el.className = "cap"; el.id = `cap-${li}-${k}`;
      el.innerHTML = `<span>${c}</span>`;
      caps.appendChild(el);
      CAPS.push([el.id, t, t + dur]);
      t += dur;
    });
  });

  const S = W / 1512; // px per photo px at z = 1
  const pose = ([cx, cy, z]) => ({ x: W / 2 - cx * 1512 * S * z, y: ZONE_Y - cy * 2016 * S * z, scale: S * z });

  const tl = gsap.timeline({ paused: true });

  SCENES.forEach((s, i) => {
    const a = s.t, b = i + 1 < SCENES.length ? SCENES[i + 1].t : END;
    const inAt = i === 0 ? 0 : a, outAt = b;
    // camera: one slow continuous move across the whole time the photo is visible
    tl.fromTo("#img-" + i, pose(s.A), { ...pose(s.B), duration: outAt + XF - inAt, ease: "sine.inOut" }, inAt);
    if (i > 0) tl.fromTo("#ph-" + i, { opacity: 0 }, { opacity: 1, duration: XF, ease: "sine.out" }, inAt);
    else tl.set("#ph-0", { opacity: 1 }, 0);
    tl.to("#ph-" + i, { opacity: 0, duration: XF, ease: "sine.in" }, b - XF);
    // headline
    tl.fromTo("#hd-" + i, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, a + (i === 0 ? 0.35 : 0.2));
    tl.to("#hd-" + i, { opacity: 0, y: -10, duration: 0.35, ease: "power1.in" }, b - 0.4);
  });

  CAPS.forEach(([id, a, b]) => {
    tl.fromTo("#" + id, { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "none" }, a);
    tl.to("#" + id, { opacity: 0, duration: 0.12, ease: "none" }, b);
  });

  // end card
  const ec = ["#ec-mark", "#ec-sub", "#ec-rule", "#ec-name", "#ec-line", "#ec-btn"];
  tl.fromTo("#endcard", { opacity: 0 }, { opacity: 1, duration: XF, ease: "sine.inOut" }, END - XF / 2);
  ec.forEach((sel, k) => tl.fromTo(sel, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }, END + 0.1 + k * 0.14));
  tl.fromTo("#ec-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "power2.out" }, END + 0.38);

  window.__timelines["main"] = tl;
  tl.seek(0);
})();
