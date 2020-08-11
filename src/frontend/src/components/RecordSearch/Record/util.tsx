import React from "react";

export function newlineOrsInString(
  leading_label: JSX.Element,
  eligibilityString: string
) {
  const splittedElements = eligibilityString.split("OR");

  let boldSpliced = splittedElements.map((element: string, index: number) => {
    return (
      <div className={(index > 0 && "bt b--light-gray pt2 mt2") + ""}>
        {index === 0 ? leading_label : <span className="fw7">OR </span>}
        {element}
      </div>
    );
  });
  return boldSpliced;
}
