"use strict";
const progress = document.querySelector(".progress");
const updateProgress = () => {
  const distance = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${distance > 0 ? Math.min(100, window.scrollY / distance * 100) : 0}%`;
};
window.addEventListener("scroll", updateProgress, {passive: true});
window.addEventListener("resize", updateProgress);
updateProgress();
if ("IntersectionObserver" in window) {
  const links = Array.from(document.querySelectorAll(".side-nav a"));
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      for (const link of links) {
        const active = link.hash === `#${entry.target.id}`;
        link.classList.toggle("active", active);
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      }
    }
  }, {rootMargin: "-8% 0px -65% 0px"});
  document.querySelectorAll(".section[id]").forEach(section => observer.observe(section));
}
