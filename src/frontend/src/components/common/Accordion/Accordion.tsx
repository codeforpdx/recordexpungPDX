import { useEffect, useRef } from "react";
import { openDetailsAncestors } from "./openDetails";

interface Props {
  title: string;
  type?: "qna";
  id?: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}

/**
 * Collapsible content section built on the native `<details>` element.
 * Automatically opens when the URL hash matches its `id`, including nested accordions.
 * Set `type` to `"qna"` for a Q&A-style header.
 */
function Accordion({ title, type, id, defaultOpen, children }: Props) {
  const detailsRef = useRef<HTMLDetailsElement>(null);
  const contentRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const details = detailsRef.current;
    if (!details) return;

    const handleToggle = () => {
      if (details.open && contentRef.current) {
        contentRef.current.style.animation = "none";
        requestAnimationFrame(() => {
          if (contentRef.current) {
            contentRef.current.style.animation = "";
          }
        });
      }
    };

    details.addEventListener("toggle", handleToggle);
    return () => details.removeEventListener("toggle", handleToggle);
  }, []);

  useEffect(() => {
    if (!id) return;

    const openIfHashMatches = () => {
      if (window.location.hash === `#${id}` && detailsRef.current) {
        openDetailsAncestors(detailsRef.current);
      }
    };

    openIfHashMatches();
    window.addEventListener("hashchange", openIfHashMatches);
    return () => window.removeEventListener("hashchange", openIfHashMatches);
  }, [id]);

  return (
    <details ref={detailsRef} className="accordion-details ba pa2 br3 scroll-mt-20" id={id} open={defaultOpen}>
      {type === "qna" ? (
        <summary aria-label={title}>
          <strong>Q: </strong> {title}
        </summary>
      ) : (
        <summary className="f4 fw7" aria-label={title}>
          {title}
        </summary>
      )}
      <section ref={contentRef} className="pl2 pr2 mb1 content">
        {children}
      </section>
    </details>
  );
}

export default Accordion;
