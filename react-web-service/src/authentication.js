import React from 'react';

export default function Login() {

  return (
    <div className="container">
      <h1>Login</h1>
      <div className="d-flex justify-content-center">
        <div className="row">
          <div className="col">
            <div id="loginFormContainer">
              <form method="post">
                <div className="form-row">
                  <div className="form-group col-6">
                    <label htmlFor="usernameInput">Username</label>
                    <input id="usernameInput" className="form-control" type="text" name="username" placeholder="Username"/>
                  </div>
                  <div className="form-group col-6">
                    <label htmlFor="passwordInput">Password</label>
                    <input id="passwordInput" className="form-control" type="password" name="password" placeholder="Password"/>
                  </div>
                </div>
                <div className="d-flex flex-row">
                  <a className="btn btn-secondary" href="/">Register new account</a>
                  <button className="btn btn-primary ml-auto" type="submit">Login</button>
                </div>
              </form>
              <div className="row">
                <a href="/">Forgot your password?</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}