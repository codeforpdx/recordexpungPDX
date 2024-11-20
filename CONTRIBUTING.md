# Contributing

This document provides some overall guidelines and suggestions for how to get started with contributing to the project. There are several features, enhancements, and fixes that we'd like to work on, so there are lots of opportunities to get started.

## Table of Contents
- [First steps](#first-steps)

- [Using Git](#using-git)

- [Where to contribute](#where-to-contribute)

- [How to use the Issues board](#how-to-use-the-issues-board)

### First steps

1. [Set up your local dev environment](README.md#installation)
2. Say hi on our Slack Channel!

### Using Git

* First, be sure that your local repo is a clone of your fork and not of the main project repository (see the main README.md).
* Define the `upstream` remote repository to be the main project repo on github:
`git remote add upstream https://github.com/codeforpdx/recordexpungPDX`

##### Creating a new feature branch

* Navigate to your local master branch: `$ git checkout master`
* Sync your local master branch with the upstream repository `$ git pull -r upstream master`
* Create a new branch for the issue you would like to work on ie: `$ git checkout -b name-of-new-branch`

At this point you should now be in your new branch and can begin working on the new feature or bug fix.

##### Once you have changes that you would like to make available for others to see and use:
* Run the backend unit tests and check that they all pass. In the main project directory, run `make dev_test`.
* Add the changes: `$ git add .` There are many versions of this command, consult docs mentioned below for more details or run `$ git help add` to get help in the terminal.
* Commit the changes: `$ git commit` This opens an editor to write your commit message. Consult articles about how to write a  good commit message; here is one by freeCodeCamp: https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/
* Update you local branch with the latest changes on the main repo: `git pull -r upstream master` (the `-r` flag makes this perform a rebase on `master`; see https://git-scm.com/docs/git-rebase)
* Push the changes to *your* remote repository: `$ git push origin name-of-new-branch`
* Open a Pull Request on the `codeforpdx/recordExpungPDX` repository referencing the issue that this PR addresses
* Please do not push direcly to a branch on the shared repo.
* Avoid making a local merge or update in your master branch. Your local changes should only be reflected in your master branch after they have merged on the github repo, and then pulled down again to sync to your local repo.

![image](https://user-images.githubusercontent.com/42503418/72772548-09f10380-3bb9-11ea-9564-ec40669f39fe.png)

* Request review.


![image](https://user-images.githubusercontent.com/42503418/72772596-2f7e0d00-3bb9-11ea-863c-9cb81f449a70.png)

* Move the issue from the `In Progress` column into the `Review` column.


![image](https://user-images.githubusercontent.com/42503418/72772499-ec239e80-3bb8-11ea-8ea6-a7ac5fdd65e6.png)

* Once your pull request has been approved, ensure it is up to date with the `codeforpdx/recordexpungPDX` master branch and then merge it into the repository.


![image](https://user-images.githubusercontent.com/42503418/72772654-589e9d80-3bb9-11ea-9ef8-cadd69c836cc.png)

* When you have merged the branch, close the issue if it is fully resolved.


![image](https://user-images.githubusercontent.com/42503418/72772728-8d125980-3bb9-11ea-8364-37f076f36fc8.png)


##### More information on general GitHub commands and tutorials:
* https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html
* https://try.github.io/
* https://www.atlassian.com/git/tutorials
* https://learngitbranching.js.org/?locale=en_US


### Where to contribute

If you're wondering where to get started, the answer may best depend on what skills you want to use and/or develop:

If you're interested in frontend development, there are several core app components that are still missing or in progress. We're using React for page rendering and Redux and Typescript to manage the app. Many of us are quite new to these tools and we're learning as we go! Talk to Jordan or Forrest.

Python is used for the backend, and can be broken down further: if you're interested in working on implementing functional logic programming, check out the Expunger. It's this is the core of the app that deals with the individual criminal records and checks eligibilty rules. It has been mostly completed according to the client specification, but there are a few bugs and additional features still on the todo list. Ask Jordan or Kent about this.

Python is also used to expose our backend API. We don't save any collected or analyzed record data, but we store some really basic usage statistics gathered from our nginx logs to report on the impact of our app. Ask Kent or Jordan.

Tech documentation: A lot of us dive in to just work on, and learn, one part of the app. Documentation would be great not just for new contributors, but to help us with the full stack integration too! We could use docstrings on the various components of our app, both frontend and backend. And, if you're a bit lost looking at our project, consider the folks who might want to join and help next month :)

### How to use the issues board

#### There are two different ratings systems to think about before choosing an issue to work on:

##### Complexity:
> This is a rough estimation of the time required to complete this task. It will be rated on a scale of 1 - 4. If this is the first issue you are going to take on, please consider choosing one with a complexity rating of 1

* 1 - Simple tasks, do not take much time to complete. A good starting point.


![image](https://user-images.githubusercontent.com/42503418/72772081-e5e0f280-3bb7-11ea-8d29-a343cf8827e3.png)

* 2 - Slightly more complex, may take more effort and some additional research.


![image](https://user-images.githubusercontent.com/42503418/72772124-0741de80-3bb8-11ea-8762-5c7a2ea3e6c6.png)

* 3 - These tasks may require some code refactoring and additional input or research to find the best solution to the problem.


![image](https://user-images.githubusercontent.com/42503418/72772162-16289100-3bb8-11ea-9fc7-68e565c079c7.png)

* 4 - These tasks will require changes including but not limited to: design changes, major refactors, new feature development, researching best practices, input from multiple team members. Do not let this dissuade you, please reach out to team members for help and guidance.


![image](https://user-images.githubusercontent.com/42503418/72772200-25a7da00-3bb8-11ea-9ea4-288df82f49fb.png)


##### Priority:
> This highlights the value completing this issue brings to the project. They will be scored either: Low, Medium, or High value. When possible please prioritize High value items as these will bring the most value to the application.

* High priority - Please work on these issues first when possible.


![image](https://user-images.githubusercontent.com/42503418/72771933-58050780-3bb7-11ea-83b7-72b029b1d46d.png)

* Medium priority - These will help the application be more useful and should be prioritized over things labeled as "Low".


![image](https://user-images.githubusercontent.com/42503418/72771980-7c60e400-3bb7-11ea-8b8b-c877f223f940.png)

* Low priority - These have a low impact on the overall functioning/improvement of the app. They are still useful and should be completed when other issues in "Ready to Start" are complete.


![image](https://user-images.githubusercontent.com/42503418/72772027-add9af80-3bb7-11ea-8c1c-a99676a8fef0.png)


---------
#### How to track the issue you are working on:

* Under the `Assignees` section select yourself.

* If you have any questions that will help you progress on the issue, please comment on the issue, or post to the Slack channel #recordsponge-dev
![image](https://user-images.githubusercontent.com/42503418/72772304-630c6780-3bb8-11ea-88d8-cde32f5488d8.png)

* if you are unable to complete an issue or do not have time to work on it within a few days, please remove yourself from the `Assignees` section. This ensures that we are able to consistently move forward with the current issues at hand. 

> We appreciate any and all help with this Volunteer based project, and may check in on issues that are assigned to individuals and that have not been updated in some time.

---
