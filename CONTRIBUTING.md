# Contribution Guidelines

Welcome! Thank you for your interest in contributing to Project Magpie, we welcome all contributors! Please refer to the following guidelines before submmiting a pull request.

## <a name="question"></a> Questions?

If you have questions regarding how to use the Magpie API, please shoot an email to saavy2016@gmail.com.

## <a name="issue"></a> Found an Issue/ Want a Feature?
If you find a bug in the source code or a mistake in the documentation, you can help us by
submitting an issue to our GitHub Repository. 

You can also submit a Pull Request with a fix.

## <a name="submit"></a> Submission Guidelines

### Submitting an Issue
Before you submit your issue or feature request, search the archive, maybe your question was already answered.

### Submitting a Pull Request
We ask that all pull requests made must have an issue # in the description of the pull request.
Each pull request should contain a short description regarding what code was changed.

Please run all unit tests and comply with our style guides before submitting a request.

Example of a PR:

### Creating branches
As a contributor to Magpie, each branch must be named with short descriptor in underscores of the feature the code contributes to.
If the branch is to fix a bug, a *fix_* prefix should be added.
If possible, also add the issue number to the branch name as prefix, eg. *i20_*

example:
```
i4_fix_metadata_scrapper_bug <- bug fix branch with issue #4
i32_add_youtube_metadata_scrapper <- feature branch with issue #32
```

## <a name="rules"></a> Coding Rules


### Style Guide
We are using [<a href="https://google-styleguide.googlecode.com/svn/trunk/pyguide.html"> Google Python Style Guide </a>] as reference to our code base.

With the following additions/ exceptions:

- Seperate imports 3 different sections, seperated by an empty line between each section. Imports should be alphabetical
	- first section: standard import libraries
	- second section: external import libraries
	- third section: internal import

### Testing

You should be writing unit tests for any new features, if it is a bug fix the bug fix there should also be tests written for the bug fix.

Unit tests be structured in the same structure as the base file structure but instead located in `tests` file directory . 
Each unit test file should be prefixed with `test_`.

for example:
```
   client\
      api.py
   tests\
      client\
          test_api.py
```

