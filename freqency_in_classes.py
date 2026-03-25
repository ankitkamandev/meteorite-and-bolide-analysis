import matplotlib.pyplot as plt
from data_prep import df2

''' Count of meteorite in each class '''
value_counts = df2['recclass'].value_counts()
total_count = value_counts.sum()

threshold_percentage = 1

filtered_value_counts = value_counts[value_counts / total_count * 100 > threshold_percentage]

filtered_value_counts['Other'] = total_count - filtered_value_counts.sum()

plt.figure(figsize=(8, 8))
filtered_value_counts.plot(kind='pie', autopct = '%1.1f%%', startangle = 90, legend = False)

plt.title('Distribution of recclass (Above 1%)')
plt.ylabel('')

print("\nCount of Meteorites in each class")
for class_name, count in filtered_value_counts.items():
    print(f"{class_name}: {count}")

plt.savefig('images/frequency_in_classes.png', bbox_inches='tight', dpi=300)

plt.show()
