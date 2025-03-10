from ray.job_submission import JobSubmissionClient

client = JobSubmissionClient("http://127.0.0.1:8265")
job_id = client.submit_job(
    entrypoint="python main.py",
    runtime_env={"working_dir": "./"}
)
print(job_id)
