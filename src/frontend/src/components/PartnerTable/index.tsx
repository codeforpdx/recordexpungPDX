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
        website: "https://www.pcc.edu/clear-clinic/services/",
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
        contacts: [
          "Sarah Kolb",
          "medfordexpungementclinic@gmail.com",
          "541-778-4473",
        ],
        website: "https://www.facebook.com/Ruraloregonexpungement",
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
    ];
    let partners;
    const toggleOpen = (order: any) => {
      this.setState({ active: order === this.state.active ? -1 : order });
    };

    partners = partnerData.map((partner, index) => (
      <li className="bt bw2 b--lightest-blue1">
        <Disclosure
          open={index === this.state.active}
          id={index}
          onChange={() => toggleOpen(index)}
        >
          <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3">
            <span className="w-70 db pr3 mb2 mb0-ns">{partner.name}</span>
            <span className="w-30 pr3">{partner.area}</span>
            <span className="absolute top-0 right-0 pt3 ph3">
              {index == this.state.active ? (
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
                  <li className="flex-ns mb3">
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
                  <li className="mb3">{contact}</li>
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
            xmlns="http://www.w3.org/2000/svg"
            style={{ width: 55, height: 40 }}
            className="mr3"
            viewBox="0 0 55 40"
          >
            <g fill="none" fillRule="evenodd" transform="translate(.938 .41)">
              <path
                fill="#D0E1F7"
                d="M2.345 38.801L0 33.61l2.345-7.923L3.35 13.442 5.3 0h3.652l3.07 1.501.795 4.37 4.408.887 3.927-.887 3.926.887 1.888-1.77h4.019l2.488-1.116 3.72-.897h12.88l3.278 2.896-1.886 6.434-2.858 5.55L50.7 19.4l-.628 3.215V38.8z"
              ></path>
              <circle cx="12.442" cy="10.117" r="1.382" fill="#2B75D2"></circle>
              <circle cx="15.898" cy="11.845" r="1.382" fill="#2B75D2"></circle>
              <circle cx="13.133" cy="14.609" r="1.382" fill="#2B75D2"></circle>
              <circle cx="16.589" cy="32.235" r="1.382" fill="#2B75D2"></circle>
              <circle cx="8.986" cy="21.867" r="1.382" fill="#2B75D2"></circle>
              <circle cx="26.957" cy="21.867" r="1.382" fill="#2B75D2"></circle>
            </g>
          </svg>
        </div>
        <ul className="list">{partners}</ul>
      </div>
    );
  }
}

export default PartnerTable;
