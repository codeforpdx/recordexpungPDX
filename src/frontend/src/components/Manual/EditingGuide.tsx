import React from "react";
import { HashLink as Link } from "react-router-hash-link";
import useDisclosure from "../../hooks/useDisclosure";
import AddButton from "../RecordSearch/Record/AddButton";
import EditButton from "../RecordSearch/Record/EditButton";
import EditedBadge from "../RecordSearch/Record/EditedBadge";
import { createNextBlankCharge } from "../RecordSearch/Record/Case";
import EditChargePanel from "../RecordSearch/Record/EditChargePanel";

export default function EditingGuide() {
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
  } = useDisclosure();

  return (
    <div className="bg-gray-blue-2 shadow br3 pa3 mb3">
      <h3 className="f3 fw7 mb2">Editing Results</h3>
      <p className="mb2">
        RecordSponge allows in-line editing of search results to correct any
        errors or missing information. This is an advanced feature.
      </p>
      <button {...disclosureButtonProps}>
        <span className="flex items-center fw6 mid-gray link hover-blue pb1">
          Editing Guide
          <span
            aria-hidden="true"
            className={`pt1 pl1 fas fa-angle-${
              disclosureIsExpanded ? "up" : "down"
            }`}
          ></span>
        </span>
      </button>
      <div {...disclosureContentProps} className="pt3">
        <h3 className="f4 fw7 mb2">Why Edit</h3>
        <section className="mb4">
          <p className="mb3">
            Sometimes the result of a Search doesn’t completely match a person’s
            true record. This can happen for a few reasons:
          </p>
          <ol className="mh4">
            <li className="mb3 pb1">
              The search returns the wrong person’s record: In the rare event
              that a different person’s Oregon record shares a birth date and
              name with the person of interest, these records may appear in the
              search result.
            </li>
            <li className="mb3 pb1">
              One or more of a person’s cases cannot be found: If the record has
              a typo in the name or the incorrect birth date, it can be
              difficult to locate by searching OECI.
            </li>
            <li className="mb3 pb1">
              A charge date or other piece of information for a particular case
              is missing or incorrect in OECI.
            </li>
            <li className="mb3 pb1">
              The expungement analyzer could not classify the charge: Many of
              the records in OECI are older and have statutes that have been
              renumbered or repealed; or a charge has an irregular name not
              recognized by our analyzer.
            </li>
          </ol>
          <p className="mb3">
            If any of these issues appear in the record, they can be corrected
            with the Editing feature. You can also use the Editing feature to
            build a record from scratch and run an analysis without relying on
            OECI at all. Editing is built directly in to the main Search
            feature.
          </p>
          <h3 className="f4 fw7 mb2">Enable Editing</h3>
          <p className="mb3">
            Click the Enable Editing button on the Record Search page:
          </p>
          <button className="inline-flex bg-white f6 fw5 br2 ba b--black-10 mid-gray link hover-blue pv1 ph2 mb3">
            Enable Editing
          </button>
          <p className="mb3">
            You can now perform the following actions to change the contents of
            the record. These changes exist only temporarily in your session and
            will disappear if you run another search. The edits will persist if
            you navigate between Search and the Manual or other pages on
            recordsponge.com, but they will disappear if you leave the website.
          </p>
          <h3 className="f4 fw7 mb2">Add Case</h3>
          <p className="mb3">
            Click the Add Case button just below the Summary panel:
          </p>
          <div className="ma3">
            <AddButton onClick={() => {}} actionName="Add" text="Case" />
          </div>
          <p className="mb3">
            This lets you create a new case from scratch that can be populated
            with new charges. You must provide the case Current Status, County,
            Balance, and Birth Year, all of which are used to provide complete
            analysis of the record.
          </p>
          <h3 className="f4 fw7 mb2">Edit Case</h3>
          <p className="mb3">
            You can edit any of these fields on an existing or newly created
            case by clicking the edit button in the case's header.
          </p>
          <div className="ml3 mb3">
            <EditButton onClick={() => {}} actionName="Edit Case" />
          </div>
          <p className="mb3">
            {" "}
            Creating or editing a case will add a badge to that case indicating
            that the case was created or edited. You can click the badge to undo
            the change.
          </p>
          <div className="flex-l mb3">
            <EditedBadge
              editStatus={"ADD"}
              onClick={() => {}}
              showEditButtons={true}
            />
            <div className="mh2"></div>
            <EditedBadge
              editStatus={"UPDATE"}
              onClick={() => {}}
              showEditButtons={true}
            />
          </div>
          <h3 className="f4 fw7 mb2">Add Charge</h3>
          <p className="mb2">
            Next to the Edit Case{" "}
            <EditButton onClick={() => {}} actionName="Edit Case" /> button is
            another Add{" "}
            <span className="mh1">
              {" "}
              <AddButton
                onClick={() => {}}
                actionName="Add Charge"
                text=""
              />{" "}
            </span>{" "}
            button. This allows you to add charges to a newly-created or
            existing case.
          </p>
          <p className="mb2">
            For an existing charge, you can also the information by clicking the
            Edit
            <EditButton onClick={() => {}} actionName="Edit Case" />
            button on that charge.
          </p>
          <p className="mb2">
            Both of these operations open a similar panel to allow creating or
            editing the charge:
          </p>

          <div className="bg-gray-blue-2 shadow br3 overflow-auto mb4">
            <div className="br3 ma2 bg-white">
              <EditChargePanel
                charge={createNextBlankCharge("123456", 1)}
                isNewCharge={false}
                whenDoneEditing={() => {}}
                handleUndoEditClick={() => {}}
              />
            </div>
          </div>
          <p>
            Creating or editing a charge requires that you select both a
            disposition and a Charge Type. The charge type and disposition
            jointly determine the type-eligibility of the charge. See our
            complete list of{" "}
            <Link className="bb hover-blue" to="/rules#chargetypes">
              {" "}
              Charge Types{" "}
            </Link>{" "}
            so that you can accurately select a charge type for each new or
            edited charge.
          </p>
        </section>
      </div>
    </div>
  );
}
