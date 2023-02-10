import React from "react";

interface Props {
  conditions?: boolean[];
  contents: JSX.Element[] | string[];
}

export default function InvalidInputs({
  conditions = undefined,
  contents,
}: Props) {
  return (
    <div role="alert" className="black-70 w-100">
      {contents.map((content, i) => {
        const message = (
          <p key={i} className="bg-washed-red mv3 pa3 br3 fw6">
            {content}
          </p>
        );
        return conditions ? conditions[i] && message : message;
      })}
    </div>
  );
}
