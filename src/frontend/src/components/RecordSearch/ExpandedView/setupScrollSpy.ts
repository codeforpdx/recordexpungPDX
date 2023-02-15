export default function setUpScrollSpy() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const elemId = entry.target.getAttribute("id");

        if (!elemId) return;

        const split = elemId.split("_");
        const type = split[1];
        const id = split[2];
        const linkItem = document.querySelector(`#scroll-spy-target-${id}`);
        const theClass = type === "case" ? "fw9" : "bg-lightest-blue";
        if (entry.isIntersecting) {
          linkItem?.classList.add(theClass);
        } else {
          linkItem?.classList.remove(theClass);
        }
      });
    },
    { rootMargin: "-25% 0% -75% 0%" }
  );

  document.querySelectorAll("li[id]").forEach((section) => {
    observer.observe(section);
  });

  return () => observer.disconnect();
}
