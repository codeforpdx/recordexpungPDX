import { SearchRecordState } from "./types";

const initialState: SearchRecordState = {
  loading: "",
  loadingExpungementPacket: false,
  loadingWaiverPacket: false,
  edits: {},
  userInformation: {},
  waiverInformation: {}
};

export default initialState;
