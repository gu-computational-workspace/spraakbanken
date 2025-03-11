import sys
from ray.job_submission import JobSubmissionClient

runtime_env = {
                "pip": "./requirements.txt",
                "working_dir": "./"
        }

client = JobSubmissionClient("http://127.0.0.1:8265")
job_id = client.submit_job(
    entrypoint="python main.py " + sys.argv[1],
    runtime_env=runtime_env
)

print(job_id)
