import { useAppDispatch } from "../../../redux/hooks";
import { startLoadingSummary } from "../../../redux/summarySlice";
import { buildAndSendDownloadPdfRequest } from "../../../redux/search/actions";
import { clearAllData } from "../../../redux/store";
import SplitSection from "./SplitSection";
import SingleSection from "./SingleSection";
import CasesSummary from "../ExpandedView/CasesSummary";
import Stats from "../ExpandedView/SummaryStats";
import Record from "../Record";
import CasesNavList from "../ExpandedView/CasesNav";
import AssumptionsNew from "../ExpandedView/AssumptionsNew";
import IconButton from "../../common/IconButton";
import ExpungementFormsInfo from "./ExpungementFormsInfo";
import UserDataForm from "../../FillForms/UserDataForm";

export const headingLargeClass = "f3 fw8 tc pt2 mb4 ph4";

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
      <SplitSection
        leftHeading="Review Summary"
        leftComponent={<CasesSummary showColor={showColor} />}
        rightHeading="Counts"
        rightComponent={<Stats showColor={showColor} />}
      />

      <SplitSection
        leftHeading="Analyze Cases"
        leftComponent={<Record />}
        rightHeading="Quick Links"
        rightComponent={<CasesNavList className="f6 overflow-y-auto vh-75" />}
        rightClassName="self-start sticky-l"
      />

      <SingleSection
        heading="Get The Expungement Analysis Report"
        className="tc"
      >
        <IconButton
          styling="button"
          buttonClassName="bg-blue white hover-bg-dark-blue"
          iconClassName="fa-download pr2"
          displayText="Download Now"
          onClick={handleDownloadSummaryClick}
        />
      </SingleSection>

      <SingleSection heading="Verify Assumptions">
        <AssumptionsNew className="f5 lh-copy mw6-ns mw5 pl4-ns center list" />
      </SingleSection>

      <SingleSection className="flex-l">
        <div className="w-60-l">
          <h2 className={headingLargeClass}>Get Expungement Forms</h2>
          <ExpungementFormsInfo className="f5 lh-copy mw6-ns mw5 pl4-ns center list" />
        </div>

        <div className="w-40-l">
          <UserDataForm />
        </div>
      </SingleSection>

      <SingleSection heading="Finish Up" className="tc pb5 mb3">
        <IconButton
          styling="button"
          buttonClassName="bg-red white hover-bg-dark-red "
          iconClassName="fa-arrow-up pr2"
          displayText="Clear Data And Start Over"
          onClick={handleStartOverClick}
        />
      </SingleSection>
    </>
  );
}
