export interface AliasData {
  // this data structure is sent in the endpoint request, so it uses python's snake_case
  first_name: string;
  middle_name: string;
  last_name: string;
  birth_date: string;
}
export type AliasFieldNames = "first_name" | "middle_name" | "last_name" | "birth_date";