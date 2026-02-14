import React from "react";
import { HashLink as Link } from "react-router-hash-link";
import AddButton from "../RecordSearch/Record/AddButton";
import EditButton from "../RecordSearch/Record/EditButton";
import EditedBadge from "../RecordSearch/Record/EditedBadge";
import { createNextBlankCharge } from "../RecordSearch/Record/Case";
import EditChargePanel from "../RecordSearch/Record/EditChargePanel";
import Accordion from "../common/Accordion";

export default function EditingGuide() {
  return (
    <Accordion title="Editing Guide" id="editing">
      <div className="mt1">
        <p className="mb3">
          RecordSponge allows in-line editing of search results to correct any
          errors or missing information. This is an advanced feature.
        </p>
        <h3 className="f4 fw7">Why Edit</h3>
        <section className="mb2">
          <p className="mb3">
            Sometimes the result of a Search doesn’t completely match a person’s
            true record. This can happen for a few reasons:
          </p>
          <ol className="mh4">
            <li className="mb3 pb1">
              The search returns the wrong person's record: In rare cases,
              another person with the same name and birth date may appear in
              results.
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
            OECI at all. Editing is built directly into the main Search feature.
          </p>
          <h3 className="f4 fw7">Enable Editing</h3>
          <p className="mb3">
            Click the "Enable Editing" button on the Record Search page:
          </p>
          <span
            className="inline-flex bg-white f6 fw5 br2 ba b--black-10 mid-gray pv1 ph2 mb3"
            aria-hidden="true"
          >
            Enable Editing
          </span>
          <p className="mb3">
            You can now perform the following actions to change the contents of
            the record. Edits are temporary and persist while you navigate the
            site, but will reset if you run a new search or leave
            recordsponge.com.
          </p>
          <h3 className="f4 fw7">Add Case</h3>
          <p className="mb3">
            Click the "Add Case" button just below the Summary panel:
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
          <h3 className="f4 fw7">Edit Case</h3>
          <p className="mb3">
            You can edit any of these fields on an existing or newly created
            case by clicking the "Edit" button in the case's header.
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
          <h3 className="f4 fw7">Add Charge</h3>
          <p>
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
          <p>
            For an existing charge, you can also edit the information by
            clicking the Edit
            <EditButton onClick={() => {}} actionName="Edit Case" />
            button on that charge.
          </p>
          <p>
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
            <Link
              className="bb hover-blue"
              to="/rules#chargetypes"
              target="_blank"
              rel="noreferrer noopener"
            >
              Charge Types
            </Link>{" "}
            so that you can accurately select a charge type for each new or
            edited charge.
          </p>
        </section>
      </div>
    </Accordion>
  );
}
