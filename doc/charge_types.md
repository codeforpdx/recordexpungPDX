# Charge Types
The expungement system defines this custom set of charge types, to compute their correct type eligibility."
## Civil Offense
\[rules documentation not added yet\]

## Contempt of Court
 This is a civil offense that is always ineligible regardless of level / conviction status 

## DUII
A DUII conviction is not eligible for expungement, as it is considered a traffic violation.
A DUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8)(b).
HOWEVER, a DUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.
Therefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.


## Felony Class A
Class A felony convictions generally are omitted from the statute, and are ineligible, unless that Class A Felony was related to the Manufacturing/Delivery/Possession of Marijuana.
Class A felony dismissals are always eligible under 137.225(5)(a).


## Felony Class B
Class B felony dismissals are always eligible under 137.225(5)(a).
Class B felony convictions are generally eligible but subject to additional restrictions compared to other charge types, as listed in 137.225(5)(a).
The extra restrictions are:
 * An extended time restriction: the class B felony is ineligible until 20 years after its date of conviction.
 * The class B felony is ineligible if the person has been arrested or convicted for any crime, other than a traffic violation, following the date of the class B felony conviction.
 * If the charge is also classified as a [Person Crime](manual/charge-types#personcrime) it is ineligible.
If a class B felony is eligible under any other subsection of the statute, that eligibility takes precedences and the extra restrictions here are ignored. The alternate positive criteria that can apply to B felonies are:
 * Some class B felonies fall under [Subsection 6](#Subsection6) or [Subsection 12](#Subsection12), which take precendence over 137.225(5)(a).
 * If the class B felony is punishable as a misdemeanor, it is eligible under 137.225(5)(b).

## Felony Class C
There are certain types of Class C felony which are generally ineligible, including sex crimes, child
abuse, elder abuse, traffic crimes, and criminally negligent homicide. Other Class C felony convictions are almost
always eligible under 137.225(5)(b).
Class C felony dismissals are always eligible under 137.225(1)(b).

## Juvenile
\[rules documentation not added yet\]

## Manufacture/Delivery
Manufacture/Delivery is possibly eligible if it pertains to marijuana, under statute 137.226.
Otherwise, it follows the normal eligibility rules for charge level and is typically a Class A or Class B Felony.
It might be a marijuana charge if the charge is for schedule 1, or if the schedule is not specified in the charge name. If it's schedule 2, we can conclude that it's not a marijuana charge.
The charge type is most easily idenfiable by name, so we check the presence of either of the following in the charge name (lowercase): "delivery", "manu/del".
If it's not a marijuana charge, This charge type may or may not have time eligibility under the Class B Felony rule. Because it's simpler to determine time eligibility for a B felony, we instruct the user to determine this information manually:
A Class B Felony that meets no other eligibility criteria will become eligible only after 20 years, and only if the person has no subsequent charges, other than traffic violations.
A dismissed Manufacture/Delivery charge is eligible under 137.225(1)(b).


## Marijuana Eligible
ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below.
    One way to identify a marijuana crime is if it has the statute section 475860.
    Also if "marijuana", "marij", or "mj" are in the charge name, we conclude it's a marijuana eligible charge (after filtering out MarijuanaIneligible charges by statute).

## Marijuana Ineligible
ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below. However, there are certain marijuana-related crimes which are still considered major felonies. These are:

475B.359 Arson incident to manufacture of cannabinoid extract in first degree
475B.367 Causing another person to ingest marijuana
475B.371 Administration to another person under 18 years of age
167.262: Use of minor in controlled substance or marijuana item offense

## Misdemeanor
Convictions for misdemeanors are generally eligible under ORS 137.225(5)(b).
Exceptions include convictions related to sex, child and elder abuse, and driving, including DUII

Dismissals for misdemeanors are generally eligible under ORS 137.225(1)(b). Exceptions include cases dismissed due to successful completion of DUII diversion.

## Parking Ticket
Parking Tickets are not eligible. ORS 137.225(7)(a) specifically prohibits expungement of convicted traffic offenses. No other section specifically allows for parking offenses to be eligible.

## Person Felony Class B
If a [Class B Felony](#FelonyClassB) is also defined as a person felony under Oregon law, it is type-ineligible.
A person felony is defined in section 14 of this page: (https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=712)
In some cases, the statute named in this list includes a subsection. Because OECI can have a data error that excludes the subsection, records that are a B felony and also charged under one of these sections are tagged with Needs More Analysis, because the charge may or may not constitute a person felony depending on the subsection under which the person was charged.
Dismissal of a person felony is eligible as usual under 137.225(1)(b).
A person felony that is below a class B felony is not considered under this subsection and lower levels of charge may still be eligible, with the exceptions named elsewhere such as in [Subsection 6](#Subsection6).


## Sex Crime

        Sex Crimes are type-ineligible for expungement, other than a narrow exception for "Romeo and Juliet" cases.
        For further detail, see 137.225(6)(a)
        

## Subsection 6
Subsection (6) names five felony statutes that have specific circumstances of the case under which they are ineligible.
However, two of the statutes named -- 163.165(1)(h) (Assault in the third degree)
This subsection also specifies conditions under which [SexCrimes](#SexCrime) are eligible or ineligible.
The three remaining specifications in the statute are:
 * 163.200 (Criminal mistreatment II) is ineligible if the victim at the time of the crime was 65 years of age or older; otherwise eligible as a (Class A) [Misdemeanor](#Misdemeanor).
 * 163.205 (Criminal mistreatment I) is ineligible if the victim at the time of the crime was 65 years of age or older or a minor; otherwise eligible as a [Class C Felony](#FelonyClassC).
 * 163.575 (Endangering the welfare of a minor) (1)(a) is ineligible when the offense constitutes child abuse as defined in ORS 419B.005 (Definitions); otherwise eligible as a (Class A) [Misdemeanor](#Misdemeanor).
 * 163.145 (Criminally negligent homicide) is ineligible when that offense was punishable as a Class C felony.
Dismissals are eligible under 137.225(1)(b).

## Traffic Non-Violation
\[rules documentation not added yet\]

## Traffic Violation
Convictions for traffic-related offenses are not eligible for expungement under ORS 137.225(7)(a). This includes Violations, Misdemeanors, and Felonies. Traffic-related charges include Reckless Driving, Driving While Suspended, DUII, Failure to Perform Duties of a Driver, Giving False Information to a Police Officer (when in a car), Fleeing/Attempting to Elude a Police Officer, Possession of a Stolen Vehicle
Notably, Unauthorized Use of a Vehicle is not considered a traffic offense.
Dismissed traffic-related Violations are not eligible for expungement
HOWEVER, dismissed traffic-related Misdemeanors and Felonies, like all dismissed Misdemeanors and Felonies, ARE eligible for expungement.

## Unclassified
\[rules documentation not added yet\]

## Violation
Violation convictions are eligible under ORS 137.225(5)(d).
Examples include Fare Violation, Minor in Possession of Alcohol, Failure to Send or Maintain a Child in School.
However, traffic violations are ineligible under (7)(a).
Moreover, certain civil matters are not considered violations and are thus not eligible: Contempt of Court, Extradition.
Dismissed violations are ineligible because they are omitted from the expungement statute.
