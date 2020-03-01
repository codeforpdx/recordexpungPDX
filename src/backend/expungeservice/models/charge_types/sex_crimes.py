from dataclasses import dataclass

from expungeservice.models.charge import Charge
from expungeservice.models.expungement_result import TypeEligibility, EligibilityStatus


@dataclass(eq=False)
class SexCrimes(Charge):
    type_name: str = "Sex Crimes"
    expungement_rules: str = (
        """
        Sex Crimes are type-ineligible for expungement, other than a narrow exception for "Romeo and Juliet" cases.
        According to 137.225(6)(a):
        Notwithstanding subsection (5) of this section, the provisions of subsection (1)(a) of this section do not apply 
        to a conviction for:
            (...)
            (f)Any sex crime, unless:
                (A)The sex crime is listed in ORS 163A.140 (Relief from reporting obligation) (1)(a) and:
                (i)The person has been relieved of the obligation to report as a sex offender pursuant to a court order 
                entered under ORS 163A.145 (Procedure for relief under ORS 163A.140) or 163A.150 (Procedure for relief 
                under ORS 163A.140); and
                (ii)The person has not been convicted of, found guilty except for insanity of or found to be within the 
                jurisdiction of the juvenile court based on a crime for which the court is prohibited from setting aside 
                the conviction under this section; or
                    (B)The sex crime constitutes a Class C felony and:
                (i)The person was under 16 years of age at the time of the offense;
                (ii)The person is:
                    (I)Less than two years and 180 days older than the victim; or
                    (II)At least two years and 180 days older, but less than three years and 180 days older, than the 
                    victim and the court finds that setting aside the conviction is in the interests of justice and of 
                    benefit to the person and the community;
                (iii) The victim’s lack of consent was due solely to incapacity to consent by reason of being less than 
                a specified age;
                (iv)The victim was at least 12 years of age at the time of the offense;
                (v)The person has not been convicted of, found guilty except for insanity of or found to be within the 
                jurisdiction of the juvenile court based on a crime for which the court is prohibited from setting aside
                the conviction under this section; and
                (vi)Each conviction or finding described in this subparagraph involved the same victim.
        """
    )

    statutes = [
        '163365',  # Rape II
        '163375',  # Rape I
        '163395',  # Sodomy II
        '163405',  # Sodomy I
        '163408',  # Sexual Penetration II
        '163411',  # Sexual Penetration I
        '163413',  # Purchasing Sex with a Minor
        '163425',  # Sexual Abuse II
        '163427',  # Sexual Abuse I
        '163432',  # Online Sexual Corruption of a Child II
        '163433',  # Online Sexual Corruption of a Child I
        '163452',  # Custodial Sexual Misconduct in the First Degree
        '163454',  # Custodial sexual misconduct in the second degree
        '163465',  # Felony Public Indecency
        '163467',  # Private indecency
        '163472',  # Unlawful Dissemination of Initimate Image
        '163476',  # Unlawfully being in a location where children regularly congregate
        '163479',  # Unlawful Contact with a Child
        '163670',  # Using Child In Display of Sexual Conduct
        '163684',  # Encouraging Child Sex Abuse I
        '163686',  # Encouraging Child Sex Abuse II
        '163687',  # Encouraging child sexual abuse in the third degree
        '163688',  # Possession of Material Depicting Sexually Explicit Conduct of Child I
        '163689',  # Possession of Material Depicting Sexually Explicit Conduct of Child II
        '163693',  # Failure to report Child Pornography
    ]


    # Romeo and Juliet exception; If a person is convicted of one of the following, and follows certain other
    # requirements which are not identifiable in eCourts, they are eligible.
    romeo_and_juliet_exceptions = [
        '163355',  # Rape in the third degree
        '163385',  # Sodomy in the third degree
        '163415',  # Sexual Abuse in the Third Degree
        '163435',  # Contributing to the sexual deliquency of a minor
        '163445',  # Sexual Misconduct
    ]

    def _type_eligibility(self):
        if self.dismissed():
            return TypeEligibility(EligibilityStatus.ELIGIBLE, reason="Dismissals are eligible under 137.225(1)(b)")
        elif self.convicted():
            if self.statute in self.romeo_and_juliet_exceptions:
                return TypeEligibility(
                    EligibilityStatus.NEEDS_MORE_ANALYSIS,
                    reason="Romeo and Juliet exception, needs other elligibility requirements. See 163A.140(1)",
                )
            else:
                return TypeEligibility(EligibilityStatus.INELIGIBLE, reason="Ineligible under 137.225(6)(a)")
