import math

heart_rate_data = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]


heart_rate_peaks = []
successive_differences = []

for i in range(1, len(heart_rate_data)-1):
    if heart_rate_data[i] > heart_rate_data[i-1] and heart_rate_data[i] > heart_rate_data[i+1]:
        heart_rate_peaks.append(heart_rate_data[i])
        

mean_ppi = sum(heart_rate_data)/len(heart_rate_data)


heart_rate = 60/(mean_ppi/1000)

for i in range(1, len(heart_rate_data)):
    difference = heart_rate_data[i] - heart_rate_data[i-1]
    successive_differences.append(difference)

squared_differences = [x**2 for x in successive_differences]

mean_squared_differences = sum(squared_differences) / len(squared_differences)
rmssd = mean_squared_differences ** 0.5


deviations = [(x - mean_ppi) ** 2 for x in heart_rate_peaks]

sum_sq_dev = sum(deviations)

sdnn = math.sqrt(sum_sq_dev / (len(heart_rate_peaks) ))

print("Heart rate peaks: ", heart_rate_peaks)

print("Mean PPI: ", round(mean_ppi))

print("Mean heart rate :", round(heart_rate))

print("RMSSD: ", round(rmssd))

print("SDNN: ", round(sdnn))

