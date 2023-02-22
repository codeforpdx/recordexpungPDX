import React from "react";
import { useAppSelector } from "../../../redux/hooks";
import LoadingSpinner from "../../LoadingSpinner";

export default function Status() {
  const record = useAppSelector((state) => state.search.record);
  const loading = useAppSelector((state) => state.search.loading);

  return (
    <section>
      {loading === "loading" ? (
        <LoadingSpinner inputString="your search results" />
      ) : record?.cases?.length === 0 ? (
        <p className="bg-light-gray mv4 pa4 br3 fw6">
          No search results found.
        </p>
      ) : null}
    </section>
  );
}
