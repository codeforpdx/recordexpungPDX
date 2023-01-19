// Reference: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/

import React, { useState, useEffect } from "react";

export interface DisclosureButtonProps {
  "aria-controls": string;
  "aria-expanded": boolean;
  onClick: React.MouseEventHandler;
  onKeyDown: React.KeyboardEventHandler;
}

export interface DisclosureContentProps {
  id: string;
  hidden?: boolean;
}

interface UseDisclosureParams {
  id?: string;
  isOpenToStart?: boolean;
  callback?: (id: string) => any;
}

export default function useDisclosure({
  id = "panel--disclosure",
  isOpenToStart = false,
  callback,
}: UseDisclosureParams = {}) {
  const [disclosureIsExpanded, setIsExpanded] = useState(isOpenToStart);

  const onClick = (event: React.MouseEvent) => {
    event.preventDefault();
    setIsExpanded(!disclosureIsExpanded);
  };

  const onKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === " " || event.key === "Enter") {
      event.preventDefault();
      setIsExpanded(!disclosureIsExpanded);
    }
  };

  useEffect(() => {
    if (callback && disclosureIsExpanded) {
      callback(id);
    }
  }, [callback, id, disclosureIsExpanded]);

  const disclosureButtonProps: DisclosureButtonProps = {
    "aria-controls": id,
    "aria-expanded": disclosureIsExpanded,
    onClick,
    onKeyDown,
  };

  const disclosureContentProps: DisclosureContentProps = {
    id,
    hidden: !disclosureIsExpanded,
  };

  return {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
    setIsExpanded,
  };
}
