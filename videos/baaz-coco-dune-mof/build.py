# Writes index.html (9:16, 1080x1920) and feed/index.html (4:5, 1080x1350) from one
# template so both formats stay in sync. Timing and motion live in ad.js.
# Run: python3 build.py
import os, shutil
FORMATS = {
    "index.html": dict(h=1920, scrim_solid=470, scrim_fade=640, head_top=272, head_size=74, cap_top=1452, ec_center=915),
    "feed/index.html": dict(h=1350, scrim_solid=262, scrim_fade=420, head_top=64, head_size=62, cap_top=1176, ec_center=675),
}

TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height={h}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Playfair Display"; src: url("assets/fonts/playfair-display-latin-400-normal.woff2") format("woff2"); font-weight: 400; font-style: normal; }}
      @font-face {{ font-family: "Playfair Display"; src: url("assets/fonts/playfair-display-latin-500-normal.woff2") format("woff2"); font-weight: 500; font-style: normal; }}
      @font-face {{ font-family: "Playfair Display"; src: url("assets/fonts/playfair-display-latin-400-italic.woff2") format("woff2"); font-weight: 400; font-style: italic; }}
      @font-face {{ font-family: "Inter"; src: url("assets/fonts/inter-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
      @font-face {{ font-family: "Inter"; src: url("assets/fonts/inter-latin-500-normal.woff2") format("woff2"); font-weight: 500; }}
      @font-face {{ font-family: "Inter"; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); font-weight: 600; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: {h}px; overflow: hidden; background: #f7f0e6; }}
      #root {{ width: 100%; height: 100%; position: relative; overflow: hidden; color: #3d2b20; font-family: "Inter", sans-serif; }}
      #ground {{ position: absolute; inset: 0; background: radial-gradient(1200px 900px at 50% 45%, #faf3e9, #f2e9dd); }}

      .photo {{ position: absolute; inset: 0; opacity: 0; }}
      .photo img {{ position: absolute; left: 0; top: 0; width: 1512px; height: 2016px; transform-origin: 0 0;
        -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 9%, #000 91%, transparent 100%), linear-gradient(to right, transparent 0, #000 8%, #000 92%, transparent 100%);
        -webkit-mask-composite: source-in; mask-composite: intersect; }}

      #scrim {{ position: absolute; left: 0; right: 0; top: 0; height: {scrim_fade}px;
        background: linear-gradient(to bottom, #faf3e9 0, #faf3e9 {scrim_solid}px, rgba(250, 243, 233, 0) {scrim_fade}px); }}
      .head {{ position: absolute; left: 90px; right: 90px; top: {head_top}px; text-align: center; opacity: 0;
        font-family: "Playfair Display", serif; font-weight: 400; font-size: {head_size}px; line-height: 1.14; letter-spacing: -0.01em; color: #3d2b20; text-wrap: balance; }}

      .cap {{ position: absolute; left: 70px; right: 70px; top: {cap_top}px; text-align: center; opacity: 0; }}
      .cap span {{ display: inline-block; background: rgba(250, 243, 233, 0.9); border-radius: 14px; padding: 12px 24px;
        font-size: 38px; font-weight: 500; line-height: 1.3; color: #3d2b20; }}

      #endcard {{ position: absolute; inset: 0; opacity: 0; background: #faf3e9; }}
      #ec-stack {{ position: absolute; left: 0; right: 0; top: {ec_center}px; height: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #ec-mark {{ font-family: "Playfair Display", serif; font-weight: 500; font-size: 128px; letter-spacing: 0.1em; line-height: 1; padding-left: 0.1em; }}
      #ec-sub {{ margin-top: 14px; font-size: 26px; font-weight: 600; letter-spacing: 0.46em; padding-left: 0.46em; color: #a8834f; }}
      #ec-rule {{ margin: 46px 0 40px; width: 120px; height: 2px; background: #b8935a; transform-origin: 50% 50%; }}
      #ec-name {{ font-family: "Playfair Display", serif; font-style: italic; font-size: 92px; line-height: 1.05; }}
      #ec-line {{ margin-top: 18px; font-size: 32px; font-weight: 400; color: #6b5444; }}
      #ec-btn {{ margin-top: 56px; background: #3d2b20; color: #faf3e9; border-radius: 999px; padding: 26px 60px; font-size: 34px; font-weight: 600; letter-spacing: 0.02em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="22" data-width="1080" data-height="{h}">
      <div id="bg" class="clip" data-start="0" data-duration="22" data-track-index="0"><div id="ground"></div></div>
      <div id="photos" class="clip" data-start="0" data-duration="22" data-track-index="1"></div>
      <div id="scrimwrap" class="clip" data-start="0" data-duration="22" data-track-index="2"><div id="scrim"></div></div>
      <div id="heads" class="clip" data-start="0" data-duration="22" data-track-index="3"></div>
      <div id="caps" class="clip" data-start="0" data-duration="22" data-track-index="4"></div>
      <div id="end" class="clip" data-start="0" data-duration="22" data-track-index="5">
        <div id="endcard">
          <div id="ec-stack">
            <div id="ec-mark">BAAZ</div>
            <div id="ec-sub">LEATHERS</div>
            <div id="ec-rule"></div>
            <div id="ec-name">Coco Dune</div>
            <div id="ec-line">Handmade Peshawari Chappals</div>
            <div id="ec-btn">Shop Coco Dune</div>
          </div>
        </div>
      </div>
    </div>
    <script>
{script}
    </script>
  </body>
</html>
"""

SCRIPT = open("ad.js").read()
# feed/ is its own HyperFrames project (one root composition per project), so it
# gets its own copy of the assets the page loads.
os.makedirs("feed/assets", exist_ok=True)
for d in ("photos", "fonts", "vendor"):
    shutil.copytree(f"assets/{d}", f"feed/assets/{d}", dirs_exist_ok=True)
for name, f in FORMATS.items():
    with open(name, "w") as fh:
        fh.write(TEMPLATE.format(script=SCRIPT, **f))
    print("wrote", name)
