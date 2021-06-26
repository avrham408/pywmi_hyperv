import logging


logger = logging.getLogger(__name__)


def _parse_job_id(job_res: str) -> str:
    size = len(job_res)
    if size < 38:
        raise Exception(f"The response job is smaller then 38 {job_res} can't parse the job")
    instance_id = job_res[size - 37:size - 1]
    return instance_id
