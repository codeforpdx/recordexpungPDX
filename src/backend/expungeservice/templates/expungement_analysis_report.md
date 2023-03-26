{{ header }}

## PLEASE READ THIS

### Disclaimer:
RecordSponge is not your lawyer. The results below should be used as a guide only. If you are relying on this information to expunge your record, please email roe@qiu-qiulaw.com for free consultation.

{% if has_open_cases %}
<b>You have open charges. You are not eligible to expunge ANY records, including old charges, while you have open charges.</b>
{% endif %}

### Assumptions
<b>1) Successful completion of court requirements</b> &nbsp; If you are currently on probation or conditional discharge, the analysis below assumes that you will successfully complete those requirements.

<b>2) Court debt paid off</b> &nbsp; You must pay off all court debt on a case before you file for expungement on any case which you are otherwise eligible to expunge.

<b>3) No records outside of Oregon State court from last seven years</b> &nbsp; We are only able to access your public Oregon records. Your analysis may be different if you have had cases from <b>within the last seven years</b> which were:

  * from States besides Oregon
  * from Federal Court (in any State)
  * from local District Courts, e.g. Medford Municipal Court (not Jackson Circuit Court)
  * already expunged

Below is a summary of your eligibility for expungement based on the assumptions above.
If the above assumptions are not true for you and you would like an updated analysis, email roe@qiu-qiulaw.com with your name and date of birth with subject line, “Updated Analysis”.

## Charges Eligible Now
{% if eligible_case_charges_tuples | count > 0 %}
  {% for case_info, charges_info in eligible_case_charges_tuples %}
    {% if case_info %}
 - {{ case_info }}
      {% for id, description in charges_info %}
     - description
      {% endfor %}
    {% else %}
      {% for id, description in charges_info %}
 - description
      {% endfor %}
    {% endif %}
  {% endfor %}
{% else %}
You are not currently eligible to expunge any charges.
{% endif %}

{% if ineligible_case_charges_tuples | count > 0 %}
## Ineligible Charges
These convictions are not eligible for expungement at any time under the current law.

  {% for case_info, charges_info in ineligible_case_charges_tuples %}
    {% if case_info %}
 - {{ case_info }}
      {% for id, description in charges_info %}
     - description
      {% endfor %}
    {% else %}
      {% for id, description in charges_info %}
 - description
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endif %}
