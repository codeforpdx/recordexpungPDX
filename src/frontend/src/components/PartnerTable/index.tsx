import { useState } from "react";
import { HashLink as Link } from "react-router-hash-link";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";
import currentPartners from "./currentPartners";
import SVG from "../common/SVG";

interface Partner {
  details: string[][];
  name: string;
  area: string;
  instructions: string;
  contacts: string[];
  website: string;
}

interface PartnerElementProps {
  partner: Partner;
  disclosureIdx: number;
  activeIdx: number;
  handleChange: (idx: number) => void;
}

function PartnerElement({
  partner,
  disclosureIdx,
  activeIdx,
  handleChange,
}: PartnerElementProps) {
  return (
    <li className="bt bw2 b--lightest-blue1">
      <Disclosure
        open={disclosureIdx === activeIdx}
        id={disclosureIdx}
        onChange={() => handleChange(disclosureIdx)}
      >
        <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3">
          <span className="w-70 db pr3 mb2 mb0-ns">{partner.name}</span>
          <span className="w-30 pr3">{partner.area}</span>
          <span className="absolute top-0 right-0 pt3 ph3">
            <span
              aria-hidden="true"
              className={`fas fa-angle-${
                disclosureIdx === activeIdx ? "up" : "down"
              }`}
            ></span>
          </span>
        </DisclosureButton>
        <DisclosurePanel>
          <div className="bl bw2 f5 b--blue pv3 ph3 mb3 ml3">
            <ul className="list mb2">
              {partner.details.map((detail, detailsIdx) => (
                <li key={detailsIdx} className="flex-ns mb3">
                  <span className="w10rem db fw6 mr3">{detail[0]}</span>
                  <span>{detail[1]}</span>
                </li>
              ))}
            </ul>
            <p className="mw6 lh-copy mb3">
              The majority of court fees are subject to waiver for
              income-qualified individuals who complete the waiver form.{" "}
              <Link className="link hover-blue bb" to="/manual#filepaperwork">
                Learn More
              </Link>
            </p>
            <hr className="bt b--black-05 mb3" />
            <p className="fw6 mb3">{partner.instructions}</p>
            <ul className="list mb3">
              {partner.contacts.map((contact, contactsIdx) => (
                <li key={contactsIdx} className="mb3">
                  {contact}
                </li>
              ))}
            </ul>
            <a href={partner.website} className="link hover-blue bb">
              {partner.website}
            </a>
          </div>
        </DisclosurePanel>
      </Disclosure>
    </li>
  );
}

export default function PartnerTable({ partners = currentPartners }) {
  // Only one Disclosure should be opened at a particular time.
  // activeIdx === -1 means that all Disclosures are closed
  const [activeIdx, setActiveIdx] = useState(-1);

  const toggleDiscolsure = (newIdx: number) => {
    setActiveIdx(newIdx === activeIdx ? -1 : newIdx);
  };

  return (
    <div className="ba bw3 br3 b--lightest-blue1 bg-white mb6">
      <div className="flex items-center justify-between">
        <h3 className="f3 fw9 pv4 ph3">Partners</h3>
        <SVG
          name="oregonMap"
          className="mr3"
          style={{ width: "55px", height: "40px" }}
          viewBox="0 0 110 80"
        />
      </div>
      <ul className="list">
        {partners.map((partner, index) => (
          <PartnerElement
            partner={partner}
            key={index}
            disclosureIdx={index}
            activeIdx={activeIdx}
            handleChange={toggleDiscolsure}
          />
        ))}
      </ul>
    </div>
  );
}
