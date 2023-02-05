import { SearchRecordState } from "./types";

const initialState: SearchRecordState = {
  demo: false,
  loading: "",
  loadingExpungementPacket: false,
  aliases: [
    {
      first_name: "",
      middle_name: "",
      last_name: "",
      birth_date: "",
    },
  ],
  today: "",
  edits: {},
  editingRecord: false,
  userInformation: {},
};

export default initialState;
