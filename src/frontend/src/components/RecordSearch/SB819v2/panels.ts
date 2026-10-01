/** The record summary and the SB-819 header swap places at the top when the view toggles. */
export const RECORD_SUMMARY_PANEL_ID = "record-summary-panel";
export const SB819_HEADER_PANEL_ID = "sb819-summary-panel";

/**
 * Brings a panel to the top after the view swaps. The panel is mounted by the same state
 * change, so this waits a frame for React to commit. The panels carry `scroll-mt-20` to
 * clear the fixed header.
 */
export function scrollToPanel(id: string) {
  requestAnimationFrame(() => {
    document.getElementById(id)?.scrollIntoView?.({ block: "start" });
  });
}
