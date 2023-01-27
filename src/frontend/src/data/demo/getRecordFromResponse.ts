import { RecordData } from "../../components/RecordSearch/Record/types";

export default function getRecordFromResponse(response: { record: any }) {
  const { questions, ...record_ } = response.record;
  return record_ as RecordData;
}
