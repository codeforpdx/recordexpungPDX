export default {
  request: jest.fn(request => {
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
        data: [
          {
            name: 'WOODS, LAVELLE D',
            birth_year: 1970,
            case_number: 'ZA0081909',
            citation_number: 'ZA0081909',
            location: 'Multnomah',
            date: '07/02/2013',
            violation_type: 'Offense Violation',
            current_status: 'Inactive',
            balance_due: '0',
            charges: [
              {
                name: 'Failure to Properly Use Safety Belts - MV Operator',
                statute: '8112101A',
                level: 'Violation Class D',
                date: '06/11/2013',
                disposition: {
                  date: '07/16/2013',
                  ruling: 'Convicted'
                },
                expungement_result: {
                  type_eligibility: 'True',
                  type_eligibility_reason: 'some string',
                  time_eligibility: 'True',
                  time_eligibility_reason: 'some string',
                  date_of_eligibility: 'date'
                }
              }
            ],
            case_detail_link:
              'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=9036658'
          }
        ]
      });
    } else if (
      request.url.includes('http://localhost:5000/api/') &&
      request.method === 'get'
    ) {
      return Promise.reject({
        error: new Error('Request failed with status code 404')
      });
    } else if (!request.url.includes('http://localhost:5000/api/')) {
      return Promise.reject({
        error: new Error(
          'bad base url, it should be: http://localhost:5000/api/'
        )
      });
    } else {
      return Promise.reject({
        error: new Error(
          `mock API doesn't recognize the request.  Please check your code, or update the mock API`
        )
      });
    }
  })
};
