import React from 'react';
import { useTranslation } from "react-i18next";

export default function Login() {
  const { t } = useTranslation();

  return (
    <div className="container">
      <h1>{t('Login')}</h1>
      <div className="d-flex justify-content-center">
        <div className="row">
          <div className="col">
            <div id="loginFormContainer">
              <form method="post">
                <div className="form-row">
                  <div className="form-group col-6">
                    <label htmlFor="usernameInput">{t('Username')}</label>
                    <input id="usernameInput" className="form-control" type="text" name="username" placeholder={t('Username')}/>
                  </div>
                  <div className="form-group col-6">
                    <label htmlFor="passwordInput">{t('Password')}</label>
                    <input id="passwordInput" className="form-control" type="password" name="password" placeholder={t('Password')}/>
                  </div>
                </div>
                <div className="d-flex flex-row">
                  <a className="btn btn-secondary" href="/">{t('Register new account')}</a>
                  <button className="btn btn-primary ml-auto" type="submit">{t('Login')}</button>
                </div>
              </form>
              <div className="row">
                <a href="/">{t('Forgot your password?')}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}