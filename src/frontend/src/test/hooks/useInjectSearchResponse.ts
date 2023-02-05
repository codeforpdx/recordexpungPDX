import { SearchResponse } from "../../redux/search/types";
import { useAppDispatch } from "../../redux/hooks";
import { storeSearchResponse } from "../../redux/search/actions";
import blank from "../data/blankResponse";
import complex from "../data/complexResponse";
import common from "../data/commonResponse";
import multiple from "../data/multipleResponse";

export type FakeResponseName = "blank" | "complex" | "common" | "multiple";

export function getResponseFromRecordName(name: FakeResponseName) {
  return {
    blank,
    complex,
    common,
    multiple,
  }[name] as SearchResponse;
}

export function useInjectSearchResponse(recordName?: FakeResponseName) {
  const dispatch = useAppDispatch();

  return () => {
    // just in case
    if (window.location.href.includes("recordsponge")) return;

    if (recordName) {
      storeSearchResponse(getResponseFromRecordName(recordName), dispatch);
    }
  };
}
