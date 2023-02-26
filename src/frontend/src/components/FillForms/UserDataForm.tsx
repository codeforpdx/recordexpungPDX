import React, { useState, useEffect } from "react";
import history from "../../service/history";
import { downloadExpungementPacket } from "../../redux/search/actions";
import InvalidInputs from "../InvalidInputs";
import moment from "moment";
import { useAppSelector } from "../../redux/hooks";
import { useDispatch } from "react-redux";
import EmptyFieldsModal from "./EmptyFieldsModal";
import {
  initialState,
  selectSearchFormValues,
} from "../../redux/searchFormSlice";
import { isBlank } from "../../service/validators";

export default function UserDataForm() {
  const aliases = useAppSelector(selectSearchFormValues).aliases;
  const dispatch = useDispatch();
  const [name, setName] = useState(buildName());
  const [dob, setDob] = useState(buildDob());
  const [mailingAddress, setMailingAddress] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("Oregon");
  const [zipCode, setZipCode] = useState("");
  const [invalidZipCode, setInvalidZipCode] = useState(false);
  const [invalidPhone, setInvalidPhone] = useState(false);
  const [invalidBirthDate, setInvalidBirthDate] = useState(false);
  const loadingExpungementPacket = useAppSelector(
    (state) => state.search.loadingExpungementPacket
  );
  const [modalClose, setModalClose] = useState(true);

  function buildName() {
    if (aliases.length > 0) {
      const firstAlias = aliases[0];
      const nameString = `${firstAlias.first_name} ${
        firstAlias.middle_name ? firstAlias.middle_name + " " : ""
      }${firstAlias.last_name}`;
      if (!nameString.includes("*")) {
        return nameString;
      } else {
        return "";
      }
    } else {
      return "";
    }
  }

  function buildDob() {
    if (aliases.length > 0) {
      const firstAlias = aliases[0];
      return firstAlias.birth_date;
    } else {
      return "";
    }
  }

  function emptyFieldsCheck() {
    if (
      ![zipCode, phoneNumber, dob, mailingAddress, city, state, name].some(
        isBlank
      )
    )
      return true;

    setModalClose(false);
  }

  function validateForm() {
    //the phone RegEx accecpts the following formats (123) 456-7890, 123-456-7890, 123.456.7890, 1234567890, (123)-456-7890
    const phoneNumberPattern = new RegExp(
      "^\\(?(\\d{3})\\)?[-.\\s]?(\\d{3})[-.\\s]?(\\d{4})$"
    );
    //the zipCode RegEx accepts any 5 digit entry ex. "12345"
    const zipCodePattern = new RegExp("[0-9][0-9][0-9][0-9][0-9]");
    const phoneNumberMatch = phoneNumberPattern.test(phoneNumber);
    const zipCodeMatch = zipCodePattern.test(zipCode);
    const isValidZipCode = zipCode.length > 0 && zipCodeMatch;
    const isValidPhoneNumber = phoneNumber.length > 0 && phoneNumberMatch;
    const isValidBirthDate =
      dob.length > 0 && moment(dob, "M/D/YYYY", true).isValid();

    setInvalidZipCode(!isValidZipCode);
    setInvalidPhone(!isValidPhoneNumber);
    setInvalidBirthDate(!isValidBirthDate);

    return isValidZipCode && isValidBirthDate && isValidPhoneNumber;
  }

  function handleSubmit(e: React.BaseSyntheticEvent) {
    e.preventDefault();
    if (emptyFieldsCheck() && validateForm()) {
      return downloadExpungementPacket(
        name,
        dob,
        mailingAddress,
        phoneNumber,
        city,
        state,
        zipCode
      )(dispatch);
    }
  }

  useEffect(() => {
    if (!(aliases.length > 0)) {
      return history.push("/record-search");
    }
  });

  return (
    <>
      <main className="mw6">
        <EmptyFieldsModal
          close={modalClose}
          onClose={() => setModalClose(true)}
          onDownload={() =>
            downloadExpungementPacket(
              name,
              dob,
              mailingAddress,
              phoneNumber,
              city,
              state,
              zipCode
            )(dispatch)
          }
        />
        <section className="cf pa3 pa4-ns bg-white shadow br3">
          <h1 className="f4 fw7 mt0 mb4">User Information</h1>
          <form onSubmit={handleSubmit} noValidate={true}>
            <legend className="visually-hidden">User Information</legend>
            <div className="mb4">
              <label htmlFor="name" className="db mb1 fw6">
                Full Name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                onChange={(e) => setName(e.target.value)}
                value={name}
              />
            </div>
            <div className="mb4">
              <label htmlFor="dob" className="db mb1">
                <span className="fw6"> Date of Birth </span>{" "}
                <span className="fw2">mm/dd/yyyy </span>
              </label>
              <input
                id="dob"
                name="dob"
                type="text"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                onChange={(e) => setDob(e.target.value)}
                value={dob}
              />
            </div>
            <div className="mb4">
              <label htmlFor="mailingAddress" className="db mb1 fw6">
                Mailing Street Address
              </label>
              <input
                id="mailingAddress"
                name="mailingAddress"
                type="text"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                onChange={(e) => setMailingAddress(e.target.value)}
                value={mailingAddress}
              />
            </div>
            <div className="mb4">
              <label htmlFor="city" className="db mb1 fw6">
                City
              </label>
              <input
                id="city"
                name="city"
                type="text"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                onChange={(e) => setCity(e.target.value)}
                value={city}
              />
            </div>
            <div className="mb4">
              <label htmlFor="state" className="db mb1 fw6">
                State
              </label>
              <div className="relative">
                <select
                  id="state"
                  name="state"
                  required={true}
                  className="w-100 pa3 br2 bw1 b--black-20 input-reset bg-white"
                  onChange={(e) => setState(e.target.value)}
                  value={state}
                >
                  <option value=""></option>
                  <option value="Alabama">Alabama</option>
                  <option value="Alaska">Alaska</option>
                  <option value="American Samoa">American Samoa</option>
                  <option value="Arizona">Arizona</option>
                  <option value="Arkansas">Arkansas</option>
                  <option value="California">California</option>
                  <option value="Colorado">Colorado</option>
                  <option value="Connecticut">Connecticut</option>
                  <option value="Delaware">Delaware</option>
                  <option value="District Of Columbia">
                    District Of Columbia
                  </option>
                  <option value="Florida">Florida</option>
                  <option value="Georgia">Georgia</option>
                  <option value="Guam">Guam</option>
                  <option value="Hawaii">Hawaii</option>
                  <option value="Idaho">Idaho</option>
                  <option value="Illinois">Illinois</option>
                  <option value="Indiana">Indiana</option>
                  <option value="Iowa">Iowa</option>
                  <option value="Kansas">Kansas</option>
                  <option value="Kentucky">Kentucky</option>
                  <option value="Louisiana">Louisiana</option>
                  <option value="Maine">Maine</option>
                  <option value="Maryland">Maryland</option>
                  <option value="Massachusetts">Massachusetts</option>
                  <option value="Michigan">Michigan</option>
                  <option value="Minnesota">Minnesota</option>
                  <option value="Mississippi">Mississippi</option>
                  <option value="Missouri">Missouri</option>
                  <option value="Montana">Montana</option>
                  <option value="Nebraska">Nebraska</option>
                  <option value="Nevada">Nevada</option>
                  <option value="New Hampshire">New Hampshire</option>
                  <option value="New Jersey">New Jersey</option>
                  <option value="New Mexico">New Mexico</option>
                  <option value="New York">New York</option>
                  <option value="North Carolina">North Carolina</option>
                  <option value="North Dakota">North Dakota</option>
                  <option value="Northern Mariana Islands">
                    Northern Mariana Islands
                  </option>
                  <option value="Ohio">Ohio</option>
                  <option value="Oklahoma">Oklahoma</option>
                  <option value="Oregon">Oregon</option>
                  <option value="Pennsylvania">Pennsylvania</option>
                  <option value="Puerto Rico">Puerto Rico</option>
                  <option value="Rhode Island">Rhode Island</option>
                  <option value="South Carolina">South Carolina</option>
                  <option value="South Dakota">South Dakota</option>
                  <option value="Tennessee">Tennessee</option>
                  <option value="Texas">Texas</option>
                  <option value="United States Minor Outlying Islands">
                    United States Minor Outlying Islands
                  </option>
                  <option value="Utah">Utah</option>
                  <option value="Vermont">Vermont</option>
                  <option value="Virgin Islands">Virgin Islands</option>
                  <option value="Virginia">Virginia</option>
                  <option value="Washington">Washington</option>
                  <option value="West Virginia">West Virginia</option>
                  <option value="Wisconsin">Wisconsin</option>
                  <option value="Wyoming">Wyoming</option>
                </select>
                <div className="absolute pa3 right-0 top-0 bottom-0 pointer-events-none">
                  <i aria-hidden="true" className="fas fa-angle-down"></i>
                </div>
              </div>
            </div>
            <div className="mb4">
              <label htmlFor="zipCode" className="db mb1 fw6">
                Zip code
              </label>

              <input
                id="zipCode"
                name="zipCode"
                type="text"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                onChange={(e) => setZipCode(e.target.value)}
                value={zipCode}
              />
            </div>
            <div className="mb4">
              <label htmlFor="phoneNumber" className="db mb1">
                <span className="fw6"> Phone Number </span>{" "}
              </label>
              <input
                id="phoneNumber"
                name="phoneNumber"
                type="text"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                onChange={(e) => setPhoneNumber(e.target.value)}
                value={phoneNumber}
              />
            </div>
            <button
              className={`bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc ${
                loadingExpungementPacket ? " loading-btn" : ""
              }`}
            >
              Download Expungement Packet
            </button>
          </form>
          <InvalidInputs
            conditions={[invalidZipCode, invalidPhone, invalidBirthDate]}
            contents={[
              <span>Zip code must lead with five digits</span>,
              <span>Phone number must contain a digit</span>,
              <span>Date Birth format must be mm/dd/yyyy</span>,
            ]}
          />
        </section>
      </main>
    </>
  );
}
