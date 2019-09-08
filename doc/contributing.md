If you're wondering where to get started, the answer may best depend on what skills you want to use and/or develop:

If you're interested in frontend development, there are several core app components that are still missing or in progress. We're using React for page rendering and Redux and Typescript to manage the multi-page app. Many of us are quite new to these tools and we're learning as we go! Talk to Max or Forrest.

Python is used for the backend, and can be broken down further: if you're interested in working on implementing logic and object-oriented programming, check out the Expunger. It's also the core of the app that deals with the individual criminal records and checks eligibilty rules.  It has been mostly completed according to the client specification, but there are a few bugs and additional features still on the todo list. Ask Nick, he built the thing and he posts a lot of tasks on the issues board!

Python is also used to expose our backend API, and to connect to the database. This is mostly for basic user account management, like changing user account settings or password. We don't save any collected or analyzed record data, but we plan to store some really basic usage statistics to report on the impact of our app. Ask Erik or Jordan.

Software architecture: we can use help here too. There are some features only partially documented and need to be reconciled with the existing code, or that haven't been fully designed.

Tech documentation: A lot of us dive in to just work on, and learn, one part of the app. Documentation would be great not just for new contributors, but to help us with the full stack integration too! We could use docstrings on the various components of our app, both frontend and backend. And, if you're a bit lost looking at our project, consider the folks who might want to join and help next month :)

Cloud and deployment: everyone hates it except for hiring managers. We haven't finished our deployment pipeline. We use Heroku for webapp hosting and Nginx for server configuration. Ask Nick or Jordan if you want to be able to say "cloud technologies" in a job interview.