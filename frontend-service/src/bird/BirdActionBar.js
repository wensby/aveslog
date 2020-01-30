import React from 'react';
import { useAuthentication } from '../authentication/AuthenticationHooks';
import { SightingFormLinkButton } from "./SightingFormLinkButton";
import './BirdActionBar.scss';

export function BirdActionBar({ bird }) {
  const { account } = useAuthentication();
  return (
    <div className='bird-action-bar'>
      {account && <SightingFormLinkButton bird={bird} />}
    </div>
  );
}
