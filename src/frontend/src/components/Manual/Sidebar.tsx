import { openDetailsById } from "../common/Accordion";

const sectionLinks = [
  { title: "General Info", href: "#general-info", subSection: false },
  { title: "Part 1: OECI Login", href: "#oeci-login", subSection: false },
  {
    title: "Part 2: Search Records",
    href: "#search-records",
    subSection: false,
  },
  { title: "Assumptions", href: "#assumptions", subSection: true },
  { title: "Search", href: "#search", subSection: true },
  { title: "Results", href: "#results", subSection: true },
  { title: "Editing", href: "#editing", subSection: true },
  { title: "Fines and Fees", href: "#fines-and-fees", subSection: true },
  {
    title: "Part 3: Complete Paperwork",
    href: "#complete-paperwork",
    subSection: false,
  },
  { title: "Expungement", href: "#generate-paperwork", subSection: true },
  { title: "Financial Obligations", href: "#feewaiver", subSection: true },
  {
    title: "Part 4: Obtain Fingerprints",
    href: "#obtain-fingerprints",
    subSection: false,
  },
  {
    title: "Part 5: File Paperwork",
    href: "#file-paperwork",
    subSection: false,
  },
  { title: "FAQs", href: "#faqs", subSection: false },
];

interface Props {
  handleSidebarOpen?: () => void;
}

/**
 * Table-of-contents navigation for the Manual page.
 * Opens the target accordion section on click.
 */
function Sidebar({ handleSidebarOpen }: Props) {
  const handleClick = (href: string) => {
    const id = href.slice(1);
    openDetailsById(id);
    handleSidebarOpen?.();
  };

  return (
    <nav className="shrink-none w5 bg-white pa3" aria-label="Manual">
      <ul className="list">
        {sectionLinks.map((link, index) => {
          const isLast = index === sectionLinks.length - 1;
          return (
            <li
              className={`${isLast ? "" : "mb2"} ${
                link.subSection ? "ml3 f5" : ""
              }`}
              key={link.title}
            >
              <a
                href={link.href}
                onClick={() => handleClick(link.href)}
                className="link hover-blue"
              >
                {link.title}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

export default Sidebar;
