import { useAppDispatch } from "../../../redux/hooks";
import { startLoadingSummary } from "../../../redux/summarySlice";
import { buildAndSendDownloadPdfRequest } from "../../../redux/search/actions";
import CasesSummary from "../ExpandedView/CasesSummary";
import Stats from "../ExpandedView/SummaryStats";
import Record from "../Record";
import CasesNavList from "../ExpandedView/CasesNav";
import AssumptionsNew from "../ExpandedView/AssumptionsNew";
import { IconButton } from "../../common/IconButton";
import ExpungementFormsInfo from "./ExpungementFormsInfo";
import UserDataForm from "../../FillForms/UserDataForm";
import { panelClass } from "../Layout";

export const headingLargeClass = "f3 fw8 tc pt3 mb4 ph4";
const panelHeadingClass = "f5 fw7 tc mt2 mb3 ";
const leftPanelClass = "w-70-l f6 ph4 ";
const rightPanelClass = "w-30-l ml2-l pl3 pb2 ";

export default function ExpandedView({ showColor }: { showColor: boolean }) {
  const dispatch = useAppDispatch();

  function handleDownloadSummaryClick() {
    dispatch(startLoadingSummary());
    dispatch(buildAndSendDownloadPdfRequest);
  }

  return (
    <>
      <section className="flex-l mh2">
        <div className={panelClass + leftPanelClass}>
          <h2 className={panelHeadingClass}>Summary</h2>
          <CasesSummary showColor={showColor} />
        </div>

        <div className={panelClass + rightPanelClass}>
          <h2 className={panelHeadingClass}>Counts</h2>
          <Stats showColor={showColor} />
        </div>
      </section>

      <section className="flex-l mh2 mt2">
        <div className={panelClass + leftPanelClass}>
          <h2 className={panelHeadingClass}>Review Case Details</h2>
          <Record />
        </div>

        <div className={panelClass + rightPanelClass + "self-start sticky-l"}>
          <h2 className={panelHeadingClass}>Navigate</h2>
          <CasesNavList />
        </div>
      </section>

      <section className="flex-l mh2 mv2">
        <div className={panelClass + leftPanelClass + "pb2"}>
          <h2 className={headingLargeClass}>Assumptions</h2>
          <AssumptionsNew className="f5 lh-copy mw6-ns mw5 pl4-ns center list" />
        </div>

        <div className={panelClass + rightPanelClass + "tc"}>
          <h2 className={headingLargeClass}>Expungement Analysis Report</h2>
          <IconButton
            buttonClassName="bg-blue white hover-bg-dark-blue bg-animate mt4 pv3 ph4"
            iconClassName="fa-download pr2"
            displayText="Download Now"
            onClick={handleDownloadSummaryClick}
          />
        </div>
      </section>

      <section className="flex-l mh2 mv2">
        <div className={panelClass + leftPanelClass}>
          <h2 className={headingLargeClass}>Expungement Forms</h2>
          <ExpungementFormsInfo className="f5 lh-copy mw6-ns mw5 pl4-ns center list" />
        </div>

        <div className={panelClass + rightPanelClass + "tc"}>
          <h2 className={headingLargeClass}>Client Information</h2>
          <UserDataForm />
        </div>
      </section>
    </>
  );
}
