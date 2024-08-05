import matplotlib.pyplot as plt
import os
from collections import Counter

# Define file paths
log_file_path = './test3.log'
output_dir = './1500razeen/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the data from the provided test2.log file
with open(log_file_path, 'r') as file:
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
        try:
            total_divs_processed = int(line.split(': ')[1])
        except ValueError:
            continue
    if 'Total promoted divs:' in line:
        try:
            total_promoted_divs = int(line.split(': ')[1])
        except ValueError:
            continue

# Calculate the ratio of normal posts to sponsored posts
normal_posts = total_divs_processed - total_promoted_divs
ratio_normal_to_sponsored = normal_posts / total_promoted_divs if total_promoted_divs != 0 else 'N/A'
avg_sponsored_interval = total_divs_processed / total_promoted_divs if total_promoted_divs != 0 else 'N/A'

# Graph 1: Post Distribution
plt.figure(figsize=(10, 6))
categories = ['Total Posts', 'Normal Posts', 'Sponsored Posts']
values = [total_divs_processed, normal_posts, total_promoted_divs]
plt.bar(categories, values, color=['blue', 'green', 'red'])
plt.title('Post Distribution')
plt.xlabel('Post Type')
plt.ylabel('Count')
plt.savefig(os.path.join(output_dir, 'post_distribution.png'))
plt.close()

# Graph 2: Ratio of Normal to Sponsored Posts
plt.figure(figsize=(8, 8))
labels = ['Normal Posts', 'Sponsored Posts']
sizes = [normal_posts, total_promoted_divs]
colors = ['green', 'red']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Ratio of Normal to Sponsored Posts')
plt.savefig(os.path.join(output_dir, 'post_ratio.png'))
plt.close()

# Graph 3: Sponsored Post Frequency Over Time
plt.figure(figsize=(10, 6))
sponsored_post_positions = [i for i, line in enumerate(lines) if 'Sponsored:' in line]
plt.plot(sponsored_post_positions, list(range(1, len(sponsored_post_positions)+1)), marker='o', linestyle='-')
plt.title('Sponsored Post Frequency Over Time')
plt.xlabel('Post Position')
plt.ylabel('Cumulative Sponsored Posts')
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'sponsored_post_frequency_over_time.png'))
plt.close()

# Graph 4: Intervals Between Sponsored Posts Over Time
if len(sponsored_post_positions) > 1:
    intervals = [sponsored_post_positions[i] - sponsored_post_positions[i-1] for i in range(1, len(sponsored_post_positions))]
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(intervals)+1), intervals, marker='o', linestyle='-', color='purple')
    plt.title('Intervals Between Sponsored Posts Over Time')
    plt.xlabel('Interval Sequence')
    plt.ylabel('Interval Length (in posts)')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'intervals_between_sponsored_posts_over_time.png'))
    plt.close()

# Graph 5: Sponsor Dominance
sponsor_counts = Counter(sponsors)
sorted_sponsor_counts = sponsor_counts.most_common()
plt.figure(figsize=(12, 8))
sponsor_names, sponsor_frequencies = zip(*sorted_sponsor_counts)
plt.barh(sponsor_names, sponsor_frequencies, color='skyblue')
plt.title('Sponsor Dominance')
plt.xlabel('Number of Appearances')
plt.ylabel('Sponsor')
plt.gca().invert_yaxis()
plt.savefig(os.path.join(output_dir, 'sponsor_dominance.png'))
plt.close()

# Graph 6: Sponsor Appearance Over Time
plt.figure(figsize=(12, 8))
for sponsor in set(sponsors):
    sponsor_positions = [i for i, line in enumerate(lines) if f'Sponsored: {sponsor}' in line]
    plt.scatter(sponsor_positions, [sponsor] * len(sponsor_positions), label=sponsor, alpha=0.6)
plt.title('Sponsor Appearance Over Time')
plt.xlabel('Post Position')
plt.ylabel('Sponsor')
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'sponsor_appearance_over_time.png'))
plt.close()

# Save the sponsor dominance information to a text file
dominance_summary = "Sponsor Dominance Analysis:\n\n"
for sponsor, count in sorted_sponsor_counts:
    dominance_summary += f"{sponsor}: {count} appearances\n"

dominance_summary_file_path = os.path.join(output_dir, 'sponsor_dominance_summary.txt')
with open(dominance_summary_file_path, 'w') as file:
    file.write(dominance_summary)

# Summary of all metrics
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
summary_file_path = os.path.join(output_dir, 'hotspot_metrics_summary2.txt')
with open(summary_file_path, 'w') as output_file:
    output_file.write(summary)

