import { useState, useEffect } from "react";

export default function useSetupPage(pageName: string, scrollTop = false) {
  const [title, setTitle] = useState(pageName);
  const [shouldScrollTop, setShouldScrollTop] = useState(scrollTop);

  useEffect(() => {
    document.title = title + " - RecordSponge";
  }, [title]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [shouldScrollTop]);

  return { title, setTitle, shouldScrollTop, setShouldScrollTop };
}
