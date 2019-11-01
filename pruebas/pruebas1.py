higher       = []
lower        = []
past14Days   = [6971.73, 6937.08, 8218.05, 9251.27, 8870.82, 9114.72, 10226.86, 10107.26, 11233.95, 11767.74, 11459.71, 11104.2, 11175.87, 11429.02]

x = 0
for i in past14Days:
    if len(past14Days)-1 >= x+1:

        if past14Days[x+1] > past14Days[x]:
            high = past14Days[x+1] - past14Days[x]
            higher.append(high)

        elif past14Days[x+1] < past14Days[x]:
            low = past14Days[x] - past14Days[x+1]
            lower.append(low)
    x+=1

upwordAvg   = sum(higher) / len(higher)
downwordAvg = sum(lower) / len(lower)
print(upwordAvg)
print(downwordAvg)
RS          = upwordAvg / downwordAvg
RSI         = 100 - (100/(1+RS))

print(RSI)
