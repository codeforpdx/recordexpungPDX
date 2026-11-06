import React from "react";
import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { appRender, clickButton } from "../../../test/testHelpers";
import Case from "./Case";
import { CaseData, SetAsideMotionData } from "./types";
import { describeMotion, motionEditFrom, shortToMMDDYYYY } from "./util";

const FILED: SetAsideMotionData = {
  status: "Filed",
  filed_date: "Feb 18, 2026",
  resolved_date: null,
};
const DENIED: SetAsideMotionData = {
  status: "Denied",
  filed_date: "Feb 18, 2026",
  resolved_date: "Aug 24, 2026",
};

function aCase(set_aside_motion: SetAsideMotionData | null): CaseData {
  return {
    balance_due: 0,
    birth_year: 1990,
    case_detail_link:
      "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=1",
    case_number: "21CR00001",
    charges: [],
    citation_number: "",
    current_status: "Closed",
    district_attorney_number: "",
    edit_status: "UNCHANGED",
    date: "Jan 1, 2010",
    location: "Multnomah",
    name: "Doe, John",
    violation_type: "Offense Misdemeanor",
    restitution: false,
    set_aside_motion,
  };
}

function renderCase(motion: SetAsideMotionData | null, editing = false) {
  return appRender(
    <Case
      case={aCase(motion)}
      showEditButtons={editing}
      editing={false}
      isNewCase={false}
      whenEditing={() => {}}
      whenDoneEditing={() => {}}
    />
  );
}

describe("the motion sentence", () => {
  it("reads open, denied, or withdrawn with the dates it has", () => {
    expect(describeMotion(FILED)).toBe(
      "A motion to set aside this case was filed on Feb 18, 2026."
    );
    expect(describeMotion(DENIED)).toBe(
      "A motion to set aside this case was filed on Feb 18, 2026 and denied on Aug 24, 2026."
    );
    expect(
      describeMotion({ ...DENIED, status: "Withdrawn", resolved_date: null })
    ).toBe(
      "A motion to set aside this case was filed on Feb 18, 2026 and withdrawn."
    );
  });

  it("is shown on the case, and absent when there is no motion", () => {
    renderCase(DENIED);
    expect(screen.getByText(describeMotion(DENIED))).toBeInTheDocument();
    renderCase(null);
    expect(screen.queryByText(/motion to set aside/i)).toHaveTextContent(
      describeMotion(DENIED)
    );
  });
});

describe("the editor's form of the motion", () => {
  it("rewrites the API's dates for the date fields", () => {
    expect(shortToMMDDYYYY("Feb 18, 2026")).toBe("2/18/2026");
    expect(shortToMMDDYYYY(null)).toBe("");
    expect(motionEditFrom(DENIED)).toEqual({
      status: "Denied",
      filed_date: "2/18/2026",
      resolved_date: "8/24/2026",
    });
    expect(motionEditFrom(null)).toEqual({
      status: "None",
      filed_date: "",
      resolved_date: "",
    });
  });

  it("opens on the scraped state and shows the date fields the state needs", async () => {
    const user = userEvent.setup();
    renderCase(DENIED, true);
    await clickButton(user, "edit case");
    expect(screen.getByLabelText("Denied")).toBeChecked();
    expect(screen.getByLabelText(/motion filed/i)).toHaveValue("2/18/2026");
    expect(screen.getByLabelText(/motion denied/i)).toHaveValue("8/24/2026");

    await user.click(screen.getByLabelText("Filed"));
    expect(screen.queryByLabelText(/motion denied/i)).not.toBeInTheDocument();
    expect(screen.getByLabelText(/motion filed/i)).toHaveValue("2/18/2026");

    await user.click(screen.getByLabelText("None"));
    expect(screen.queryByLabelText(/motion filed/i)).not.toBeInTheDocument();
  });

  it("requires a filed date for a motion, and a resolved date for a denial", async () => {
    const user = userEvent.setup();
    renderCase(null, true);
    await clickButton(user, "edit case");
    await user.click(screen.getByLabelText("Denied"));
    await clickButton(user, "update case");
    expect(
      screen.getByText("Motion Filed date is required")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Motion Denied or Withdrawn date is required")
    ).toBeInTheDocument();

    await user.type(screen.getByLabelText(/motion filed/i), "2/18/2026");
    await user.type(screen.getByLabelText(/motion denied/i), "not a date");
    await clickButton(user, "update case");
    expect(
      screen.getByText("Motion Denied or Withdrawn date format is invalid")
    ).toBeInTheDocument();
  });
});
