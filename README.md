# How to Make Delicious Chicken Wings with Lambda Functions

MacAdmins Campfire Sessions 2021.

## Dev Environment

This project requites the following utilities:
- AWS SAM CLI ([Pip](https://pypi.org/project/aws-sam-cli/) , [Homebrew](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html#serverless-sam-cli-install-mac-sam-cli))
- Pipenv ([Pip](https://pipenv.pypa.io/en/latest/install/))
- Docker ([Desktop](https://www.docker.com/products/docker-desktop))

### Setup Pipenv

To sync your local development environment with the project Pipfile, run:

```shell
pipenv --sync --dev
```

### Linting and Tests

Code must conform to the Python `black` linter version in the Pipfile. You can set up automatic linting and formatting for your IDE.

```shell
# Run 'black' against all Python files to auto-format
pipenv run black .
# Alternatively, check files without formatting them
pipenv run black --check .
```

CloudFormation templates must pass validation using `cfn-lint`.

```shell
# Test template files (ignoring non-CloudFormation files)
pipenv run cfn-lint ./*.yaml
```

This project uses `pytest` for unit testing. All files are expected to have test coverage better than 90% coverage and passing. Unit tests should cover expected event patterns and success/fail states.

```shell
# Run all tests
pipenv run pytest

# Run one test file
pipenv run pytest tests/test_my_file

# Run one test within a file
pipenv run pytest tests/test_my_file::test_my_test
```

### Deploy Dev Stack

Create a `samconfig.toml` file by running the following command and following the prompts:

```shell
sam deploy --guided --profile ${AWS_PROFILE_NAME}
```

Deploy the entire environment using the `template.yaml` file at the root of the repo and the SAM config created in the previous step.

```shell
sam build --use-container --cached && sam deploy
# sam build -uc && sam deploy
```
