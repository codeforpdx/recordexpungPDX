# Contributing

This document provides some overall guidelines and suggestions for how to get started with contributing to the project. There are several features, enhancements, and fixes that we'd like to work on, so there are lots of opportunities to get started.

## Table of Contents
- [First steps](#first-steps)
- [Contributing code](#contributing-code)
- [Installation](#installation)
- [Running Components](#running-the-docker-stack)

### First steps

1. [Set up your local dev environment](README.md#installation)
2. Be sure to read our [code of conduct](CODE_OF_CONDUCT.md)
3. Say hi on our Slack Channel!

### Contributing code

 1. **[Fork](https://help.github.com/articles/fork-a-repo/#fork-an-example-repository)** the repo on GitHub
 and **[Clone](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork)** the project to your own machine. Replacing YOUR-USERNAME with your github username.
   ```bash
    $ git clone https://github.com/YOUR-USERNAME/recordexpungPDX.git
   ```
 3. cd into recordexpungPDX
   ```bash
    $ cd recordexpungPDX
   ```
 4. Configure upstream to sync with your fork
   ```bash
    $ git remote add upstream https://github.com/codeforpdx/recordexpungPDX.git
   ```
 5. Create a branch to work on. Replacing BRANCH_NAME with a descriptive name of the work planned such as `update_contributing_doc`
   ```bash
     $ git checkout -b BRANCH_NAME
   ```
 6. **Commit** changes to your branch (never to master)
 7. **Push** your work back up to your fork
   ```bash
     $ git push
   ```
   - NOTE: The first time you do `git push` on your branch it will error with:
   ```bash
    fatal: The current branch BRANCH_NAME has no upstream branch.
    To push the current branch and set the remote as upstream, use

        git push --set-upstream origin BRANCH_NAME
   ```
   - Copy the output and run it. Then afterwords simply push more commits by running `git push`.
 8. Submit a **Pull request**

- NOTE: For future contributions be sure to sync master with upstream
```bash
  $ git checkout master
  $ git pull upstream master
  $ git checkout -b BRANCH_NAME
```

  Python code should follow the [PEP8 standard](https://www.python.org/dev/peps/pep-0008/). Notably:

  * **module** names should be lowercase and run together, e.g. `mymodule`
  * **class** names should be camel case, e.g. `MyClass`
  * **method** and variable names should be snake case, e.g. `my_method()` and `my_var`


### Where to contribute

If you're wondering where to get started, the answer may best depend on what skills you want to use and/or develop:

If you're interested in frontend development, there are several core app components that are still missing or in progress. We're using React for page rendering and Redux and Typescript to manage the app. Many of us are quite new to these tools and we're learning as we go! Talk to Max or Forrest.

Python is used for the backend, and can be broken down further: if you're interested in working on implementing logic and object-oriented programming, check out the Expunger. It's also the core of the app that deals with the individual criminal records and checks eligibilty rules. It has been mostly completed according to the client specification, but there are a few bugs and additional features still on the todo list. Ask Nick, he built the thing and he posts a lot of tasks on the issues board!

Python is also used to expose our backend API, and to connect to the database. This is mostly for basic user account management, like changing user account settings or password. We don't save any collected or analyzed record data, but we plan to store some really basic usage statistics to report on the impact of our app. Ask Erik or Jordan.

Software architecture: we can use help here too. There are some features only partially documented and need to be reconciled with the existing code, or that haven't been fully designed.

Tech documentation: A lot of us dive in to just work on, and learn, one part of the app. Documentation would be great not just for new contributors, but to help us with the full stack integration too! We could use docstrings on the various components of our app, both frontend and backend. And, if you're a bit lost looking at our project, consider the folks who might want to join and help next month :)

Cloud and deployment: everyone hates it except for hiring managers. We haven't finished our deployment pipeline. We use Heroku for webapp hosting and Nginx for server configuration. Ask Nick or Jordan if you want to be able to say "cloud technologies" in a job interview.