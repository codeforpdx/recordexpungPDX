import React from 'react';

export default class SearchResults extends React.Component {
  render() {
    return (
      <section className="bg-gray-blue-2 shadow br3 overflow-auto">
        {/* <div class="mb3">
          <div class="cf pv2 br3 br--top shadow-case">
            <div class="fl ph3 pv1">
              <span class="fw7">Case </span>
              <a class="underline" href="#">PA0061902</a>
            </div>
            <div class="fl ph3 pv1">
              <span class="fw7">Balance </span>
              $200.00
        </div>
            <div class="fl ph3 pv1">
              <span class="fw7">Name </span>
              Mark Monk
        </div>
            <div class="fl ph3 pv1">
              <span class="fw7">DOB </span>
              1/24/2014
        </div>
          </div>

          <div class="br3 ma2 bg-white">
            <h2 class="fw6 green bg-washed-green pv2 ph3 ma2 mb3 dib br3">Eligible now</h2>
            <div class="flex-l ph3 pb3">
              <div class="w-100 w-30-l pr3">
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-check-circle green"></i>
                  <div class="ml3 pl1"><span class="fw7">Time:</span> Eligible now</div>
                </div>
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-check-circle green"></i>
                  <div class="ml3 pl1"><span class="fw7">Type:</span> Eligible <span class="nowrap">137.225(5)(b)</span></div>
                </div>
              </div>
              <div class="w-100 w-70-l pr3">
                <ul class="list">
                  <li class="mb2">
                    <span class="fw7">Charge: </span>4759924B - Poss Controlled Sub 2
              </li>
                  <li class="mb2">
                    <span class="fw7">Disposition: </span>Convicted
              </li>
                  <li class="mb2">
                    <span class="fw7">Convicted: </span>2/12/1987
              </li>
                </ul>
              </div>
            </div>
          </div>

          <div class="br3 ma2 bg-white">
            <h2 class="fw6 dark-blue bg-washed-blue pv2 ph3 ma2 mb3 dib br3">Eligible 3/28/2023</h2>
            <div class="flex-l ph3 pb3">
              <div class="w-100 w-30-l pr3">
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-clock dark-blue"></i>
                  <div class="ml3 pl1"><span class="fw7">Time:</span> 10 years from most recent conviction</div>
                </div>
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-check-circle green"></i>
                  <div class="ml3 pl1"><span class="fw7">Type:</span> Eligible <span class="nowrap">137.225(5)(c)</span></div>
                </div>
              </div>
              <div class="w-100 w-70-l pr3">
                <ul class="list">
                  <li class="mb2">
                    <span class="fw7">Charge: </span>4759924B - Poss Controlled Sub 2
              </li>
                  <li class="mb2">
                    <span class="fw7">Disposition: </span>Dismissed
              </li>
                  <li class="mb2">
                    <span class="fw7">Arrested: </span>2/12/2007
              </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="mb3">
          <div class="cf pv2 br3 br--top shadow-case">
            <div class="fl ph3 pv1">
              <span class="fw7">Case </span>
              <a class="underline" href="#">P20111J11</a>
            </div>
            <div class="fl ph3 pv1">
              <span class="fw7">Balance </span>
              $0.00
        </div>
            <div class="fl ph3 pv1">
              <span class="fw7">Name </span>
              Mark Monk
        </div>
            <div class="fl ph3 pv1">
              <span class="fw7">DOB </span>
              1/24/2014
        </div>
          </div>

          <div class="br3 ma2 bg-white">
            <h2 class="fw6 purple bg-washed-purple pv2 ph3 ma2 mb3 dib br3">Eligible 11/28/2023 (review)</h2>
            <div class="flex-l ph3 pb3">
              <div class="w-100 w-30-l pr3">
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-clock dark-blue"></i>
                  <div class="ml3 pl1"><span class="fw7">Time:</span> No conviction within 3 years</div>
                </div>
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-question-circle purple"></i>
                  <div class="ml3 pl1"><span class="fw7">Type:</span> List B</div>
                </div>
              </div>
              <div class="w-100 w-70-l pr3">
                <ul class="list">
                  <li class="mb2">
                    <span class="fw7">Charge: </span>4759924B - Poss Controlled Sub 2
              </li>
                  <li class="mb2">
                    <span class="fw7">Disposition: </span>Dismissed
              </li>
                  <li class="mb2">
                    <span class="fw7">Arrested: </span>2/12/2007
              </li>
                </ul>
              </div>
            </div>
          </div>

          <div class="br3 ma2 bg-white">
            <h2 class="fw6 red bg-washed-red pv2 ph3 ma2 mb3 dib br3">Ineligible</h2>
            <div class="flex-l ph3 pb3">
              <div class="w-100 w-30-l pr3">
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-clock dark-blue"></i>
                  <div class="ml3 pl1"><span class="fw7">Time:</span> No more than 1 arrest in 3 years</div>
                </div>
                <div class="relative mb3">
                  <i aria-hidden="true" class="absolute fas fa-times-circle red"></i>
                  <div class="ml3 pl1"><span class="fw7">Type:</span> Ineligible <span class="nowrap">137.225(5)(a)(A)(i)</span></div>
                </div>
              </div>
              <div class="w-100 w-70-l pr3">
                <ul class="list">
                  <li class="mb2">
                    <span class="fw7">Charge: </span>2359924B - Ineligible type
              </li>
                  <li class="mb2">
                    <span class="fw7">Disposition: </span>Dismissed
              </li>
                  <li class="mb2">
                    <span class="fw7">Arrested: </span>2/12/2007
              </li>
                </ul>
              </div>
            </div>
          </div>
        </div> */}
      </section>
    );
  }
}
