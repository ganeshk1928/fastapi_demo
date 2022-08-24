from fastapi import FastAPI
from fastapi import status
from subprocess import Popen, PIPE, CalledProcessError
import threading

app = FastAPI()


@app.get("/trigger", status_code=status.HTTP_201_CREATED)
def get_call(
    team: str, environment: str, eks_version: str, cluster_name: str, terraform_version: str, tfvars_url: str
):
    res = f"Team name - {team}, Environment - {environment}, EKS Version - {eks_version}, Cluster - {cluster_name}, Terraform Version - {terraform_version}, TFVARS URL - {tfvars_url}"
    
    output = []
    out_put = execute(team, environment, eks_version, cluster_name, terraform_version, tfvars_url)
    for out in out_put:
        output.append(out)
    print(output)

    return res


def execute(team, environment, eks_version, cluster_name, terraform_version, tfvars_url):
    cmd = ['sh', './script.sh', f'{team}', f'{environment}', f'{eks_version}', f'{cluster_name}', f'{terraform_version}', f'{tfvars_url}']
    popen = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE)
    error = []
    thread = threading.Thread(target=print_errors, args=(popen, error))
    thread.start()

    while popen.poll() is None:
        output = clean_output(popen.stdout.readline())
        if output:
            yield output

    # Process has finished, read rest of the output
    for output_line in popen.stdout.readlines():
        output = clean_output(output_line)
        if output:
            yield output

    popen.stdout.close()
    return_code = popen.wait()
    popen.kill()
    thread.join()
    if return_code:
        raise CalledProcessError(return_code, cmd, '\n'.join(error))


def clean_output(data):
    output = data.decode('utf-8').rstrip()
    return output


def print_errors(popen, error):
    while popen.poll() is None:
        stderr_line = clean_output(popen.stderr.readline())
        if stderr_line:
            error.append(stderr_line)

    for stderr in popen.stderr.readlines():
        stderr_line = clean_output(stderr)
        if stderr_line:
            error.append(stderr_line)
    popen.stderr.close()