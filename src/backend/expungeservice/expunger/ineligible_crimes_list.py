"""
####################################################

this is the list of crime statute numbers which are INELIGIBLE for expungement
#todo: maybe put this list in the database and have some interface for the public defenders office to view/ modify it.

####################################################


"""

# in crimes list A, the pairs are a range, so anything equal to or between those values is not eligible
CrimesListA = [
    ['163.305', '163.479'],  # 'Crimes against Persons'
    ['163.670', '163.693'],  # todo: find out what these laws are and comment it here.
    ['167.008', '167.107'],  # Promoting/Compelling Prostitution
    ['167.057', '167.080']]  # Obscenity and minors

# List B consists of discreet values
CrimesListB = ['163.200',  # Criminal Mistreatment in the Second Degree: '163.200'
               '163.205',  # Criminal Mistreament in the First Degree: '163.205'
               '163.575',  # Endangering the welfare of a minor: '163.575'
               '163.535',  # Abandonment of a child: '163.535'
               '163.175',  # Attempted Assault in the Second Degree 163.175
               '163.275',  # Coercion 163.275
               '162.165',  # Attempted Escape in the First Degree 162.165
               '163.525',  # Incest: 163.525
               '163.225',  # Intimidation in the first degree: 163.225
               '164.405',  # Attempted Robbery in the Second Degree: 164.405
               '164.395',  # Robbery in the Third Degree: 164.395
               '162.185',  # Supplying contraband: 162.185
               '162.185',  # Unlawful use of a weapon: 166.220
               ]

#driving crimes is also a range so anything in between or equal to these values is ineligible
DrivingCrimes = [['801.000', '825.999']]

#some marijuana crimes are ineligible for expungment, note: these are NOT a range but rather they are discreet values
MarijuanaIneligible = ['475B.349(3)(C)', '475B.359', '475B.367', '475B.371', '419A.265', '167.262'] #475B.349(3)(C) unlawful manufacture of cannabinoid extract




