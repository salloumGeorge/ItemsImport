import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Sample log data (replace this with reading from your actual log file)
log_data = """2024-11-01T22:25:09Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:11Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:14Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:16Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.01%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:19Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:21Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:24Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:27Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.02%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:29Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:32Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:34Z,{"BlockIO":"82.1MB / 2.74GB","CPUPerc":"0.00%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"11.45%","MemUsage":"171.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"323MB / 96.7MB","PIDs":"7"}
2024-11-01T22:25:37Z,{"BlockIO":"84.9MB / 2.77GB","CPUPerc":"49.05%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"12.51%","MemUsage":"187.7MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"333MB / 99.6MB","PIDs":"17"}
2024-11-01T22:25:39Z,{"BlockIO":"91.3MB / 2.82GB","CPUPerc":"49.10%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"12.66%","MemUsage":"190MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"354MB / 105MB","PIDs":"17"}
2024-11-01T22:25:42Z,{"BlockIO":"99MB / 3.05GB","CPUPerc":"42.27%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"12.98%","MemUsage":"194.8MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"372MB / 110MB","PIDs":"18"}
2024-11-01T22:25:44Z,{"BlockIO":"135MB / 3.1GB","CPUPerc":"49.40%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.30%","MemUsage":"199.5MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"390MB / 115MB","PIDs":"17"}
2024-11-01T22:25:47Z,{"BlockIO":"142MB / 3.37GB","CPUPerc":"49.07%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.64%","MemUsage":"204.7MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"410MB / 121MB","PIDs":"17"}
2024-11-01T22:25:49Z,{"BlockIO":"146MB / 3.41GB","CPUPerc":"0.67%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.68%","MemUsage":"205.2MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"420MB / 123MB","PIDs":"17"}
2024-11-01T22:25:52Z,{"BlockIO":"146MB / 3.42GB","CPUPerc":"1.26%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.68%","MemUsage":"205.2MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"420MB / 123MB","PIDs":"17"}
2024-11-01T22:25:54Z,{"BlockIO":"146MB / 3.42GB","CPUPerc":"0.65%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.66%","MemUsage":"204.9MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"420MB / 123MB","PIDs":"17"}
2024-11-01T22:25:57Z,{"BlockIO":"146MB / 3.42GB","CPUPerc":"0.31%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.66%","MemUsage":"204.9MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"420MB / 123MB","PIDs":"17"}
2024-11-01T22:26:00Z,{"BlockIO":"150MB / 3.47GB","CPUPerc":"49.89%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.91%","MemUsage":"208.6MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"430MB / 126MB","PIDs":"17"}
2024-11-01T22:26:02Z,{"BlockIO":"155MB / 3.57GB","CPUPerc":"50.07%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.89%","MemUsage":"208.3MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"443MB / 130MB","PIDs":"17"}
2024-11-01T22:26:05Z,{"BlockIO":"161MB / 3.78GB","CPUPerc":"49.34%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.89%","MemUsage":"208.4MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"456MB / 133MB","PIDs":"17"}
2024-11-01T22:26:07Z,{"BlockIO":"167MB / 3.9GB","CPUPerc":"50.13%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.87%","MemUsage":"208.1MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"469MB / 137MB","PIDs":"17"}
2024-11-01T22:26:10Z,{"BlockIO":"174MB / 4.17GB","CPUPerc":"51.01%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.89%","MemUsage":"208.3MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"484MB / 141MB","PIDs":"17"}
2024-11-01T22:26:12Z,{"BlockIO":"180MB / 4.35GB","CPUPerc":"49.35%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.90%","MemUsage":"208.5MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"495MB / 144MB","PIDs":"17"}
2024-11-01T22:26:15Z,{"BlockIO":"187MB / 4.62GB","CPUPerc":"50.86%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.87%","MemUsage":"208MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"508MB / 147MB","PIDs":"17"}
2024-11-01T22:26:17Z,{"BlockIO":"193MB / 4.83GB","CPUPerc":"32.49%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.87%","MemUsage":"208MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
2024-11-01T22:26:20Z,{"BlockIO":"193MB / 4.84GB","CPUPerc":"1.52%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.87%","MemUsage":"208MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
2024-11-01T22:26:22Z,{"BlockIO":"193MB / 4.97GB","CPUPerc":"0.63%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.87%","MemUsage":"208MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
2024-11-01T22:26:25Z,{"BlockIO":"193MB / 4.97GB","CPUPerc":"0.35%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.86%","MemUsage":"208MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
2024-11-01T22:26:27Z,{"BlockIO":"193MB / 4.97GB","CPUPerc":"0.79%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.86%","MemUsage":"208MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
2024-11-01T22:26:30Z,{"BlockIO":"193MB / 4.98GB","CPUPerc":"0.33%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.86%","MemUsage":"207.9MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
2024-11-01T22:26:33Z,{"BlockIO":"193MB / 4.98GB","CPUPerc":"0.32%","Container":"d5bece7b0fe3","ID":"d5bece7b0fe3","MemPerc":"13.86%","MemUsage":"207.9MiB / 1.465GiB","Name":"itemsservice-db-1","NetIO":"518MB / 150MB","PIDs":"17"}
"""

# Parse the log data
lines = log_data.strip().split('\n')
timestamps = []
cpu_usage = []
mem_usage = []

for line in lines:
    timestamp_str, json_data = line.split(',', 1)
    timestamp = datetime.fromisoformat(timestamp_str[:-1])  # Convert to datetime
    data = json.loads(json_data)  # Parse the JSON

    timestamps.append(timestamp)
    cpu_usage.append(float(data['CPUPerc'].strip('%')))  # Convert CPU percentage to float
    mem_percentage = float(data['MemPerc'].strip('%'))  # Convert Memory percentage to float
    mem_usage.append(mem_percentage)

# Create a DataFrame for easier plotting
df = pd.DataFrame({
    'Timestamp': timestamps,
    'CPU Usage (%)': cpu_usage,
    'Memory Usage (%)': mem_usage
})

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['CPU Usage (%)'], label='CPU Usage (%)', marker='o')
plt.plot(df['Timestamp'], df['Memory Usage (%)'], label='Memory Usage (%)', marker='x')

# Formatting the plot
plt.title('CPU and Memory Usage Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Usage (%)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()

# Show the plot
plt.show()
