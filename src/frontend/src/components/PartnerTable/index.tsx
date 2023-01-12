import React from "react";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";
import { HashLink as Link } from "react-router-hash-link";

class PartnerTable extends React.Component<{}, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      active: -1,
    };
  }
  render() {
    let partnerData = [
      {
        details: [
          ["Locations", "Multnomah County"],
          ["Income Restrictions", "Low-income only"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "Free"],
          ["Court Fees", "Not Included"],
        ],
        name: "Portland Community College",
        area: "Northeast Portland",
        instructions: "Contact",
        contacts: ["Leni Tupper"],
        website: "https://www.pcc.edu/clear-clinic/intake-form/",
      },
      {
        details: [
          ["Locations", "Multnomah County"],
          ["Income Restrictions", "No"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "$100/case"],
          ["Court Fees", "Not Included"],
        ],
        name: "Criminals Anonymous",
        area: "East Portland",
        instructions: "Contact",
        contacts: ["hrcubbedge1776@gmail.com"],
        website: "https://www.qiu-qiulaw.com/crimanon",
      },
      {
        details: [
          ["Locations", "Portland Metro"],
          ["Income Restrictions", "None"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "$100/case"],
          ["Court Fees", "Not Included"],
        ],
        name: "Qiu-Qiu Law",
        area: "Portland",
        instructions: "Check your eligibility",
        contacts: [""],
        website: "https://www.qiu-qiulaw.com/recordsponge",
      },
      {
        details: [
          ["Locations", "Portland Metro"],
          ["Income Restrictions", "Unknown"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "Unknown"],
          ["Court Fees", "Not Included"],
        ],
        name: "Clackamas Workforce Partnership",
        area: "Oregon City",
        instructions: "Contact",
        contacts: ["Amanda Wall"],
        website: "https://www.clackamasworkforce.org",
      },
      {
        details: [
          ["Locations", "Central Oregon"],
          ["Income Restrictions", "Unknown"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "Unknown"],
          ["Court Fees", "Not Included"],
        ],
        name: "Lane Public Defender Services",
        area: "Eugene",
        instructions: "Contact",
        contacts: ["Zara Lukens"],
        website: "http://www.lanepds.org",
      },
      {
        details: [
          ["Locations", "Central Oregon"],
          ["Income Restrictions", "Unknown"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "Unknown"],
          ["Court Fees", "Not Included"],
        ],
        name: "Redmond Housing Works",
        area: "Redmond",
        instructions: "Contact",
        contacts: ["Andy Hall"],
        website: "https://www.facebook.com/OregonHousingWorks",
      },
      {
        details: [
          ["Locations", "Jackson County"],
          ["Income Restrictions", "None"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "$100/case"],
          ["Court Fees", "Not Included"],
        ],
        name: "Signs of Hope",
        area: "Medford",
        instructions: "Contact",
        contacts: ["Sarah Kolb", "hope@janekolb.com", "541-821-5577"],
        website: "https://www.janekolb.com",
      },
      {
        details: [
          ["Locations", "Southern Oregon"],
          ["Income Restrictions", "Unknown"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "Unknown"],
          ["Court Fees", "Not Included"],
        ],
        name: "Probation and Parole, Community Justice Center",
        area: "Medford",
        instructions: "Contact",
        contacts: ["Eric Guyer"],
        website: "https://jacksoncountyor.org/community-justice",
      },
      {
        details: [
          ["Locations", "Umatilla County"],
          ["Income Restrictions", "None"],
          ["Analysis Cost", "Free"],
          ["Paperwork Cost", "Free"],
          ["Court Fees", "Not Included"],
        ],
        name: "Pendleton Legal Aid Services of Oregon",
        area: "Pendleton",
        instructions: "Contact",
        contacts: ["Arron Guevara", "arron.guevara@lasoregon.org"],
        website: "https://www.facebook.com/pendletonlegalaid/",
      },
    ];
    let partners;
    const toggleOpen = (order: any) => {
      this.setState({ active: order === this.state.active ? -1 : order });
    };

    partners = partnerData.map((partner, index) => (
      <li key={index} className="bt bw2 b--lightest-blue1">
        <Disclosure
          open={index === this.state.active}
          id={index}
          onChange={() => toggleOpen(index)}
        >
          <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3">
            <span className="w-70 db pr3 mb2 mb0-ns">{partner.name}</span>
            <span className="w-30 pr3">{partner.area}</span>
            <span className="absolute top-0 right-0 pt3 ph3">
              {index === this.state.active ? (
                <span aria-hidden="true" className="fas fa-angle-up"></span>
              ) : (
                <span aria-hidden="true" className="fas fa-angle-down"></span>
              )}
            </span>
          </DisclosureButton>
          <DisclosurePanel>
            <div className="bl bw2 f5 b--blue pv3 ph3 mb3 ml3">
              <ul className="list mb2">
                {partner.details.map((detail, index) => (
                  <li key={index} className="flex-ns mb3">
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
                {partner.contacts.map((contact, index) => (
                  <li key={index} className="mb3">
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
    ));

    return (
      <div className="ba bw3 br3 b--lightest-blue1 bg-white mb4">
        <div className="flex items-center justify-between">
          <h3 className="f3 fw9 pv4 ph3">Partners</h3>
          <svg
            className="mr3"
            style={{ width: "55px", height: "40px" }}
            aria-hidden="true"
            viewBox="0 0 110 80"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M6.56 78.42L1.88 68.04l4.68-15.85L8.58 27.7 12.48.82h7.3l6.14 3 1.59 8.74 8.81 1.77 7.86-1.77 7.85 1.77 3.78-3.54h8.03l4.98-2.23 7.44-1.8h25.76l6.56 5.8-3.77 12.87-5.72 11.1 4.19 3.09-1.26 6.43v32.37H6.56z"
              fill="#D0E1F7"
            />
            <circle cx="26.76" cy="21.05" r="2.76" fill="#2B75D2" />
            <circle cx="33.67" cy="24.51" r="2.76" fill="#2B75D2" />
            <circle cx="79.67" cy="16.51" r="2.76" fill="#2B75D2" />
            <circle cx="28.14" cy="30.04" r="2.76" fill="#2B75D2" />
            <circle cx="35.05" cy="65.29" r="2.76" fill="#2B75D2" />
            <circle cx="19.85" cy="44.55" r="2.76" fill="#2B75D2" />
            <circle cx="55.79" cy="44.55" r="2.76" fill="#2B75D2" />
          </svg>
        </div>
        <ul className="list">{partners}</ul>
      </div>
    );
  }
}

export default PartnerTable;
