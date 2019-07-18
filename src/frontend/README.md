Please see and use the [Wiki](https://github.com/codeforpdx/recordexpungPDX/wiki/Frontend) for all topics not related to setup and installation.

In particular, see the [Resources](https://github.com/codeforpdx/recordexpungPDX/wiki#resources) section at the bottom of the main page, which contains links to the click-through prototype and design system.

## Getting started:

1. Install Node JS, which includes `npm`. You are welcome to add more detailed platform-specific install instructions here.

2. Ensure you are in the `/src/frontend/` directory relative to the root `recordexpungPDX` directory.

3. Run `npm install` to install project dependencies.

4. Run `npm start`. This should start a development server and open http://localhost:3000/ in your browser, which should show the login page for our app, and you should see something like this in your terminal:

```
Compiled successfully!

You can now view record-expunge-pdx in the browser.

  Local:            http://localhost:3000/
  On Your Network:  http://192.168.14.37:3000/

Note that the development build is not optimized.
To create a production build, use npm run build.

Proxy error: Could not proxy request /sockjs-node/488/jgepgxci/websocket from localhost:3000 to http://localhost:5000.
See https://nodejs.org/api/errors.html#errors_common_system_errors for more information (ECONNREFUSED).

```

The proxy error is expected pending updates to the backend.


5. While developing frontend code, may be useful to run the app backend to have access to its api endpoints. This process runs in the project Docker stack, which also runs an instance of the frontend webserver, at the same port used by `npm start`. In order to run the the npm server instead, you can first launch the docker stack (see the README.md file at the project's top-level directory) and then kill the docker webserver with `docker service rm recordexpungpdx_webserver`. You can also locally prevent the webserver from running within the docker stack, by uncommenting the relevant lines in the docker-compose.dev.yml file at the top-level project directory.

If you run into any issues with the above steps, please ask someone for help.

- - -


The rest of this README is the text that [Create React App](https://github.com/facebook/create-react-app) (which we used to bootstrap the app) generates by default.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
