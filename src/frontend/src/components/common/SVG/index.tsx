import { ReactNode } from "react";
import Logo from "./Logo";
import OregonMap from "./OregonMap";
import OregonMap2 from "./OregonMap2";
import WhoWeAreLogos from "./WhoWeAreLogos";
import OeciLogo from "./OeciLogo";

type Keys = "logo" | "oregonMap" | "oregonMap2" | "whoWeAreLogos" | "oeciLogo";
const nameDetailsMap: { [key in Keys]: ReactNode } = {
  logo: <Logo />,
  oregonMap: <OregonMap />,
  oregonMap2: <OregonMap2 />,
  whoWeAreLogos: <WhoWeAreLogos />,
  oeciLogo: <OeciLogo />,
};

export default function SVG({
  name = "logo" as Keys,
  xmlns = "http://www.w3.org/2000/svg",
  fill = "none",
  ...props
}) {
  return (
    <svg aria-hidden="true" fill={fill} xmlns={xmlns} {...props}>
      {nameDetailsMap[name]}
    </svg>
  );
}
