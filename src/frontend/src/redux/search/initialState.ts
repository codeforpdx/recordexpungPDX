import { SearchRecordState } from "./types";

const initialState: SearchRecordState = {
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
  userInformation: {},
};

export default initialState;
