import moment from "moment";

const today = moment().format("M/D/YYYY");

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
    demo: true,
    edits: {},
    questions: {},
    today,
  },
  method: "post",
  url: "/api/demo",
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
    demo: true,
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
    demo: true,
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
