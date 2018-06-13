PyKwiki Contributions
=====================

Extra items for use with PyKwiki deployments

## gitlab-ci.yml

The Continuous Integration configuration needed to publish GitLab Pages from the PyKwiki project upon every commit to master. Requires PyKwiki 2.1.20+ in order to set the output directory to the GitLab expected `public` subdirectory.

1. Set `target_dir: public` in PyKwiki's `config.yaml`
1. Copy `gitlab-ci.yml` to the top level of the git project as `.gitlab-ci.yml`

The project must have already been set up with the basics first, it does not initialize a new PyKwiki source/content tree. See the [GitLab Pages documentation](https://docs.gitlab.com/ee/user/project/pages/) for more information.

