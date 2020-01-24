# Contributing

This document provides some overall guidelines and suggestions for how to get started with contributing to the project. There are several features, enhancements, and fixes that we'd like to work on, so there are lots of opportunities to get started.

## Table of Contents
- [First steps](#first-steps)

- [Where to contribute](#where-to-contribute)

- [How to use the Project board](#how-to-use-the-project-board)

### First steps

1. [Set up your local dev environment](README.md#installation)
2. Be sure to read our [code of conduct](http://www.codeforpdx.org/about/conduct)
3. Say hi on our Slack Channel!

### Guidelines

Suggestions on submitting Issues and Pull Requests to be added here

### Where to contribute

If you're wondering where to get started, the answer may best depend on what skills you want to use and/or develop:

If you're interested in frontend development, there are several core app components that are still missing or in progress. We're using React for page rendering and Redux and Typescript to manage the app. Many of us are quite new to these tools and we're learning as we go! Talk to Max or Forrest.

Python is used for the backend, and can be broken down further: if you're interested in working on implementing logic and object-oriented programming, check out the Expunger. It's also the core of the app that deals with the individual criminal records and checks eligibilty rules. It has been mostly completed according to the client specification, but there are a few bugs and additional features still on the todo list. Ask Nick, he built the thing and he posts a lot of tasks on the issues board!

Python is also used to expose our backend API, and to connect to the database. This is mostly for basic user account management, like changing user account settings or password. We don't save any collected or analyzed record data, but we plan to store some really basic usage statistics to report on the impact of our app. Ask Erik or Jordan.

Software architecture: we can use help here too. There are some features only partially documented and need to be reconciled with the existing code, or that haven't been fully designed.

Tech documentation: A lot of us dive in to just work on, and learn, one part of the app. Documentation would be great not just for new contributors, but to help us with the full stack integration too! We could use docstrings on the various components of our app, both frontend and backend. And, if you're a bit lost looking at our project, consider the folks who might want to join and help next month :)

Cloud and deployment: everyone hates it except for hiring managers. We haven't finished our deployment pipeline. We use Heroku for webapp hosting and Nginx for server configuration. Ask Nick or Jordan if you want to be able to say "cloud technologies" in a job interview.

### How to use the project board

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

##### Assign yourself to the issue

* Under the `Assignees` section select yourself.


![image](https://user-images.githubusercontent.com/42503418/72772304-630c6780-3bb8-11ea-88d8-cde32f5488d8.png)

##### Move the issue to the `In Progress` column

* Drag the issue in to the column, or change it under the `Project` section, change it to `In Progress` in the drop down menu.


![image](https://user-images.githubusercontent.com/42503418/72772366-8800da80-3bb8-11ea-8151-4017aedeb632.png)


or


![image](https://user-images.githubusercontent.com/42503418/72772880-17f35400-3bba-11ea-8641-c879167f592a.png)


> Note: if you are unable to complete an issue or do not have time to work on it, please remove yourself from the `Assignees` section and move the issue back to the `Ready to Start` Column. This ensures that we are able to consistently move forward with the current issues at hand. We appreciate any and all help with this Volunteer based project, and may check in on issues that are assigned to individuals or remain in the `In Progress` column for an extended period of time.

---

#### General tips on how to work with GitHub:

##### Creating a new branch

* Navigate to your local master branch: `$ git checkout master`
* Sync your local master branch with the upstream repository `$ git pull -r upstream master`
* Create a new branch for the issue you would like to work on ie: `$ git checkout -b name-of-new-branch`

At this point you should now be in your new branch and can begin working on the new feature or bug fix.

##### Once you have changes that you would like to make available for others to see and use:
* Add the changes: `$ git add .` there are many versions of this command, consult docs mentioned below for more details or run `$ git help add` to get help in the terminal.
* Commit the changes: `$ git commit` consult articles about how to write a  good commit message here is one by freeCodeCamp: https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/
* Push the changes to *your* remote repository: `$ git push origin name-of-new-branch`
* Open a Pull Request on the `codeforpdx/recordExpungPDX` repository referencing the issue that this PR addresses


![image](https://user-images.githubusercontent.com/42503418/72772548-09f10380-3bb9-11ea-9564-ec40669f39fe.png)

* Request review.


![image](https://user-images.githubusercontent.com/42503418/72772596-2f7e0d00-3bb9-11ea-863c-9cb81f449a70.png)

* Move the issue from the `In Progress` column into the `Review` column.


![image](https://user-images.githubusercontent.com/42503418/72772499-ec239e80-3bb8-11ea-8ea6-a7ac5fdd65e6.png)

* Once your pull request has been approved, ensure it is up to date with the `codeforpdx/recordexpungPDX` master branch and then merge it into the repository.


![image](https://user-images.githubusercontent.com/42503418/72772654-589e9d80-3bb9-11ea-9ef8-cadd69c836cc.png)

* When you have merged the branch, if the issue is fully resolved move close it and move it into the done column.


![image](https://user-images.githubusercontent.com/42503418/72772728-8d125980-3bb9-11ea-8364-37f076f36fc8.png)


and


![image](https://user-images.githubusercontent.com/42503418/72772744-a0bdc000-3bb9-11ea-975a-8dcb2a6a3aa5.png)


##### More information on general GitHub commands and tutorials:
* https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html
* https://try.github.io/
* https://www.atlassian.com/git/tutorials
* https://learngitbranching.js.org/?locale=en_US