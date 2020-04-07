import { Dispatch } from 'redux';
import apiService from '../../service/api-service';
import { AxiosError, AxiosResponse } from 'axios';
import {
  SEARCH_RECORD,
  SEARCH_RECORD_LOADING,
  SearchResponse,
  CLEAR_RECORD,
  SELECT_ANSWER,
  EDIT_ANSWER,
  CANCEL_EDIT,
  UPDATE_ANALYSIS,
  QuestionEndpointData,
  QuestionsEndpointData
} from './types';
import {AliasData} from '../../components/RecordSearch/SearchPanel/types'
import {RecordData, QuestionData, QuestionsData} from '../../components/RecordSearch/Record/types'

function storeSearchResponse(data: SearchResponse, dispatch: Dispatch) {
  if (validateSearchResponseData(data)) {
    const receivedRecord = data.record;
    const questions : QuestionsData = processReceivedQuestions(receivedRecord.questions);
    let record: RecordData = {
       total_balance_due: receivedRecord.total_balance_due,
       cases: receivedRecord.cases,
       errors: receivedRecord.errors,
       summary: receivedRecord.summary,
       };
    dispatch({
      type: SEARCH_RECORD,
      record: record,
      questions: questions

    });
  } else {
  alert('Response data has unexpected format.');
  }
}

function validateSearchResponseData(data: SearchResponse): boolean {
  return data.hasOwnProperty('record');
}

function processReceivedQuestions(receivedQuestions: QuestionsEndpointData) : QuestionsData {
  let processedQuestions: QuestionsData = {};
  let processedQuestion: QuestionData;
  let receivedQuestion: QuestionEndpointData;
  for (const ambiguous_charge_id of Object.keys(receivedQuestions)){
    receivedQuestion = receivedQuestions[ambiguous_charge_id]
    processedQuestion = {
      ambiguous_charge_id: receivedQuestion.ambiguous_charge_id,
      question: receivedQuestion.question,
      options: receivedQuestion.options,  //{[option: string]: string;};
      editing: false,
      analyzed: Boolean(receivedQuestion.answer),
      selected_answer: receivedQuestion.answer,
      submitted_answer: receivedQuestion.answer
    };
    processedQuestions[ambiguous_charge_id]=processedQuestion;
  }
  return processedQuestions;
}

/*function prepareDisambiguatingQuestions() : QuestionsEndpointData {
  // ignore flags for editing, analyzed, submitted_answer
  // but assemble the data object containing:
  //   ambiguous_charge_id: string;
  //   question : string;
  //   options: {[option: string]: string;};
  //   answer = selected_answer: string;
//
  }
}*/

export function disambiguateRecord() {
  // const questions : QuestionsEndpointData = prepareDisambiguatingQuestions();
  //return (dispatch: Dispatch)

  // receive the record and questions and handle them identically to what search call is doing
}
export function searchRecord(
  aliases: AliasData[]
): any {
  return (dispatch: Dispatch) => {
    dispatch({
      type: SEARCH_RECORD_LOADING
    });
    return apiService<SearchResponse>(dispatch, {
      url: '/api/search',
      data: {
        aliases: aliases
      },
      method: 'post',
      withCredentials: true
    })
      .then((response: AxiosResponse<SearchResponse>) => {
        storeSearchResponse(response.data, dispatch)
      })
      .catch((error: AxiosError<SearchResponse>) => {
        alert(error.message);
      });
  };
}

export function clearRecord() {
  return {
    type: CLEAR_RECORD
  };
}

export function selectAnswer(
  ambiguous_charge_id: string,
  answer: string): any {
  // when you hit a radio button, but nothing else visibly changes,
  // update in redux because that will make it possible to send off data to the endpoint

  // can either return a function that accepts a dispatch, and use the dispatch to
  // return data objects to be handled in the reducer,
  // or just return a data object to be handled in the reducer.
  // in this case, just issue a data object

  return {
    type: SELECT_ANSWER,
    ambiguous_charge_id: ambiguous_charge_id,
    selected_answer: answer
  }
}

export function updateAnalysis() {
  // construct a request object with Question from redux contents,
  // the request object has data structure QuestionEndpointData
  // the answers sent are:
  // whatever is in "selected", in all cases.
  // send the disambiguate request,
  // update the app state based on the response.
  // for all questions that have a selected answer, switch analyzed = true.
}

export function editAnswer() {
  // editing becomes true for that question, causing the display state (a property) to change.
  // this only happens if the question has been analyzed
}

export function cancelEdit() {
  // edit becomes false. the selected answer is reverted to the value of submitted answer.
}