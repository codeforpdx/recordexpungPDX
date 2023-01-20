// https://www.w3.org/WAI/ARIA/apg/patterns/accordion/

import React, { useState, useEffect, Dispatch } from "react";
import useDisclosure, {
  DisclosureButtonProps,
  DisclosureContentProps,
} from "../useDisclosure";

export type UseAccordionSection = ({
  id,
}: {
  id: string;
}) => {
  isExpanded: boolean;
  headerProps: DisclosureButtonProps;
  panelProps: DisclosureContentProps;
};
// Use useAccordion in a parent element and then pass
// useAccordionSection to each child element that will represent
// the accordion section that contains the heading and panel.
// Use buttons for headings to allow tabbing.
export default function useAccordion(idPrefix = "accordion") {
  const [openPanelId, setOpenPanelId] = useState("");
  const isExpandedSetters: {
    [id in string]: Dispatch<React.SetStateAction<boolean>>;
  } = {};

  // Do not use map iterators for id's. They can cause odd behavior.
  const useAccordionSection = ({ id }: { id: string }) => {
    const id_ = `${idPrefix}-panel-${id}`;
    const {
      disclosureIsExpanded: isExpanded,
      disclosureButtonProps: headerProps,
      disclosureContentProps: panelProps,
      setIsExpanded,
    } = useDisclosure({
      id: id_,
      callback: setOpenPanelId,
    });

    isExpandedSetters[id_] = setIsExpanded;

    return {
      isExpanded,
      headerProps,
      panelProps,
    };
  };

  useEffect(() => {
    Object.entries(isExpandedSetters).forEach(([id, setIsExpanded]) => {
      if (id !== openPanelId) {
        setIsExpanded(false);
      }
    });
    // eslint-disable-next-line
  }, [openPanelId]);

  return {
    useAccordionSection,
  };
}
