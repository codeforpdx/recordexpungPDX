import { AxiosRequestConfig } from 'axios';

export default {
  request: requestMock
};

function requestMock<T>(request: AxiosRequestConfig): Promise<any> {
  if (
    request.url === 'http://localhost:5000/api/hello' &&
    request.method === 'get'
  ) {
    return Promise.resolve({
      data: 'Hello, world!'
    });
  } else if (
    request.url === 'http://localhost:5000/api/search' &&
    request.method === 'post'
  ) {
    return Promise.resolve({
      data: {
        data: {
          record: fakeRecord
        }
      }
    });
  } else if (
    request.url &&
    request.url.includes('http://localhost:5000/api/') &&
    request.method === 'get'
  ) {
    return Promise.reject({
      error: new Error('Request failed with status code 404')
    });
  } else if (
    request.url &&
    !request.url.includes('http://localhost:5000/api/')
  ) {
    return Promise.reject({
      error: new Error('bad base url, it should be: http://localhost:5000/api/')
    });
  } else {
    return Promise.reject({
      error: new Error(
        `mock API doesn't recognize the request.  Please check your code, or update the mock API`
      )
    });
  }
}

const fakeRecord = {
  record: {
    total_balance_due: 199.99,
    errors: [],
    cases: [
      {
        name: 'Doe, John',
        birth_year: 1970,
        case_number: 'HA05555555',
        citation_number: 'HA08643443',
        location: 'Multnomah',
        date: '09/05/2008',
        violation_type: 'Municipal Parking',
        current_status: 'Closed',
        charges: [
          {
            name: 'Loading Zone',
            statute: '29',
            level: 'Violation Unclassified',
            date: '09/04/2008',
            disposition: {
              date: '11/18/2008',
              ruling: 'Convicted'
            },
            expungement_result: {
              type_eligibility: {
                status: 'Ineligible',
                reason: 'Ineligible under 137.225(5)'
              },
              time_eligibility: null
            }
          }
        ],
        balance_due: 199.99,
        case_detail_link:
          'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=11918348'
      },
      {
        name: 'Doe, John',
        birth_year: 1970,
        case_number: '18VI55555',
        citation_number: 'RU420001442',
        location: 'Multnomah',
        date: '04/02/2018',
        violation_type: 'Offense Violation',
        current_status: 'Closed',
        charges: [
          {
            name: 'Violating a Speed Limit',
            statute: '811111',
            level: 'Violation Class A',
            date: '03/06/2018',
            disposition: {
              date: '04/02/2018',
              ruling: 'Dismissed'
            },
            expungement_result: {
              type_eligibility: {
                status: 'Eligible',
                reason: 'Eligible under 137.225(1)(b)'
              },
              time_eligibility: {
                status: 'Ineligible',
                reason: '',
                date_will_be_eligible: '2/11/2020'
              }
            }
          },
          {
            name: 'Violation Driving While Suspended or Revoked',
            statute: '811175',
            level: 'Violation Class A',
            date: '03/06/2018',
            disposition: {
              date: '04/02/2018',
              ruling: 'Dismissed'
            },
            expungement_result: {
              type_eligibility: {
                status: 'Eligible',
                reason: 'Eligible under 137.225(1)(b)'
              },
              time_eligibility: {
                status: 'Ineligible',
                reason: '',
                date_will_be_eligible: '2/11/2020'
              }
            }
          }
        ],
        balance_due: 0.0,
        case_detail_link:
          'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=55555555'
      }
    ]
  }
};
