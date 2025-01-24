logging 
rich_console.info(f"Running `update` {{git, pull}}...")
ho to run setup.sh
# Perform git pull to update
res = subprocess.run(['git', 'pull'], check=True)
rich_console.info(res)

rich_console.info(f"Running `{scriptname}`...")
# Run the specified script
result = subprocess.run(['python3', scriptname], check=True)

# Log the output
rich_console.info(result)