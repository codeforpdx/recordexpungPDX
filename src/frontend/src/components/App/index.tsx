import React from "react";
import AppRouter from "../AppRouter";
import Footer from "../Footer";

class App extends React.Component {
  public render() {
    return (
      <>
        <AppRouter />
        <Footer />
      </>
    );
  }
}

export default App;
