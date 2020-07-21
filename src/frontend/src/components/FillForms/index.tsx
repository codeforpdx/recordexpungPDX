import React from "react";
import history from "../../service/history";
import { downloadExpungementPacket } from "../../redux/search/actions";
import UserDataForm from "./UserDataForm";
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { AliasData } from "../RecordSearch/SearchPanel/types";

interface Props {}

interface State {}

export default class FillForms extends React.Component<Props, State> {
  public render() {
    return (
      <main className="flex-l f6 f5-l">
        <div className="w-50-l pt5 pb5 pb7-l pr3-l">
          <div className="mw6 center mr0-l ml-auto-l">
            <section className=" lh-copy mh2 ph5-l">
              {/*      <main className="center flex-l f6 f5-l pl4">
          <div className=" center w-50-l pt5 pb5 pb7-l ">
        <div className="mw6">
              <section className="lh-copy">
            */}
              <h1 className="f2 fw9 mb3 mt4">Generate Expungement Forms</h1>

              <p className="mb2">
                This will fill and download the required pdf paperwork forms for
                all cases that have charges eligible for expungement.
              </p>

              <p className="mb2">
                On this page, you may optionally provide the person's name,
                address, and other information and it will be used to populate
                the forms. It is not required if you would prefer to fill out
                the information later. We do not save any of the information.
              </p>

              <p className="mb2">
                The following required information is obtained from OECI and
                will be provided in the form:
              </p>
              <ol className="mb2 pl3">
                <li>Case number</li>
                <li>Names of charges</li>
                <li>Dates of arrest</li>
                <li>Dates of conviction or dismissal</li>
              </ol>

              <p className="mb2">
                The following information might be missing from OECI. If it's
                available, it will be provided in the form. If it is not present
                in OECI, some of the information may or may not be required in
                the application; please consult the manual.
              </p>
              <ol className="pl3 mb2">
                <li>Arresting Agency</li>
                <li>DA Number</li>
              </ol>

              <p className="mb2">
                The form that is filled out for each case is selected based on
                the COUNTY information for that case.
              </p>

              <p className="mb2">
                Many Oregon counties require their own paperwork to file for
                expungement. Currently, RecordSponge supports automatic
                form-filling for the following counties:
              </p>
              <ol className="mb2 pl3">
                <li>Multnomah</li>
                <li>Jackson</li>
                <li>Clackamas</li>
                <li>Lane</li>
                <li>Washington</li>
                <li>Marion</li>
                <li>Linn</li>
                <li>Yamhill</li>
                <li>Benton</li>
                <li>Josephine</li>
              </ol>

              <p className="mb2">
                Some other counties also require their own paperwork forms but
                are not yet supported in our software. This Generate Paperwork
                feature will automatically fill the stock expungement forms for
                any of the counties not listed above.
              </p>

              <p className="mb2">
                Please read the complete instructions in the manual for filing
                the required forms for expungement. After downloading the pdfs,
                review their contents to verify that all the required
                information is present and correct.
              </p>
            </section>
          </div>
        </div>

        <div className="w-50-l pt4 pt5-l pb5 ph4 ph6-l">
          <div className="mw6">
            <section className="lh-copy">
              <UserDataForm />
            </section>
          </div>
        </div>
      </main>
    );
  }
}
