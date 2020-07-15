import React from "react";
import AddButton from "../RecordSearch/Record/AddButton";
import EditButton from "../RecordSearch/Record/EditButton";
import EditedBadge from "../RecordSearch/Record/EditedBadge";
import { createNextBlankCharge } from "../RecordSearch/Record/Case";
import EditChargePanel from "../RecordSearch/Record/EditChargePanel";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";

export default class EditingGuide extends React.Component {
  render() {
    return (
      <>
        <h3 className="f4 fw7 mb2" id="searchresults">
          Why Edit
        </h3>
        <section className="mb5">
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
          <h3 className="f4 fw7 mb2" id="searchresults">
            Enable Editing
          </h3>
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
          <h3 className="f4 fw7 mb2" id="searchresults">
            Add Case
          </h3>
          <p className="mb3">
            Click the Add Case button just below the Summary panel:
          </p>
          <div className="mv3">
            <AddButton onClick={() => {}} actionName="Add" text="Case" />
          </div>
          <p className="mb3">
            This lets you create a new case from scratch that can be populated
            with new charges. You must provide the case Current Status, County,
            Balance, and Birth Year, all of which are used to provide complete
            analysis of the record.
          </p>
          <h3 className="f4 fw7 mb2" id="searchresults">
            Edit Case
          </h3>
          <p className="mb3">
            You can edit any of these fields on an existing or newly created
            case by clicking the edit button in the case's header.
          </p>
          <EditButton onClick={() => {}} actionName="Edit Case" />
          <p className="mt3">
            {" "}
            Creating or editing a case will add a badge to that case indicating
            that the case was created or edited. You can click the badge to undo
            the change.
          </p>
          <div className="flex-l mt2">
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
          <h3 className="f4 fw7 mb2" id="searchresults">
            Add Charge
          </h3>
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
          <Disclosure defaultOpen={true}>
            <DisclosurePanel>
              <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
                <div className="br3 ma2 bg-white">
                  <EditChargePanel
                    charge={createNextBlankCharge("123456", 1)}
                    isNewCharge={false}
                    whenDoneEditing={() => {}}
                    handleUndoEditClick={() => {}}
                  />
                </div>
              </div>
            </DisclosurePanel>
            <DisclosureButton>
              Close <span aria-hidden="true" className="fas fa-angle-up"></span>
            </DisclosureButton>
          </Disclosure>
        </section>
      </>
    );
  }
}
