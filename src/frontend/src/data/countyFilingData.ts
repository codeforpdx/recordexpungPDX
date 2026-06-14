export interface CountyFilingInfo {
  waitMonths: number;
  notes: string[];
}

export const countyFilingData: Record<string, CountyFilingInfo> = {
  Clackamas: {
    waitMonths: 4,
    notes: ["DA routinely loses fingerprints"],
  },
  Columbia: {
    waitMonths: 4,
    notes: [
      "Columbia County Court requires the arresting agency be listed on the motion to set aside. This information can be gathered from (a) asking the client, (b) looking through court documents on OECI, or (c) calling the District Attorney.",
    ],
  },
  Jackson: { waitMonths: 3, notes: [] },
  Josephine: { waitMonths: 2, notes: [] },
  Klamath: {
    waitMonths: 8,
    notes: ['Will often object based on "character"'],
  },
  Multnomah: {
    waitMonths: 18,
    notes: [
      "If a person had a case that was dismissed because the court failed to provide a court-appointed attorney in a timely manner, filing an expungement on any other case in Multnomah can cause the DA to refer the case for prosecution, resulting in the person being re-indicted. Discuss with the participant that they may be re-indicted.",
      "If they want to completely avoid this, they should wait until after the Statute of Limitations has passed on their charges. Generally, SOL is three years for felonies, two years for misdemeanors, and six months for violations. Specific crimes have longer SOLs; consult ORS 131.125 for specifics.",
      "This only applies in Multnomah County — a person can still file in other counties.",
      "Even if the participant doesn't file, they can still be re-indicted.",
      "The Statute of Limitations pauses while a case is occurring.",
      "Filing is ultimately the participant's choice.",
    ],
  },
  Umatilla: {
    waitMonths: 4,
    notes: [
      "Umatilla County will not accept Motions to Modify Financial Obligations. The court doesn't even allow them to be filed.",
    ],
  },
  Washington: {
    waitMonths: 12,
    notes: [
      'Will often object based on "character"',
      "If a person has any subsequent criminal convictions, the DA in Washington will likely object, and a hearing will be held. The DA's position appears to be that a person is only eligible for expungement if they have not committed another crime after the one they are seeking to expunge.",
      "The court has sided with the DA on some of these, resulting in a denial of the person's expungement. The issue is currently on appeal.",
      'Example: a person files to expunge a Theft III from 2001 but also has a Theft II from 2008; the DA might object due to those circumstances and behavior.',
    ],
  },
};
