import matplotlib.pyplot as plt
from data_prep import df1
'''Frequency of Bolide over the years'''

yearly_counts = df1['Date/Time - Peak Brightness (UT)'].dt.year.value_counts().sort_index()

if yearly_counts.empty:
    print("No CSV file was found")
else:
    plt.figure(figsize=(10, 6))
    yearly_counts.plot(kind='bar', color='skyblue', edgecolor='black')

    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Frequency of Bolide Appearance Over Time', fontsize=14)

    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.savefig('images/frequency_of_bolides.png', bbox_inches='tight', dpi=300)
    plt.show()
