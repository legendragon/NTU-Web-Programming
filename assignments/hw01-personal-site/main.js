const revealTargets = Array.from(document.querySelectorAll("[data-reveal]"));
const nodesContainer = document.getElementById("nodes");
const yearEl = document.getElementById("year");
const menuButton = document.querySelector(".menu");
const nav = document.querySelector(".nav");
const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    }
  },
  { threshold: 0.2 }
);
revealTargets.forEach((target) => observer.observe(target));
if (nodesContainer) {
  for (let i = 0; i < 18; i += 1) {
    const dot = document.createElement("span");
    const size = 6 + Math.random() * 8;
    dot.style.width = `${size}px`;
    dot.style.height = `${size}px`;
    dot.style.left = `${Math.random() * 100}%`;
    dot.style.top = `${Math.random() * 100}%`;
    dot.style.position = "absolute";
    dot.style.borderRadius = "50%";
    dot.style.background = i % 2 === 0 ? "#f4c8c1" : "#9fb6c8";
    dot.style.opacity = "0.5";
    nodesContainer.appendChild(dot);
  }
}
if (yearEl) {
  yearEl.textContent = new Date().getFullYear().toString();
}
menuButton?.addEventListener("click", () => {
  if (!nav) return;
  const isOpen = nav.style.display === "flex";
  nav.style.display = isOpen ? "none" : "flex";
  nav.style.flexDirection = "column";
  nav.style.position = "absolute";
  nav.style.right = "6vw";
  nav.style.top = "70px";
  nav.style.background = "#fff";
  nav.style.padding = "12px 16px";
  nav.style.borderRadius = "16px";
  nav.style.boxShadow = "0 20px 40px rgba(140, 90, 80, 0.2)";
});
