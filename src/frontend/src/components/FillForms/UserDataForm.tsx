import React, { useState } from "react";
import { downloadExpungementPacket } from "../../redux/search/actions";
import InvalidInputs from "../InvalidInputs";
import { useAppSelector } from "../../redux/hooks";
import { useDispatch } from "react-redux";
import EmptyFieldsModal from "./EmptyFieldsModal";
import { selectSearchFormValues } from "../../redux/searchFormSlice";
import { isBlank, objectToArray } from "../../service/validators";
import { Redirect } from "react-router-dom";

const isPresent = (str: string) => !isBlank(str);

const errorMessagesObjectToArray = (obj: object) => objectToArray(obj);

const isPhoneNumber = (str: string) => {
  //the phone RegEx accepts the following formats (123) 456-7890, 123-456-7890, 123.456.7890, 1234567890, (123)-456-7890
  return /^(\(?\d{3}\)?[-.\s]?){2}\d{4}$/.test(str); // Check for empty string included
};

const isZipCode = (str: string) => {
  //the zipCode RegEx accepts any 5 digit entry ex. "12345"
  return /[0-9][0-9][0-9][0-9][0-9]/.test(str); // Check for empty string included
};

export default function UserDataForm() {
  const aliases = useAppSelector(selectSearchFormValues).aliases;
  const dispatch = useDispatch();
  const [name, setName] = useState(buildName());
  const [dob, setDob] = useState(aliases[0].birth_date);
  const [mailingAddress, setMailingAddress] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("Oregon");
  const [zipCode, setZipCode] = useState("");
  const [errorMessages, setErrorMessages] = useState<string[]>([]);
  const loadingExpungementPacket = useAppSelector(
    (state) => state.search.loadingExpungementPacket
  );

  const [showModal, setShowModal] = useState(false);

  function buildName() {
    const { first_name, middle_name, last_name } = aliases[0];
    let fullName = "";
    fullName += first_name ? first_name + " " : "";
    fullName += middle_name ? middle_name + " " : "";
    fullName += last_name;

    return fullName.includes("*") ? "" : fullName || " ";
  }

  function allInputsValid() {
    const errorMessages = {
      "Zip code must lead with five digits":
        isPresent(zipCode) && !isZipCode(zipCode),
      "Phone number must be a valid 10 digit number":
        isPresent(phoneNumber) && !isPhoneNumber(phoneNumber),
    };

    if (errorMessagesObjectToArray(errorMessages).length === 0) return true;

    setErrorMessages(errorMessagesObjectToArray(errorMessages));
    return false;
  }

  function downloadPacket() {
    dispatch(
      downloadExpungementPacket(
        name,
        dob,
        mailingAddress,
        phoneNumber,
        city,
        state,
        zipCode
      )
    );
  }

  function handleSubmit(e: React.BaseSyntheticEvent) {
    e.preventDefault();

    if (!allInputsValid()) return;

    setErrorMessages([]);

    const allFormInputsPresent = [
      name,
      dob,
      mailingAddress,
      city,
      state,
      zipCode,
      phoneNumber,
    ].every(isPresent);

    allFormInputsPresent ? downloadPacket() : setShowModal(true);
  }

  if (aliases.length === 0) return <Redirect to="/record-search" />;

  return (
    <main className="mw6">
      <EmptyFieldsModal
        close={!showModal}
        onClose={() => setShowModal(false)}
        onDownload={downloadPacket}
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
        <InvalidInputs contents={errorMessages} />
      </section>
    </main>
  );
}
