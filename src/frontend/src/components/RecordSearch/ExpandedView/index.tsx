import { useAppDispatch } from "../../../redux/hooks";
import { startLoadingSummary } from "../../../redux/summarySlice";
import { buildAndSendDownloadPdfRequest } from "../../../redux/search/actions";
import { clearAllData } from "../../../redux/store";
import CasesSummary from "../ExpandedView/CasesSummary";
import Stats from "../ExpandedView/SummaryStats";
import Record from "../Record";
import CasesNavList from "../ExpandedView/CasesNav";
import AssumptionsNew from "../ExpandedView/AssumptionsNew";
import { IconButton } from "../../common/IconButton";
import ExpungementFormsInfo from "./ExpungementFormsInfo";
import UserDataForm from "../../FillForms/UserDataForm";
import { panelClass, mainWrapper, singlePanelClass } from "../Layout";

export const headingLargeClass = "f3 fw8 tc pt2 mb4 ph4";
const wrapperClass = "flex-l mh2 mt3";
const panelHeadingClass = "f5 fw7 tc pv3 ";
const leftPanelClass = "w-70-l f6 ph4 mr3";
const rightPanelClass = "w-30-l pl3 pb2 ";

export default function ExpandedView({ showColor }: { showColor: boolean }) {
  const dispatch = useAppDispatch();

  function handleDownloadSummaryClick() {
    dispatch(startLoadingSummary());
    dispatch(buildAndSendDownloadPdfRequest);
  }

  function handleStartOverClick() {
    dispatch(clearAllData());
    window.scroll(0, 0);
  }

  return (
    <>
      <section className={wrapperClass}>
        <div className={panelClass + leftPanelClass}>
          <h2 className={panelHeadingClass}>Review Summary</h2>
          <CasesSummary showColor={showColor} />
        </div>

        <div className={panelClass + rightPanelClass}>
          <h3 className={panelHeadingClass}>Counts</h3>
          <Stats showColor={showColor} />
        </div>
      </section>

      <section className={wrapperClass}>
        <div className={panelClass + leftPanelClass}>
          <h2 className={panelHeadingClass}>Analyze Cases</h2>
          <Record />
        </div>

        <div className={panelClass + rightPanelClass + "self-start sticky-l"}>
          <h3 className={panelHeadingClass}>Quick Links</h3>
          <CasesNavList className="f6 overflow-y-auto vh-75" />
        </div>
      </section>

      <section className={mainWrapper + panelClass + singlePanelClass + "tc"}>
        <h2 className={headingLargeClass}>
          Get The Expungement Analysis Report
        </h2>
        <IconButton
          type="button"
          buttonClassName="bg-blue white hover-bg-dark-blue"
          iconClassName="fa-download pr2"
          displayText="Download Now"
          onClick={handleDownloadSummaryClick}
        />
      </section>

      <section className={mainWrapper + panelClass + singlePanelClass}>
        <h2 className={headingLargeClass}>Verify Assumptions</h2>
        <AssumptionsNew className="f5 lh-copy mw6-ns mw5 pl4-ns center list" />
      </section>

      <section
        className={mainWrapper + panelClass + singlePanelClass + "flex-l"}
      >
        <div className="w-60-l">
          <h2 className={headingLargeClass}>Expungement Forms</h2>
          <ExpungementFormsInfo className="f5 lh-copy mw6-ns mw5 pl4-ns center list" />
        </div>

        <div className="w-40-l">
          <UserDataForm />
        </div>
      </section>

      <section
        className={mainWrapper + panelClass + singlePanelClass + "tc pb5 mb3"}
      >
        <h2 className={headingLargeClass}>Finish Up</h2>
        <IconButton
          type="button"
          buttonClassName="bg-red white hover-bg-dark-red "
          iconClassName="fa-arrow-up pr2"
          displayText="Clear Data And Start Over"
          onClick={handleStartOverClick}
        />
      </section>
    </>
  );
}
