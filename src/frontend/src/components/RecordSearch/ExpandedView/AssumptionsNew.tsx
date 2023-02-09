function Item({ text }: { text: string }) {
  return (
    <li className="mb4">
      <div className="flex flex-wrap">
        <i className="fa fa-check green f3 fr pr3"></i>
        <p className="w-90-l w-80">{text}</p>
      </div>
    </li>
  );
}

export default function AssumptionsNew({ ...props }) {
  return (
    <ul {...props}>
      <Item text="No open cases in any court in the United States" />

      <p className="f4 fw7 mv4">Within the last seven years:</p>
      <Item text="No previously expunged cases" />
      <Item text="No cases are from states besides Oregon" />
      <Item text="No Federal Court cases" />
      <Item
        text="No local District Courts cases, e.g. Medford Municipal Court (not
          Jackson County Circuit Court)"
      />
    </ul>
  );
}
