import { useState } from "react";
import { useAppDispatch, useAppSelector } from "../../../redux/hooks";
import {
  startLoadingSummary,
  selectSummaryIsLoading,
} from "../../../redux/summarySlice";
import { buildAndSendDownloadPdfRequest } from "../../../redux/search/actions";
import { clearAllData } from "../../../redux/store";
import { CaseData } from "../Record/types";
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
import HideTrafficChargesCheckbox from "./HideTrafficChargesCheckbox";

type CaseFilterType = "skipExcludedCharges" | "none";

interface Props {
  showColor: boolean;
}

export const headingLargeClass = "f3 fw8 tc pt2 mb4 ph4";

export default function ExpandedView({ showColor }: Props) {
  const dispatch = useAppDispatch();
  const record = useAppSelector((state) => state.search.record);
  const summaryIsLoading = useAppSelector(selectSummaryIsLoading);
  const [summaryFilterType, setSummaryFilterType] = useState<CaseFilterType>(
    "skipExcludedCharges"
  );
  const [navFilterType, setNavFilterType] = useState<CaseFilterType>(
    "skipExcludedCharges"
  );

  if (!record?.cases) return <></>;

  const cases = record.cases;

  const handleDownloadSummaryClick = () => {
    dispatch(startLoadingSummary());
    dispatch(buildAndSendDownloadPdfRequest);
  };

  const handleStartOverClick = () => {
    dispatch(clearAllData());
    window.scrollTo(0, 0);
  };

  const handleShowAllChargesToggle = (
    type: CaseFilterType,
    setter: (value: React.SetStateAction<CaseFilterType>) => void
  ) => {
    return () => {
      if (type === "skipExcludedCharges") {
        setter("none");
      } else {
        setter("skipExcludedCharges");
      }
    };
  };

  const skipExcludedCharges = (cases: CaseData[], aCase: CaseData) => {
    const includedCharges = aCase.charges.filter(
      (charge) => !charge.isExcluded
    );
    cases.push({ ...aCase, charges: includedCharges });
    return cases;
  };

  const filters = {
    skipExcludedCharges,
    none: (cases: CaseData[], aCase: CaseData) => cases.concat(aCase),
  };

  const summaryCases = cases.reduce(
    filters[summaryFilterType],
    [] as CaseData[]
  );

  const navCases = cases.reduce(filters[navFilterType], [] as CaseData[]);

  // In the future, the summary section may have more filter types which
  // the nav section may not have. For now, the nav checkbox also uses
  // this variable to determine whether it's displayed or not.
  const summaryHasFilteredCases = cases.some((aCase) =>
    aCase.charges.some((charge) => charge.isExcluded)
  );

  return (
    <>
      <SplitSection
        leftHeading="Review Summary"
        leftComponent={
          <div>
            {summaryHasFilteredCases && (
              <HideTrafficChargesCheckbox
                id="1"
                labelText="Hide Traffic Charges"
                className="checkbox checkbox-sm fw4 f6 tr mb2"
                checked={summaryFilterType === "skipExcludedCharges"}
                onChange={handleShowAllChargesToggle(
                  summaryFilterType,
                  setSummaryFilterType
                )}
              />
            )}
            <CasesSummary showColor={showColor} cases={summaryCases} />
          </div>
        }
        rightHeading="Counts"
        rightComponent={<Stats showColor={showColor} />}
      />

      <SplitSection
        leftHeading="Analyze Cases"
        leftComponent={<Record />}
        rightHeading="Quick Links"
        rightComponent={
          <div>
            {summaryHasFilteredCases && (
              <HideTrafficChargesCheckbox
                id="2"
                labelText="Hide Traffic Charges"
                className="checkbox checkbox-sm fw4 f6 mb2 pl2"
                checked={navFilterType === "skipExcludedCharges"}
                onChange={handleShowAllChargesToggle(
                  navFilterType,
                  setNavFilterType
                )}
              />
            )}

            <CasesNavList
              className="f6 overflow-y-auto vh-75"
              cases={navCases}
            />
          </div>
        }
        rightClassName="self-start sticky-l"
      />

      <SingleSection
        heading="Get The Expungement Analysis Report"
        className="tc"
      >
        <IconButton
          styling="button"
          buttonClassName={
            "bg-blue white hover-bg-dark-blue" +
            (summaryIsLoading ? " loading-btn" : "")
          }
          iconClassName="fa-download pr2"
          displayText="Download Summary Now"
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
