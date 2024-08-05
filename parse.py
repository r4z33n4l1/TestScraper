# Let's read the data from the provided test.log file and then parse it
file_path = 'test2.log'

with open(file_path, 'r') as file:
    data = file.read()

# Extract sponsors and relevant metrics from the data
sponsors = []
total_divs_processed = 0
total_promoted_divs = 0

# Splitting the data by lines
lines = data.split('\n')

for line in lines:
    if 'Sponsored:' in line:
        # Extracting the sponsor name
        sponsor_name = line.split('Sponsored: ')[1].split('Sponsored,')[0].strip()
        sponsors.append(sponsor_name)
    if 'Total divs processed:' in line:
        total_divs_processed = int(line.split(': ')[1])
    if 'Total promoted divs:' in line:
        total_promoted_divs = int(line.split(': ')[1])

# Calculate the ratio of normal posts to sponsored posts
normal_posts = total_divs_processed - total_promoted_divs
ratio_normal_to_sponsored = normal_posts / total_promoted_divs if total_promoted_divs != 0 else 'N/A'

# Calculate how often sponsored posts come up on average
avg_sponsored_interval = total_divs_processed / total_promoted_divs if total_promoted_divs != 0 else 'N/A'

# Creating a summary of the data
summary = f"""
List of Sponsors:
{', '.join(set(sponsors))}

Total Divs Processed: {total_divs_processed}
Total Promoted Divs: {total_promoted_divs}
Ratio of Normal Posts to Sponsored Posts: {ratio_normal_to_sponsored}
Average Interval of Sponsored Posts: Every {avg_sponsored_interval} posts

Other Metrics:
- Total Normal Posts: {normal_posts}
"""
    
# Save the summary into a txt file
output_file_path = 'hotspot_metrics_summary2.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(summary)

output_file_path
