export default function setupPage(pageName: string, scrollTop = false) {
  document.title = pageName + " - RecordSponge";
  if (scrollTop) {
    window.scrollTo(0, 0);
  }
}
