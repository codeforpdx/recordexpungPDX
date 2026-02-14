/**
 * Opens all `<details>` ancestors of the given element
 * so nested accordion content becomes visible.
 */
export function openDetailsAncestors(el: HTMLElement) {
  let current: HTMLElement | null = el;
  while (current) {
    if (current.tagName === "DETAILS") {
      (current as HTMLDetailsElement).open = true;
    }
    current = current.parentElement;
  }
}

/**
 * Finds an element by `id` and opens all its `<details>` ancestors.
 */
export function openDetailsById(id: string) {
  const el = document.getElementById(id);
  if (el) openDetailsAncestors(el);
}
