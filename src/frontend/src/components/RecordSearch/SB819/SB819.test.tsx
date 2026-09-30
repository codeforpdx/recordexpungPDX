import React from "react";
import "@testing-library/jest-dom";
import { act, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { setupStore, clearAllData } from "../../../redux/store";
import { default as initialSearchState } from "../../../redux/search/initialState";
import { appRender } from "../../../test/testHelpers";
import Layout from "../Layout";
import { buildAnalysis, buildRecord, DemoOptions } from "./sb819TestData";

jest.mock("axios", () => ({ request: () => new Promise(() => {}) }));

jest.mock("react-router-dom", () => ({
  ...(jest.requireActual("react-router-dom") as any),
  useNavigate: () => jest.fn(),
}));

type User = ReturnType<typeof userEvent.setup>;

function renderLayout(options: DemoOptions = {}) {
  const store = setupStore({
    search: {
      ...initialSearchState,
      record: buildRecord(buildAnalysis(options)),
    },
  });
  return {
    user: userEvent.setup(),
    ...appRender(<Layout />, undefined, { store }),
  };
}

async function openTheAnalysis(user: User) {
  await user.click(
    screen.getByRole("button", { name: /SB-819 eligibility analysis/i })
  );
}

/** The record rendered with the SB-819 view open. */
async function renderView(options: DemoOptions = {}) {
  const rendered = renderLayout(options);
  await openTheAnalysis(rendered.user);
  return rendered;
}

const control = (target: string, value: "yes" | "no") =>
  document.getElementById(`${target}-${value}`);

function answer(user: User, target: string, value: "yes" | "no") {
  const input = control(target, value);
  if (!input) throw new Error(`no ${value} control for ${target}`);
  return user.click(input);
}

const panel = (id: string) => document.getElementById(id);

const criteriaShown = () =>
  screen.queryByText("SB-819 Limiting Criteria") !== null;

/** The applicant's gate answered No: Excessive Sentencing is out, and the record opens. */
const notIncarcerated = (user: User) =>
  answer(user, "record:currently-incarcerated", "no");

describe("the feature flag", () => {
  const realLocation = window.location;

  function serveFrom(hostname: string) {
    Object.defineProperty(window, "location", {
      value: { ...realLocation, hostname },
      writable: true,
      configurable: true,
    });
  }

  afterEach(() => {
    Object.defineProperty(window, "location", {
      value: realLocation,
      writable: true,
      configurable: true,
    });
  });

  it("hides the badge on recordsponge.com", () => {
    serveFrom("recordsponge.com");
    renderLayout();
    expect(screen.queryByText(/SB-819 eligib/)).not.toBeInTheDocument();
  });

  it("shows the badge on the staging host and locally", () => {
    serveFrom("dev.recordsponge.com");
    renderLayout();
    expect(screen.getByText("Check SB-819 eligibility")).toBeInTheDocument();
  });
});

describe("the badge in the search summary", () => {
  it("invites a check while any conviction is still possible", () => {
    renderLayout();
    expect(screen.getByText("Check SB-819 eligibility")).toBeInTheDocument();
  });

  it("reads negatively when every analyzed charge is ineligible", () => {
    renderLayout({ ruledOutOnly: true });
    expect(screen.getByText("No charges SB-819 eligible")).toBeInTheDocument();
  });

  it("opens the analysis either way", async () => {
    const { user } = renderLayout({ ruledOutOnly: true });
    await openTheAnalysis(user);
    expect(
      screen.getByRole("heading", { name: /SB-819 Eligibility Analysis/i })
    ).toBeInTheDocument();
  });

  it("is absent when no charge is in scope", () => {
    renderLayout({ empty: true });
    expect(screen.queryByText(/SB-819 eligib/)).not.toBeInTheDocument();
  });
});

describe("scrolling on a view swap", () => {
  // jsdom has no scrollIntoView, so the panels report where they were asked to scroll to.
  let scrolledTo: string[];

  beforeEach(() => {
    scrolledTo = [];
    (Element.prototype as any).scrollIntoView = function () {
      scrolledTo.push((this as HTMLElement).id);
    };
    jest.spyOn(window, "scrollTo").mockImplementation(() => {});
  });

  afterEach(() => {
    delete (Element.prototype as any).scrollIntoView;
    jest.restoreAllMocks();
  });

  async function nextFrame() {
    await act(async () => {
      await new Promise((resolve) =>
        requestAnimationFrame(() => resolve(null))
      );
    });
  }

  it("brings the SB-819 panel to the top, not the page", async () => {
    await renderView();
    await nextFrame();
    expect(scrolledTo).toEqual(["sb819-summary-panel"]);
    expect(window.scrollTo).not.toHaveBeenCalled();
  });

  it("brings the search summary panel back to the top on return", async () => {
    const { user } = await renderView();
    await nextFrame();
    scrolledTo = [];
    await user.click(
      screen.getByRole("button", { name: /back to search summary/i })
    );
    await nextFrame();
    expect(scrolledTo).toEqual(["record-summary-panel"]);
  });

  it("clears the fixed header on both panels", async () => {
    const { user } = renderLayout();
    expect(document.getElementById("record-summary-panel")).toHaveClass(
      "scroll-mt-20"
    );
    await openTheAnalysis(user);
    expect(document.getElementById("sb819-summary-panel")).toHaveClass(
      "scroll-mt-20"
    );
  });
});

describe("the view itself", () => {
  it("replaces the search summary and can be dismissed", async () => {
    const { user } = await renderView();
    expect(
      screen.queryByRole("heading", { name: "Search Summary" })
    ).not.toBeInTheDocument();
    await user.click(
      screen.getByRole("button", { name: /back to search summary/i })
    );
    expect(
      screen.getByRole("heading", { name: "Search Summary" })
    ).toBeInTheDocument();
  });

  it("returns to the summary when the record stops having anything to analyze", async () => {
    // An edit can remove the last analyzed charge from a record the view was opened on.
    const { store } = await renderView();
    const record = store.getState().search.record!;
    act(() => {
      store.dispatch({
        type: "DISPLAY_RECORD",
        record: {
          ...record,
          summary: {
            ...record.summary,
            sb819_analysis: buildAnalysis({ empty: true }),
          },
        },
        questions: {},
      });
    });
    expect(
      screen.getByRole("heading", { name: "Search Summary" })
    ).toBeInTheDocument();
  });

  it("discards answers and leaves the view when a new search starts", async () => {
    // The targets carry no name, so one client's answers would otherwise be applied to the
    // next client's record.
    const { user, store } = await renderView();
    await answer(user, "record:currently-incarcerated", "yes");
    expect(store.getState().sb819.isViewing).toBe(true);
    act(() => {
      store.dispatch({ type: "RECORD_LOADING" });
    });
    expect(store.getState().sb819Answers.answers).toEqual({});
    expect(store.getState().sb819.isViewing).toBe(false);
  });

  it("discards answers on Start Over", async () => {
    const { user, store } = await renderView();
    await notIncarcerated(user);
    expect(Object.keys(store.getState().sb819Answers.answers)).toHaveLength(1);
    act(() => {
      store.dispatch(clearAllData());
    });
    expect(store.getState().sb819Answers.answers).toEqual({});
  });
});

describe("stage 0: the applicant", () => {
  it("shows the header and the applicant's gate, and nothing else", async () => {
    await renderView();
    expect(
      screen.getByRole("heading", { name: "SB-819 Eligibility Analysis" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "Full rules" })
    ).toBeInTheDocument();
    expect(screen.getByText("About the applicant")).toBeInTheDocument();
    expect(screen.getByText("0 of 1 answered")).toBeInTheDocument();
    expect(control("record:currently-incarcerated", "yes")).toBeInTheDocument();
    expect(control("record:juvenile-transfer", "yes")).toBeNull();
    expect(screen.queryByText("Needs More Analysis")).toBeNull();
    expect(panel("100")).toBeNull();
  });

  it("opens the record once the gate is answered No", async () => {
    const { user } = await renderView();
    await notIncarcerated(user);
    expect(screen.getByText("1 of 1 answered")).toBeInTheDocument();
    expect(screen.getByText("Needs More Analysis")).toBeInTheDocument();
    expect(panel("100")).toBeInTheDocument();
  });

  it("asks the alternatives the record leaves open when the gate is answered Yes, and waits for them", async () => {
    const { user } = await renderView({ theft: true });
    await answer(user, "record:currently-incarcerated", "yes");
    for (const key of [
      "juvenile-transfer",
      "over-60-or-ill",
      "non-person-over-10-years",
      "person-over-16-years",
    ]) {
      expect(control(`record:${key}`, "yes")).toBeInTheDocument();
    }
    expect(screen.getByText("1 of 5 answered")).toBeInTheDocument();
    expect(panel("100")).toBeNull();

    await answer(user, "record:juvenile-transfer", "yes");
    // One met alternative satisfies the group, so the others stand down and the record opens.
    expect(control("record:over-60-or-ill", "yes")).toBeNull();
    expect(screen.getByText("2 of 2 answered")).toBeInTheDocument();
    expect(panel("100")).toBeInTheDocument();
  });

  it("brings a question back when the answer that stood it down is cleared", async () => {
    const { user } = await renderView();
    await answer(user, "record:currently-incarcerated", "yes");
    await answer(user, "record:over-60-or-ill", "yes");
    expect(control("record:juvenile-transfer", "yes")).toBeNull();

    const fieldset = control("record:over-60-or-ill", "yes")!.closest(
      "fieldset"
    )!;
    await user.click(within(fieldset).getByRole("button", { name: "Clear" }));
    expect(control("record:juvenile-transfer", "yes")).toBeInTheDocument();
    expect(panel("100")).toBeNull();
  });

  it("keeps an answered question on screen after the gate turns against it", async () => {
    const { user } = await renderView();
    await answer(user, "record:currently-incarcerated", "yes");
    await answer(user, "record:over-60-or-ill", "yes");
    await answer(user, "record:currently-incarcerated", "no");
    expect(control("record:over-60-or-ill", "yes")).toBeChecked();
    expect(control("record:juvenile-transfer", "yes")).toBeNull();
  });

  it("can be folded and unfolded", async () => {
    const { user } = await renderView();
    const header = screen.getByRole("button", { name: /About the applicant/ });
    expect(header).toHaveAttribute("aria-expanded", "true");
    await user.click(header);
    expect(header).toHaveAttribute("aria-expanded", "false");
  });
});

describe("stage 1: the summary and the cases", () => {
  it("lists every conviction under its status, linked to its case", async () => {
    const { user } = await renderView({ duii: true });
    await notIncarcerated(user);
    expect(screen.getByText("None")).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "100: Robbery in the Second Degree" })
    ).toHaveAttribute("href", "#100");
    expect(
      screen.getByRole("link", {
        name: "300: Driving Under the Influence of Intoxicants",
      })
    ).toHaveAttribute("href", "#300");
    expect(panel("100")).toHaveClass("scroll-mt-20");
    // A Clackamas charge is out of scope and absent from the view entirely.
    expect(screen.queryByText(/Assault in the First Degree/)).toBeNull();
  });

  it("asks the case's question and lists its convictions by name alone until it is answered", async () => {
    const { user } = await renderView({ theft: true });
    await notIncarcerated(user);
    expect(control("case:100:sentence-completed", "yes")).toBeInTheDocument();
    for (const id of ["100-1", "100-2"]) {
      expect(panel(id)).toHaveTextContent(/Charge/);
      expect(panel(id)).not.toHaveTextContent(/Severity/);
    }
    await answer(user, "case:100:sentence-completed", "yes");
    expect(panel("100-1")).toHaveTextContent(/Severity/);
    expect(panel("100-2")).toHaveTextContent(/Severity/);
  });

  it("applies a case answer to that case only", async () => {
    const { user } = await renderView({ theft: true, arson: true });
    await notIncarcerated(user);
    await answer(user, "case:100:sentence-completed", "yes");
    expect(
      control("charge:100-1:no-domestic-violence", "yes")
    ).toBeInTheDocument();
    expect(
      control("charge:100-2:no-domestic-violence", "yes")
    ).toBeInTheDocument();
    expect(control("charge:900-1:no-domestic-violence", "yes")).toBeNull();
    expect(panel("900-1")).not.toHaveTextContent(/Severity/);
  });

  it("asks the plea question on the case only once the applicant's gate is met", async () => {
    const { user } = await renderView();
    await answer(user, "record:currently-incarcerated", "yes");
    await answer(user, "record:juvenile-transfer", "yes");
    expect(control("case:100:not-global-plea", "yes")).toBeInTheDocument();
  });
});

describe("stages 2 and 3: a charge", () => {
  it("asks the charge's questions, then shows the criteria once they are answered", async () => {
    const { user } = await renderView();
    await notIncarcerated(user);
    await answer(user, "case:100:sentence-completed", "yes");
    expect(control("charge:100-1:innocence-claim", "yes")).toBeInTheDocument();
    expect(
      control("charge:100-1:no-domestic-violence", "yes")
    ).toBeInTheDocument();
    expect(control("charge:100-1:five-years-served", "yes")).toBeNull();
    expect(criteriaShown()).toBe(false);

    await answer(user, "charge:100-1:innocence-claim", "no");
    expect(criteriaShown()).toBe(false);
    await answer(user, "charge:100-1:no-domestic-violence", "no");
    expect(criteriaShown()).toBe(true);
  });

  it("asks a question as the question alone", async () => {
    const { user } = await renderView();
    await notIncarcerated(user);
    await answer(user, "case:100:sentence-completed", "yes");
    expect(
      screen.getByText("Did this conviction involve domestic violence?")
    ).toBeInTheDocument();
    expect(screen.queryByText("If yes:")).toBeNull();
    expect(screen.queryByText("About this case")).toBeNull();
  });

  it("carries the answers into the criteria and the summary", async () => {
    const { user } = await renderView();
    await notIncarcerated(user);
    await answer(user, "case:100:sentence-completed", "yes");
    await answer(user, "charge:100-1:innocence-claim", "yes");
    await answer(user, "charge:100-1:no-domestic-violence", "no");

    const main = screen.getByRole("button", { name: /^Main Criteria/ });
    expect(main).toHaveTextContent("all four met");
    expect(main).toHaveAttribute("aria-expanded", "false");

    const innocence = screen.getByRole("button", { name: /^Actual Innocence/ });
    expect(innocence).toHaveTextContent("Possibly SB-819 Eligible");
    expect(innocence).toHaveAttribute("aria-expanded", "false");

    const excessive = screen.getByRole("button", {
      name: /^Excessive Sentencing/,
    });
    expect(excessive).toHaveTextContent("SB-819 Ineligible");
    expect(excessive).toHaveAttribute("aria-expanded", "false");
    expect(excessive.parentElement).toHaveTextContent(
      /Is the applicant currently incarcerated\?\s*No/
    );

    const collateral = screen.getByRole("button", {
      name: /^Collateral Consequences/,
    });
    expect(collateral).toHaveTextContent("Possibly SB-819 Eligible");
    expect(collateral).toHaveAttribute("aria-expanded", "true");

    expect(
      screen.getByText("Possibly SB-819 Eligible", { selector: "span.fw7" })
        .parentElement
    ).toHaveTextContent("(1)");
  });

  it("keeps every row to the outcome, the name, and how it is settled", async () => {
    const { user } = await renderView();
    await notIncarcerated(user);
    await answer(user, "case:100:sentence-completed", "yes");
    await answer(user, "charge:100-1:innocence-claim", "yes");
    await answer(user, "charge:100-1:no-domestic-violence", "no");

    const row = screen
      .getByText("Conviction did not involve domestic violence")
      .closest("li")!;
    expect(row).toHaveTextContent(
      /^Conviction did not involve domestic violenceQuestion$/
    );
    expect(row.querySelector("input")).toBeNull();
    // Questions about the applicant are answered once at the top, not repeated per charge.
    expect(
      screen.queryByText("Applicant is currently incarcerated")
    ).toBeNull();
    // A question that stood down is not a row either.
    expect(
      screen.queryByText(
        "Applicant has served at least 5 years of the term of incarceration"
      )
    ).toBeNull();
    // Criteria nobody can settle are not rows.
    expect(
      screen.queryByText(
        "Applicant demonstrates manifest and particularized hardship"
      )
    ).toBeNull();
    // Page cites stay on the rules page.
    expect(screen.queryByText("Page 3")).toBeNull();
  });

  it("withdraws the criteria while a newly unlocked question is open, and reopens a ruled-out pathway to read it", async () => {
    const { user } = await renderView();
    await notIncarcerated(user);
    await answer(user, "case:100:sentence-completed", "yes");
    await answer(user, "charge:100-1:innocence-claim", "yes");
    await answer(user, "charge:100-1:no-domestic-violence", "no");
    expect(criteriaShown()).toBe(true);

    await answer(user, "record:currently-incarcerated", "yes");
    expect(panel("100")).toBeNull();
    await answer(user, "record:juvenile-transfer", "yes");
    // The plea question is now live on the case, which holds its charge by name again.
    expect(control("case:100:not-global-plea", "yes")).toBeInTheDocument();
    expect(panel("100-1")).not.toHaveTextContent(/Severity/);

    await answer(user, "case:100:not-global-plea", "no");
    expect(
      control("charge:100-1:five-years-served", "yes")
    ).toBeInTheDocument();
    expect(criteriaShown()).toBe(false);
    await answer(user, "charge:100-1:five-years-served", "no");
    expect(criteriaShown()).toBe(true);
    const excessive = screen.getByRole("button", {
      name: /^Excessive Sentencing/,
    });
    expect(excessive.parentElement).toHaveTextContent(
      /five years of the term of incarceration on this sentence\?\s*No/
    );
    await user.click(excessive);
    expect(excessive).toHaveAttribute("aria-expanded", "true");
    expect(
      screen.getByText(
        "Applicant has served at least 5 years of the term of incarceration"
      )
    ).toBeInTheDocument();
  });

  it("shows a conviction the record rules out in full at once, with the failing criterion", async () => {
    const { user } = await renderView({ duii: true });
    await notIncarcerated(user);
    const duii = panel("300-1")!;
    expect(duii).toHaveTextContent(/Severity/);
    expect(duii.querySelector("input")).toBeNull();
    expect(duii).toHaveTextContent(/gates every application type/);
    const main = within(duii).getByRole("button", { name: /^Main Criteria/ });
    expect(main).toHaveTextContent("SB-819 Ineligible");
    expect(main).toHaveAttribute("aria-expanded", "true");
    expect(
      within(duii)
        .getByText("Conviction was sentenced as a felony")
        .closest("li")!
        .querySelector(".fa-times-circle")
    ).not.toBeNull();
  });

  it("asks the felony question first and holds the rest behind it", async () => {
    const { user } = await renderView({ assault: true });
    await notIncarcerated(user);
    // The case's own question waits on the felony question too, so the charge is shown.
    expect(control("case:800:sentence-completed", "yes")).toBeNull();
    expect(
      control("charge:800-1:sentenced-as-felony", "yes")
    ).toBeInTheDocument();
    expect(control("charge:800-1:innocence-claim", "yes")).toBeNull();

    await answer(user, "charge:800-1:sentenced-as-felony", "no");
    expect(control("charge:800-1:innocence-claim", "yes")).toBeNull();
    expect(control("charge:800-1:sentenced-as-felony", "no")).toBeChecked();
    const assault = panel("800-1")!;
    expect(
      within(assault).getByRole("button", { name: /^Main Criteria/ })
    ).toHaveTextContent("SB-819 Ineligible");
    expect(assault).toHaveTextContent(/gates every application type/);

    await answer(user, "charge:800-1:sentenced-as-felony", "yes");
    // The case question comes next and holds the charge by name until it is answered.
    expect(control("case:800:sentence-completed", "yes")).toBeInTheDocument();
    expect(control("charge:800-1:innocence-claim", "yes")).toBeNull();
    await answer(user, "case:800:sentence-completed", "yes");
    expect(control("charge:800-1:innocence-claim", "yes")).toBeInTheDocument();
  });

  it("says which pathways the record blocks and which stay open", async () => {
    const { user } = await renderView({ rape: true });
    await notIncarcerated(user);
    // Collateral Consequences is out from the record, so the case has nothing to ask.
    expect(control("case:500:sentence-completed", "yes")).toBeNull();
    expect(panel("500-1")).toHaveTextContent(/Severity/);
    await answer(user, "charge:500-1:innocence-claim", "yes");
    expect(panel("500-1")).toHaveTextContent(
      "Blocked under Excessive Sentencing, Collateral Consequences, but still open under Actual Innocence."
    );
    const collateral = within(panel("500-1")!).getByRole("button", {
      name: /^Collateral Consequences/,
    });
    expect(collateral.parentElement).toHaveTextContent(
      "Conviction is not a registerable sex offense: explanation"
    );
  });
});
