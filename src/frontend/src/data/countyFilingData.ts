export interface CountyFilingInfo {
  waitMonths: number;
  notes: string[];
}

export const countyFilingData: Record<string, CountyFilingInfo> = {
  Clackamas: {
    waitMonths: 12,
    notes: ["DA routinely loses fingerprints"],
  },
  Columbia: {
    waitMonths: 4,
    notes: ["Arresting Agency must be filled out"],
  },
  Jackson: { waitMonths: 3, notes: [] },
  Josephine: { waitMonths: 2, notes: [] },
  Klamath: {
    waitMonths: 8,
    notes: ['Will often object based on "character"'],
  },
  Multnomah: { waitMonths: 18, notes: [] },
  Washington: {
    waitMonths: 12,
    notes: ['Will often object based on "character"'],
  },
};
