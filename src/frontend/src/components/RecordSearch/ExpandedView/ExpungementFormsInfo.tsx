import Aside from "../../common/Aside";

function Item({
  text,
  iconClassName = "fa-check green",
}: {
  text: string;
  iconClassName?: string;
}) {
  return (
    <li className="mv3">
      <div className="flex flex-wrap">
        <i className={"f3 fr pr3 fa " + iconClassName}></i>
        <p className="w-90-l w-80">{text}</p>
      </div>
    </li>
  );
}

export default function ExpungementFormsInfo({ ...props }) {
  const h3Class = "f4 fw7 mb3 ";
  const listClassName = "list mb5";

  return (
    <div {...props}>
      <h3 className={h3Class}>Pre-filled Information</h3>
      <p>For eligible cases the following will be included:</p>
      <ul className={listClassName}>
        <Item text="Case number" />
        <Item text="Charge name" />
        <Item text="Arrest date" />
        <Item text="Conviction or dismissal date" />
      </ul>

      <h3 className={h3Class}>Potentially Missing Information</h3>
      <ul className={listClassName}>
        <Item text="Arresting agency" iconClassName="fa-question blue" />
        <Item
          text="District attorney number"
          iconClassName="fa-question blue"
        />
      </ul>

      <h3 className={h3Class}>Before Mailing Forms</h3>
      <ul className={listClassName}>
        <Item
          text="Verify all information is correct"
          iconClassName="fa-exclamation red"
        />
        <Item
          text="Add additional information as required"
          iconClassName="fa-exclamation red"
        />
      </ul>

      <h3 className={h3Class + "mt5"}>Note</h3>
      <Aside text="Forms can be dowloaded without additional client information. Pre-filled information is based on county records." />
    </div>
  );
}
