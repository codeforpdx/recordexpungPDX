import React from "react";
import AppRouter from "../AppRouter";
import Footer from "../Footer";
import Header from "../Header";

class App extends React.Component {
  public render() {
    return (
      <>
        <Header />
        <AppRouter />
        <Footer />
      </>
    );
  }
}

export default App;
