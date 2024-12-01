FULL = 202299

total = 0

total += ( 1005 + 5867 + 984 ) # very top
total += ( 990 + 5870 + 987 ) # very bottom

# above
for row in range(FULL):
    total += ( 7819 + 7796 ) * ( FULL - (row + 1) )
    total += 7819
    total += ( 1005 + 6827 + 6836 + 984 )

# below
for row in range(FULL):
    total += ( 7819 + 7796 ) * ( FULL - (row + 1) )
    total += 7819
    total += ( 990 + 6820 + 6846 + 987 )

# center
total += ( 7819 + 7796 ) * FULL
total += 7819
total += ( 5851 + 5886 )

print(total)
