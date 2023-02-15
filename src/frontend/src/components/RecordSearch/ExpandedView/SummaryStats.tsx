import React from "react";
import { useAppSelector } from "../../../redux/hooks";
import { selectStats } from "../../../redux/statsSlice";
import { shortLabels } from "../Record/types";
import toDollars from "../../../service/currency-format";
import { getEligibilityColor } from "../Record/util";

interface ElementProps extends React.HTMLAttributes<HTMLElement> {
  className?: string;
  text?: string;
  children?: React.ReactNode;
}

function Col({ className = "", children }: ElementProps) {
  return <div className={`pb2 ${className}`}>{children}</div>;
}

function Row({ className = "", children }: ElementProps) {
  return <div className={`flex flex-wrap mb1 ${className}`}>{children}</div>;
}

interface Props {
  showColor: boolean;
}

export default function SummaryStats({ showColor, ...props }: Props) {
  const stats = useAppSelector(selectStats);
  const smallColClass = "w-20 pl2";
  const {
    totalCases,
    totalCharges,
    numExcludedCharges,
    numIncludedCharges,
    totalFines,
    numChargesByEligibilityStatus,
    finesByCounty,
  } = stats;

  if (!stats || totalCases === 0) return <></>;

  return (
    <div {...props}>
      <Row>
        <Col className="w-40"></Col>
        <Col className={smallColClass}>Total</Col>
        <Col className={smallColClass}>Includ.</Col>
        <Col className={smallColClass}>Exclud.</Col>
      </Row>
      <Row>
        <Col className="w-40 f5 fw7">Cases</Col>
        <Col className={smallColClass}>{totalCases}</Col>
        <Col></Col>
        <Col></Col>
      </Row>

      <Row className="mt4">
        <Col className="w-40 f5 fw7 mb2">Charges</Col>
        <Col className={smallColClass}>{totalCharges}</Col>
        <Col className={smallColClass}>
          {numIncludedCharges > 0 ? numIncludedCharges : ""}
        </Col>
        <Col className={smallColClass}>
          {numExcludedCharges > 0 ? numExcludedCharges : ""}
        </Col>
      </Row>

      {shortLabels.map((label) => {
        const statusStats = numChargesByEligibilityStatus[label];
        const { color, bgColor } = getEligibilityColor(label, 0);

        if (!statusStats || statusStats.total === 0)
          return <React.Fragment key={label}></React.Fragment>;

        const { total, numIncluded, numExcluded } = statusStats;
        return (
          <Row key={label}>
            <Col
              className={`w-40 fw6 f6 br3 tc pv1 ${showColor ? color : ""} ${
                showColor ? bgColor : ""
              }`}
            >
              {label}
            </Col>
            <Col className={smallColClass}>{total}</Col>
            <Col className={smallColClass}>
              {numIncluded > 0 ? numIncluded : ""}
            </Col>
            <Col className={smallColClass}>
              {numExcluded > 0 ? numExcluded : ""}
            </Col>
          </Row>
        );
      })}

      <div className="f5 fw7 mt4 mb3">Fines Due</div>
      {Object.entries(finesByCounty)
        .sort(([, fines]) => fines)
        .map(([county, fines]) => {
          if (fines === 0)
            return <React.Fragment key={county}></React.Fragment>;
          return (
            <Row key={county}>
              <Col className="w-40">{county}</Col>
              <Col className={smallColClass}>{toDollars(fines)}</Col>
            </Row>
          );
        })}

      <Row>
        <Col className="w-40">Total</Col>
        <Col className={smallColClass}>{toDollars(totalFines)}</Col>
      </Row>
    </div>
  );
}
