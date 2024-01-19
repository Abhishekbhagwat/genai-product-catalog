# Contributing

## Contributor's Setup

Follow the setup instructions for Data Scientists, plus the following:

* Java 17 + (Note, this is only for bulding the project)
    * [Azul](https://www.azul.com/downloads/#downloads-table-zulu)
* NodeJS
    * [Downloads](https://nodejs.org/en/download)

Once downloaded, install them to their default locations, and add the following
to you .bash_rs, .bash_profile, or .zsh_rc file:

### Mac OS X
```shell
# Sets the Java Home
export JAVA_HOME=`/usr/libexec/java_home -v 17`
```

### Finish setup from the project directory

```shell
# Install the CI/CD tools
# NOTE: not needed if only running the notebooks
npm install -g @bazel/bazelisk

# Test the build
bazel build //... 

# Run the test cases
bazel test //...
```

> NOTE: Bazel build a hermetic python environment, so it WILL NOT
> break your local python installs.

## Create a user.bazelrc

In the project root, create a file named `user.bazelrc`
and add the following contents:

```text
test --test_env=GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT_NAME>
```

## Running the examples

### Cloud Environment Setup


## Dependencies

### Mac

Install graphviz `brew install graphviz && brew install xdot` 

Visualize the dependency graph

```shell
bazel query "allpaths(//google ...)" | dot -Tpng -o docs/dependencies.png
```