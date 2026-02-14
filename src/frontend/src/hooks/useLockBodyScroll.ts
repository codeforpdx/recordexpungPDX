import { useEffect } from "react";

/**
 * Prevents body scrolling when `locked` is `true`.
 * Restores scroll on unlock or unmount.
 */
function useLockBodyScroll(locked: boolean) {
  useEffect(() => {
    if (locked) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [locked]);
}

export default useLockBodyScroll;
