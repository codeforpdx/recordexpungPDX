// https://create-react-app.dev/docs/running-tests/#initializing-test-environment

global.window.scrollTo = jest.fn();
global.window.alert = jest.fn();
global.IntersectionObserver = function () {
  return {
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
  };
};
