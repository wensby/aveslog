import React from 'react';
import { Label } from './Label';
import { useCommonName } from '../bird/BirdHooks';

export function BirdSection({ bird }) {
  const { commonName, loading } = useCommonName(bird);

  return (
    <div className='form-group row'>
      <Label htmlFor='birdInput' label='bird-label' />
      <div className='col-sm-10'>
        <input id='birdInput' type='text' readOnly className='col-sm-10 form-control-plaintext' value={loading ? '' : commonName || bird.binomialName} />
      </div>
    </div>
  );
}
