import os


from pathlib import PathLike

gcp_vault = """
vault:
  gcp_secret_manager:
    project: <gcp-project-id>
""".strip()


def find_replace(file: PathLike, find: str, replace: str):
    file = os.path.expanduser(file)
    with open(file, "r") as f:
        content = f.read()
    content = content.replace(find, replace)
    with open(file, "w") as f:
        f.write(content)


def write_file(file: PathLike, content: str):
    file = os.path.expanduser(file)
    with open(file, "w") as f:
        f.write(content)


def setup_bigquery_cicd(reverse: bool = False):
    # setup variables
    project_dir = os.path.join("projects", "bigquery")
    profiles_dir = os.path.join(project_dir, "profiles")
    staging_profile = os.path.join(profiles_dir, "staging.yaml")

    to_find = "<your-gcp-project>"
    to_replace = "ascend-io-cody"
    if reverse:
        to_find, to_replace = to_replace, to_find

    find_replace(staging_profile, to_find[0], to_replace[0])

    to_find = "OTTOS_EXPEDITIONS_STAGING"
    to_replace = "ASCEND_COMMUNITY_OTTOS_EXPEDITIONS_STAGING_CICD"
    if reverse:
        to_find, to_replace = to_replace, to_find

    find_replace(staging_profile, to_find, to_replace)


def run_cicd_setup(reverse: bool = False):
    setup_bigquery_cicd(reverse=reverse)
