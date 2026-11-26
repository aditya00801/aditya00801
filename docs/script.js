// Interactive profile. The text and contribution data come from the files in /data.
const RAW = "https://raw.githubusercontent.com/aditya00801/aditya00801/main/data/";
const REPOS = {
  "student-stress": "Student_Lifestyle_and_Stress_Prediction",
  "cyber-shield": "Cyber-Shield-Auto",
  "brain-tumor": "Brain-Tumor-Detection",
  "coral-reef": "coral-reef-health-monitoring"
};
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
const mouse = matchMedia("(hover: hover) and (pointer: fine)").matches;
const $ = (selector) => document.querySelector(selector);

function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
}

async function load(name) {
  const response = await fetch(RAW + name);
  if (!response.ok) throw new Error(`${name}: ${response.status}`);
  return response.json();
}

function renderProfile(profile) {
  $("#lead").textContent = profile.lead;
  $("#about").textContent = profile.about;
  for (const tool of profile.toolkit) {
    const card = el("article", "", "card tilt");
    card.append(el("h3", tool.name), el("p", tool.detail));
    $("#toolkit").append(card);
  }
  for (const project of profile.projects) {
    const card = el("a", "", "card tilt");
    card.href = `https://github.com/aditya00801/${REPOS[project.slug] || ""}`;
    card.append(el("p", project.status, "eyebrow"), el("h3", project.title),
      el("p", project.description), el("p", project.tech, "meta"));
    $("#projects").append(card);
  }
  for (const entry of profile.logbook) {
    const item = el("li");
    const body = el("div", entry.title);
    body.append(el("span", entry.issuer));
    item.append(el("time", entry.date), body);
    $("#logbook").append(item);
  }
}

// ---- Contribution city (isometric SVG) ----
function shade(hex, factor) {
  return "#" + [1, 3, 5].map((i) =>
    Math.floor(parseInt(hex.slice(i, i + 2), 16) * factor).toString(16).padStart(2, "0")).join("");
}

function renderCity({ days }) {
  const svg = $("#skyline");
  const make = (tag, attributes, parent) => {
    const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
    parent.append(node);
    return node;
  };
  const point = (w, d, h = 0) => `${108 + w * 12.8 - d * 9.6},${150 + w * 3.7 + d * 7 - h}`;
  const polygon = (points, fill, parent) => make("polygon", { points: points.join(" "), fill }, parent);
  const start = new Date(days[0].date + "T00:00:00Z");
  start.setUTCDate(start.getUTCDate() - start.getUTCDay());
  const cells = days.map((day) => {
    const offset = Math.round((new Date(day.date + "T00:00:00Z") - start) / 864e5);
    return { ...day, w: Math.floor(offset / 7), d: offset % 7 };
  });
  const peak = Math.max(1, ...cells.map((c) => c.count));
  for (const { w, d } of cells) {
    polygon([point(w, d), point(w + .86, d), point(w + .86, d + .86), point(w, d + .86)], "#B7BEA9", svg);
  }
  const readout = $("#readout");
  let active;
  const active_days = cells.filter((c) => c.count)
    .sort((a, b) => (a.w * 3.7 + a.d * 7) - (b.w * 3.7 + b.d * 7));
  for (const { w, d, count, date } of active_days) {
    const level = Math.sqrt(count / peak);
    const h = 10 + 92 * level;
    const top = level < .35 ? "#A9B887" : level < .65 ? "#718064" : "#2E3D28";
    const when = new Date(date + "T00:00:00Z").toLocaleDateString("en-GB",
      { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
    const label = `${when}: ${count} contribution${count === 1 ? "" : "s"}`;
    const group = make("g", { class: "building", tabindex: "0", role: "img", "aria-label": label }, svg);
    const a = .08, e = .78;
    polygon([point(w + a, d + e), point(w + e, d + e), point(w + e, d + e, h), point(w + a, d + e, h)], shade(top, .82), group);
    polygon([point(w + e, d + a), point(w + e, d + e), point(w + e, d + e, h), point(w + e, d + a, h)], shade(top, .66), group);
    polygon([point(w + a, d + a, h), point(w + e, d + a, h), point(w + e, d + e, h), point(w + a, d + e, h)], top, group);
    const show = () => {
      active?.classList.remove("active");
      active = group;
      group.classList.add("active");
      readout.textContent = label;
    };
    for (const type of ["pointerenter", "focus", "click"]) group.addEventListener(type, show);
    if (!calm) {
      group.animate([{ opacity: 0, translate: "0 24px" }, { opacity: 1, translate: "0 0" }],
        { duration: 600, delay: w * 30, easing: "ease-out", fill: "backwards" });
    }
  }
}

// ---- Cursor effects (one listener for the whole page) ----
function followCursor() {
  if (!mouse || calm) return;
  const ring = $(".cursor");
  let x = 0, y = 0, ringX = 0, ringY = 0, running = false;
  const step = () => {
    ringX += (x - ringX) * .22;
    ringY += (y - ringY) * .22;
    ring.style.transform = `translate(${ringX}px, ${ringY}px)`;
    running = Math.abs(x - ringX) + Math.abs(y - ringY) > .3;
    if (running) requestAnimationFrame(step);
  };
  let hovered;
  const reset = (card) => ["--mx", "--my", "--rx", "--ry"].forEach((name) => card.style.removeProperty(name));
  addEventListener("pointermove", (event) => {
    x = event.clientX;
    y = event.clientY;
    ring.classList.add("on");
    ring.classList.toggle("big", Boolean(event.target.closest("a, .building, li")));
    if (!running) { running = true; requestAnimationFrame(step); }
    const card = event.target.closest(".panel, .card");
    if (hovered && hovered !== card) reset(hovered);
    hovered = card;
    if (!card) return;
    const box = card.getBoundingClientRect();
    const px = (x - box.left) / box.width, py = (y - box.top) / box.height;
    card.style.setProperty("--mx", `${x - box.left}px`);
    card.style.setProperty("--my", `${y - box.top}px`);
    if (card.classList.contains("tilt")) {
      const strength = card.classList.contains("card") ? 10 : 4;
      card.style.setProperty("--rx", `${(.5 - py) * strength}deg`);
      card.style.setProperty("--ry", `${(px - .5) * strength}deg`);
    }
  });
  document.documentElement.addEventListener("pointerleave", () => {
    ring.classList.remove("on");
    if (hovered) reset(hovered);
  });
}

function revealOnScroll() {
  if (calm || !("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add("visible");
    observer.unobserve(entry.target);
  }));
  document.querySelectorAll("main > section").forEach((section) => {
    section.classList.add("reveal");
    observer.observe(section);
  });
}

followCursor();
Promise.all([load("profile.json").then(renderProfile), load("contributions.json").then(renderCity)])
  .catch((error) => { console.error(error); $("#error").hidden = false; })
  .finally(() => {
    revealOnScroll();
    if (location.hash === "#city") $("#city").scrollIntoView();
  });
