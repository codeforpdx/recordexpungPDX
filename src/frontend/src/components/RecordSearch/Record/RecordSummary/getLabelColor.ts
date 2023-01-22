export default function getElibilityColor(eligibility: string) {
  return (
    {
      "Eligible Now": "green",
      Ineligible: "red",
      "Needs More Analysis": "purple",
    }[eligibility] ?? "dark-blue"
  );
}
