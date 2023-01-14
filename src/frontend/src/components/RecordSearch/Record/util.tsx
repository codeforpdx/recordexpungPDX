import React from "react";

export function newlineOrsInString(
  leading_label: JSX.Element,
  eligibilityString: string
) {
  const splittedElements = eligibilityString.split("OR");

  let boldSpliced = splittedElements.map((element: string, index: number) => {
    return (
      <div
        key={index}
        className={(index > 0 && "bt b--light-gray pt2 mt2") + ""}
      >
        {index === 0 ? leading_label : <span className="fw7">OR </span>}
        {convertCaseNumberIntoLinks(element)}
      </div>
    );
  });
  return boldSpliced;
}

export function convertCaseNumberIntoLinks(eligibilityString: string) {
  const elements = eligibilityString.split(/(\[.*?\])/g);
  return elements.map((element: string, index: number) => {
    if (element.match(/^\[.*\]$/)) {
      const caseNumber = element.slice(1, -1);
      return (
        <a className="underline" href={"#" + caseNumber} key={caseNumber}>
          {caseNumber}
        </a>
      );
    } else {
      return element;
    }
  });
}
