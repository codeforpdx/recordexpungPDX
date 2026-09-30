/** Ids of the two panels that swap places at the top when the SB-819 view is toggled. */
export const RECORD_SUMMARY_PANEL_ID = "record-summary-panel";
export const SB819_SUMMARY_PANEL_ID = "sb819-summary-panel";

/**
 * Brings a summary panel to the top of the viewport after the view swaps.
 *
 * The panel is mounted by the same state change that triggers the scroll, so this waits a
 * frame for React to commit before measuring. The panels carry `scroll-mt-20`, which keeps
 * them clear of the fixed header.
 */
export default function scrollToPanel(id: string) {
  requestAnimationFrame(() => {
    // scrollIntoView is absent in jsdom, so the call is feature-detected.
    document.getElementById(id)?.scrollIntoView?.({ block: "start" });
  });
}
