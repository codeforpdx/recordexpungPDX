import { SearchRecordState } from "./types";

const initialState: SearchRecordState = {
  loading: "",
  loadingExpungementPacket: false,
  loadingWaiverPacket: false,
  edits: {},
  userInformation: {},
};

export default initialState;
