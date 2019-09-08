import React, { useState, } from 'react';
import { useTranslation } from 'react-i18next';
import { useReactRouter } from '../reactRouterHook';

export default () => {
  const { match } = useReactRouter();
  const token = match.params.token;
  const [alert, setAlert] = useState(null);
  const [email, setEmail] = useState('');
  const { t } = useTranslation();

  const renderAlert = () => {
    if (alert) {
      return (
        <div className='row'>
          <div className={`col alert alert-${alert.category}`} role='alert'>
            { alert.message }
          </div>
        </div>
      );
    }
  }

  const handleFormSubmit = async event => {
    try {
      event.preventDefault();
    }
    catch (err) {

    }
  }

  return (
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <h2>{ t('Register') }</h2>
          <p>
            { t('Fill out the following form to complete your registration.') }
          </p>
        </div>
      </div>
      {renderAlert()}
      <div className='row'>
        <div className='col'>
          <form onSubmit={handleFormSubmit}>
            <div className='form-group'>
              <label htmlFor='emailInput'>{ t('Email address') }</label>
              <input
                className='form-control'
                id='emailInput'
                type='text'
                name='email'
                readonly
                placeholder={ email }
                value={ email }/>
            </div>
            <div className='form-group'>
              <label htmlFor='usernameInput'>{ t('Username') }</label>
              <input
                id='usernameInput'
                className='form-control'
                type='username'
                name='username'
                aria-describedby='usernameHelpBlock'
                placeholder={ t('Username')}
                required
                pattern='[A-Za-z0-9._-]{5,32}'/>
              <small id='usernameHelpBlock' className='form-text text-muted'>
                { t('Must be 5 to 32 characters long, contain only letters, numbers, dashes (-), periods (.), and underscores (_).') }
              </small>
              <div className='valid-feedback'>
                { t('Nice username!') }
              </div>
            </div>
            <div className='form-group'>
              <label htmlFor='passwordInput'>{ t('Password') }</label>
              <input
                id='passwordInput'
                className='form-control'
                type='password'
                name='password'
                aria-describedby='passwordHelpBlock'
                placeholder={ t('Password')}
                required
                pattern='.{8,128}'/>
              <small id='passwordHelpBlock' className='form-text text-muted'>
                { t('Must be 8 to 128 character long.') }
              </small>
              <div className='valid-feedback'>
                { t('Seems long enough!') }
              </div>
              <div className='invalid-feedback'>
                { t('Needs more love.') }
              </div>
            </div>
            <div className='form-group'>
              <label htmlFor='confirmPasswordInput'>
                { t('Confirm password') }
              </label>
              <input
                id='confirmPasswordInput'
                className='form-control'
                type='password'
                name='confirmPassword'
                placeholder={ t('Confirm password')}/>
              <div className='valid-feedback'>
                { t('Both passwords matches!') }
              </div>
              <div className='invalid-feedback'>
                { t("Doesn't match your password above.") }
              </div>
            </div>
            <div className='form-group'>
              <div className='form-check'>
                <input
                  className='form-check-input'
                  type='checkbox'
                  value=''
                  id='tocCheckbox'
                  required/>
                <label className='form-check-label' htmlFor='tocCheckbox'>
                  { t('Agree to terms and conditions') }
                </label>
                <div className='invalid-feedback'>
                  { t('You must agree before submitting.') }
                </div>
              </div>
            </div>
            <input type='hidden' name='token' value={token}/>
            <button class='btn btn-primary' type='submit'>
              { t('Register') }
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
