import moment from "moment";

const today = moment().format("M/D/YYYY");

export const expectedLoginRequest = {
  data: { oeci_password: "secret", oeci_username: "username" },
  method: "post",
  url: "/api/oeci_login",
  withCredentials: true,
};

export const expectedSearchRequest = {
  data: {
    aliases: [
      {
        birth_date: "",
        first_name: "foo",
        last_name: "bar",
        middle_name: "",
      },
    ],
    demo: false,
    edits: {},
    questions: {},
    today,
  },
  method: "post",
  url: "/api/search",
  withCredentials: true,
};

export const expectedPdfRequest = {
  data: {
    aliases: [
      {
        birth_date: "",
        first_name: "foo",
        last_name: "bar",
        middle_name: "",
      },
    ],
    demo: false,
    edits: {},
    questions: {},
    today,
  },
  method: "post",
  responseType: "blob",
  url: "/api/pdf",
  withCredentials: true,
};

export const expectedPacketRequest = {
  data: {
    aliases: [
      {
        birth_date: "",
        first_name: "foo",
        last_name: "bar",
        middle_name: "",
      },
    ],
    demo: false,
    edits: {},
    questions: {},
    today,
    userInformation: {
      city: "Portland",
      date_of_birth: "12/12/1999",
      full_name: "foo bar",
      mailing_address: "1111 NE anywhere",
      phone_number: "123-456-7890",
      state: "Oregon",
      zip_code: "12345",
    },
  },
  method: "post",
  responseType: "blob",
  url: "/api/expungement-packet",
  withCredentials: true,
};

export const expectedSecondSearchRequest = {
  data: {
    aliases: [
      { birth_date: "", first_name: "foo", last_name: "bar", middle_name: "" },
      {
        birth_date: "2/23/1999",
        first_name: "fooRocky",
        last_name: "barBalboa",
        middle_name: "",
      },
    ],
    demo: false,
    edits: {},
    questions: {},
    today,
  },
  method: "post",
  url: "/api/search",
  withCredentials: true,
};

export const expectedThirdSearchRequest = {
  data: {
    aliases: [
      {
        birth_date: "2/23/1999",
        first_name: "fooRocky",
        last_name: "barBalboa",
        middle_name: "",
      },
    ],
    demo: false,
    edits: {},
    questions: {},
    today,
  },
  method: "post",
  url: "/api/search",
  withCredentials: true,
};
